"""Database connector and query helper for NewTechWood CRM."""
import os
import sys
import sqlite3
import threading
from typing import Any, Dict, List, Optional

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(_BASE_DIR, "ntw_crm.db")

# ── Vercel / read-only FS detection ──────────────────────────────────────────
# On Vercel the function bundle is mounted read-only. The only writable location
# is /tmp. We auto-detect this situation and redirect the DB there.
# On local dev (or Docker / Render) the bundled ntw_crm.db is used if present.

def _resolve_db_path() -> str:
    """Return the resolved database file path, taking Vercel / serverless constraints into account."""
    # Explicit override wins
    env_path = os.environ.get("CRM_DB_FILE", "").strip()
    if env_path:
        return env_path

    # If the canonical DB exists and is readable, use it
    if os.path.isfile(DB_FILE):
        return DB_FILE

    # Serverless / Lambda / Vercel: use /tmp (Linux) or OS tempdir (Windows)
    if os.path.isdir("/tmp") or not sys.platform.startswith("win"):
        return "/tmp/ntw_crm.db"
    import tempfile
    return os.path.join(tempfile.gettempdir(), "ntw_crm.db")


# ── Auto-bootstrap (schema + all default seed data) ──────────────────────────
_bootstrap_lock = threading.RLock()
_bootstrapped = False

def _hash_pw(plain: str) -> str:
    """Hash password using bcrypt if available, else sha256 fallback."""
    try:
        import bcrypt
        return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except ImportError:
        import hashlib, secrets
        salt = secrets.token_hex(16)
        h = hashlib.sha256((salt + plain).encode('utf-8')).hexdigest()
        return f"sha256${salt}${h}"


def _bootstrap_db(db_path: str) -> None:
    """Create all schema tables and seed essential users/data if the DB is fresh."""
    global _bootstrapped
    if _bootstrapped:
        return
    with _bootstrap_lock:
        if _bootstrapped:
            return

        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir and not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
            except Exception:
                pass

        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            # 1. Apply schema
            applied = False
            try:
                import schema_sql
                conn.executescript(schema_sql.SCHEMA_SQL)
                applied = True
            except Exception:
                pass

            if not applied:
                schema_path = os.path.join(_BASE_DIR, "schema.sql")
                if os.path.isfile(schema_path):
                    with open(schema_path, "r", encoding="utf-8") as f:
                        conn.executescript(f.read())
            conn.commit()

            # 2. Seed default users if users table has no superadmin
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users WHERE role IN ('admin', 'superadmin');")
            admin_count = cur.fetchone()[0]
            if admin_count == 0:
                users_data = [
                    ("admin", "ADMIN-001", "admin@newtechwood.in", _hash_pw("Admin@NTW2024"), "Super Administrator", "+91 99999 00001", "superadmin", "active", "all", "SA"),
                    ("admin_user", "ADMIN-002", "admin", _hash_pw("admin"), "System Administrator", "+91 99999 00002", "admin", "active", "all", "AD"),
                    ("sales_01", "SAL-2026-001", "sales@newtechwood.in", _hash_pw("sales123"), "Rohan Verma", "+91 98333 45678", "sales", "active", "pipeline,orders,meetings,visitors", "RV"),
                    ("arch_01", "VND-2026-001", "architect@studio.design", _hash_pw("UltraShield2026"), "Skyline Architecture Studio", "+91 98200 12345", "architect", "active", "gopro_cad,pipeline_specs,meetings,invitations", "SK"),
                    ("dlr_01", "DLR-902-IND", "dealer@lumberlife.in", _hash_pw("Dealer@2026"), "Lumber Life Premier Partner", "+91 98111 67890", "dealer", "active", "waltz_orders,wholesale_catalog,invitations", "LL"),
                ]
                cur.executemany("""
                    INSERT OR REPLACE INTO users (id, vendor_id, email, password, full_name, phone, role, status, permissions, avatar_initials)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, users_data)
                conn.commit()

            # 3. Seed product price list if products table is empty
            try:
                cur.execute("SELECT COUNT(*) FROM products;")
                if cur.fetchone()[0] == 0:
                    import seed_products
                    seed_products.seed(conn=conn)
            except Exception:
                pass

            # 4. Seed sample pipeline projects if table is empty
            try:
                cur.execute("SELECT COUNT(*) FROM pipeline_projects;")
                if cur.fetchone()[0] == 0:
                    import seed
                    seed.seed_database(conn=conn)
            except Exception:
                pass
        finally:
            conn.close()
        _bootstrapped = True


def get_connection() -> sqlite3.Connection:
    path = _resolve_db_path()
    _bootstrap_db(path)
    conn = sqlite3.connect(path, timeout=15.0)
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
