"""Migration runner for NewTechWood CRM SQLite database.
Phase 1 updates:
- Handles idempotent ALTER TABLE (SQLite doesn't support IF NOT EXISTS on columns)
- Hashes existing plain-text passwords with bcrypt on first run
- Adds `stage` column to pipeline_projects if missing
"""
import os
import glob
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, "migrations")
DB_FILE = os.path.join(BASE_DIR, "ntw_crm.db")

# ─── Password hashing (bcrypt preferred, hashlib+salt fallback) ───────────────
try:
    import bcrypt
    def hash_password(plain: str) -> str:
        return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    def verify_password(plain: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    HASH_ALGO = 'bcrypt'
except ImportError:
    import hashlib, secrets
    def hash_password(plain: str) -> str:
        salt = secrets.token_hex(16)
        h = hashlib.sha256((salt + plain).encode('utf-8')).hexdigest()
        return f"sha256${salt}${h}"
    def verify_password(plain: str, hashed: str) -> bool:
        try:
            if hashed.startswith('sha256$'):
                _, salt, h = hashed.split('$')
                return hashlib.sha256((salt + plain).encode('utf-8')).hexdigest() == h
            return False
        except Exception:
            return False
    HASH_ALGO = 'sha256'

def _is_already_hashed(pw: str) -> bool:
    """Return True if password looks like a hash (bcrypt or sha256 format)."""
    return pw.startswith('$2b$') or pw.startswith('$2a$') or pw.startswith('sha256$')

def _ensure_stage_column(cursor):
    """Add stage column to pipeline_projects if missing (schema.sql omitted it)."""
    cursor.execute("PRAGMA table_info(pipeline_projects);")
    cols = [row[1] for row in cursor.fetchall()]
    if 'stage' not in cols:
        print("[FIX] Adding missing `stage` column to pipeline_projects...")
        cursor.execute(
            "ALTER TABLE pipeline_projects ADD COLUMN stage TEXT NOT NULL DEFAULT 'Pipeline' "
            "CHECK(stage IN ('Pipeline', 'Win', 'Lost'));"
        )
        print("[FIX] `stage` column added.")
    else:
        print("[OK] `stage` column already exists in pipeline_projects.")

def _hash_plain_passwords(cursor):
    """One-time migration: hash any plain-text passwords found in users table."""
    cursor.execute("SELECT id, password FROM users;")
    rows = cursor.fetchall()
    updated = 0
    for row in rows:
        uid, pw = row[0], row[1]
        if pw and not _is_already_hashed(pw):
            hashed = hash_password(pw)
            cursor.execute("UPDATE users SET password = ? WHERE id = ?;", (hashed, uid))
            updated += 1
    if updated:
        print(f"[SECURITY] Hashed {updated} plain-text password(s) using {HASH_ALGO}.")
    else:
        print(f"[OK] All passwords already hashed.")

def run_migrations():
    print(f"Connecting to database: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create migrations table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    # ── Phase 1 structural fixes (run every time, idempotent) ──────────────────
    _ensure_stage_column(cursor)
    _hash_plain_passwords(cursor)
    conn.commit()

    cursor.execute("SELECT version FROM schema_migrations;")
    applied = set(row[0] for row in cursor.fetchall())

    migration_files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.sql")))
    if not migration_files:
        print("No migration files found.")
        conn.close()
        return

    for fpath in migration_files:
        version = os.path.basename(fpath)
        if version in applied:
            print(f"[SKIP] Migration {version} already applied.")
            continue

        print(f"[APPLYING] Migration {version}...")
        with open(fpath, "r", encoding="utf-8") as f:
            sql_script = f.read()

        try:
            # Run statements one by one so ALTER TABLE errors can be caught per-statement
            for stmt in sql_script.split(';'):
                # Strip out line comments so statements starting with comments are not skipped
                clean_lines = [l for l in stmt.splitlines() if not l.strip().startswith('--')]
                stmt = '\n'.join(clean_lines).strip()
                if not stmt:
                    continue
                try:
                    cursor.execute(stmt)
                except sqlite3.OperationalError as e:
                    err = str(e).lower()
                    # Ignore "duplicate column" errors (idempotent ALTERs from 002/003)
                    if 'duplicate column' in err or 'already exists' in err:
                        print(f"  [SKIP-STMT] Idempotent: {e}")
                    else:
                        raise

            cursor.execute("INSERT OR IGNORE INTO schema_migrations (version) VALUES (?);", (version,))
            conn.commit()
            print(f"[SUCCESS] Migration {version} applied successfully.")
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Migration {version} failed: {e}", file=sys.stderr)
            raise e

    conn.close()
    print("All migrations completed successfully!")

if __name__ == "__main__":
    run_migrations()
