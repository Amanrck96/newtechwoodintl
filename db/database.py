"""Database connector and query helper for NewTechWood CRM."""
import os
import sqlite3
import threading
from typing import Any, Dict, List, Optional

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(_BASE_DIR, "ntw_crm.db")

# ── Vercel / read-only FS detection ──────────────────────────────────────────
# On Vercel the function bundle is mounted read-only. The only writable location
# is /tmp. We auto-detect this situation and redirect the DB there.
# On local dev (or Docker / Render) the bundled ntw_crm.db is used as-is.

def _resolve_db_path() -> str:
    """Return the resolved database file path, taking Vercel constraints into account."""
    # Explicit override wins
    env_path = os.environ.get("CRM_DB_FILE", "").strip()
    if env_path:
        return env_path

    # If the canonical DB exists and is readable, use it
    if os.path.isfile(DB_FILE):
        return DB_FILE

    # Vercel / ephemeral environment: use /tmp
    tmp_db = "/tmp/ntw_crm.db"
    return tmp_db


# ── Auto-bootstrap (schema + admin seed) ─────────────────────────────────────
_bootstrap_lock = threading.Lock()
_bootstrapped = False

def _bootstrap_db(db_path: str) -> None:
    """Create schema and seed a superadmin user if the DB is empty/new."""
    global _bootstrapped
    if _bootstrapped:
        return
    with _bootstrap_lock:
        if _bootstrapped:
            return
        schema_path = os.path.join(_BASE_DIR, "schema.sql")
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            # Apply schema (CREATE TABLE IF NOT EXISTS, idempotent)
            if os.path.isfile(schema_path):
                with open(schema_path, "r", encoding="utf-8") as f:
                    schema_sql = f.read()
                # Execute statement by statement (SQLite doesn't support executescript in WAL easily)
                for stmt in schema_sql.split(";"):
                    s = stmt.strip()
                    if s and not s.startswith("--"):
                        try:
                            conn.execute(s)
                        except sqlite3.OperationalError:
                            pass  # ignore duplicate column / already-exists errors
                conn.commit()

            # Seed superadmin if users table is empty
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users;")
            count = cur.fetchone()[0]
            if count == 0:
                # Hash password using bcrypt (available via requirements.txt) or sha256 fallback
                admin_pw = "Admin@NTW2024"
                try:
                    import bcrypt as _bcrypt
                    hashed = _bcrypt.hashpw(admin_pw.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")
                except ImportError:
                    import hashlib, secrets
                    salt = secrets.token_hex(16)
                    h = hashlib.sha256((salt + admin_pw).encode("utf-8")).hexdigest()
                    hashed = f"sha256${salt}${h}"

                cur.execute(
                    "INSERT OR IGNORE INTO users (id, email, password, full_name, role, status, avatar_initials) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?);",
                    ("admin", "admin@newtechwood.in", hashed, "Super Administrator", "superadmin", "active", "SA"),
                )
                conn.commit()
        finally:
            conn.close()
        _bootstrapped = True

def get_connection() -> sqlite3.Connection:
    path = _resolve_db_path()
    _bootstrap_db(path)
    conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def execute_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

def execute_commit(query: str, params: tuple = ()) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid or cursor.rowcount

def execute_many(query: str, param_list: List[tuple]) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(query, param_list)
        conn.commit()
        return cursor.rowcount
