"""Migration runner for NewTechWood CRM SQLite database."""
import os
import glob
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, "migrations")
DB_FILE = os.path.join(BASE_DIR, "ntw_crm.db")

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

    cursor.execute("SELECT version FROM schema_migrations;")
    applied = set(row[0] for row in cursor.fetchall())

    migration_files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.sql")))
    if not migration_files:
        print("No migration files found.")
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
            cursor.executescript(sql_script)
            cursor.execute("INSERT INTO schema_migrations (version) VALUES (?);", (version,))
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
