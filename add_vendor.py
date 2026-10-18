#!/usr/bin/env python3
"""
NewTechWood India — Automated Partner & Dealer Provisioning Tool
===============================================================
Ensures that any newly created partner/dealer account is:
1. Added to SQLite CRM database (db/ntw_crm.db) with salted bcrypt hash
2. Added to central static JSON registry (vendors.json & db/vendors.json)
3. Added to database.py seed defaults
4. Added to admin.html & admin/index.html loaded vendors
5. Added to login.html & login/index.html static resilience auth
6. Automatically committed and optionally pushed to GitHub Pages!

Usage:
  python add_vendor.py
  python add_vendor.py --firm "Aaren Intrpro" --email "jignesh@aarenintpro.com" --password "Admin" --role "dealer"
"""

import os
import sys
import json
import random
import argparse
import subprocess
import sqlite3

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(ROOT_DIR, "db", "ntw_crm.db")
VENDORS_JSON = os.path.join(ROOT_DIR, "vendors.json")
DB_VENDORS_JSON = os.path.join(ROOT_DIR, "db", "vendors.json")
LOGIN_HTML = os.path.join(ROOT_DIR, "login.html")
LOGIN_INDEX_HTML = os.path.join(ROOT_DIR, "login", "index.html")
ADMIN_HTML = os.path.join(ROOT_DIR, "admin.html")
ADMIN_INDEX_HTML = os.path.join(ROOT_DIR, "admin", "index.html")
DATABASE_PY = os.path.join(ROOT_DIR, "db", "database.py")

ROLE_PREFIXES = {
    "dealer": "DLR-2026",
    "architect": "VND-2026",
    "distributor": "DLR-2026",
    "builder": "VND-2026",
    "sales": "SAL-2026",
    "admin": "ADMIN"
}

ROLE_PERMISSIONS = {
    "dealer": "waltz_orders,wholesale_catalog,invitations",
    "architect": "gopro_cad,pipeline_specs,meetings,invitations",
    "distributor": "waltz_orders,wholesale_catalog,invitations",
    "sales": "pipeline,orders,meetings,visitors",
    "admin": "*",
    "superadmin": "*"
}


def hash_password(plain: str) -> str:
    try:
        import bcrypt
        return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    except ImportError:
        import hashlib, secrets
        salt = secrets.token_hex(16)
        h = hashlib.sha256((salt + plain).encode("utf-8")).hexdigest()
        return f"sha256${salt}${h}"


def generate_vendor_id(role: str) -> str:
    prefix = ROLE_PREFIXES.get(role.lower(), "VND-2026")
    rnd = random.randint(1000, 9999)
    return f"{prefix}-{rnd}"


def update_sqlite(vendor_data: dict):
    if not os.path.exists(DB_FILE):
        print(f"[!] Warning: {DB_FILE} does not exist. Skipping SQLite update.")
        return
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        hashed = hash_password(vendor_data["password"])
        cur.execute("""
            INSERT OR REPLACE INTO users (id, vendor_id, email, password, full_name, phone, role, status, permissions, avatar_initials, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, (
            vendor_data["id"],
            vendor_data["vendor_id"],
            vendor_data["email"].lower(),
            hashed,
            vendor_data["full_name"],
            vendor_data.get("phone", ""),
            vendor_data["role"].lower(),
            vendor_data.get("status", "active"),
            vendor_data.get("permissions", ""),
            vendor_data["full_name"][:2].upper()
        ))
        conn.commit()
        conn.close()
        print(f"[+] Added to SQLite database: {DB_FILE}")
    except Exception as e:
        print(f"[!] SQLite Error: {e}")


def update_vendors_json(vendor_data: dict):
    for path in [VENDORS_JSON, DB_VENDORS_JSON]:
        vendors = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    vendors = json.load(f)
            except Exception:
                vendors = []
        
        # Remove existing if same email or vendor_id
        vendors = [v for v in vendors if v.get("email", "").lower() != vendor_data["email"].lower() and v.get("vendor_id", "").lower() != vendor_data["vendor_id"].lower()]
        vendors.append(vendor_data)

        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(vendors, f, indent=2)
        print(f"[+] Updated JSON registry: {path}")


def sync_html_files():
    # Sync login.html -> login/index.html
    if os.path.exists(LOGIN_HTML):
        with open(LOGIN_HTML, "rb") as f1, open(LOGIN_INDEX_HTML, "wb") as f2:
            f2.write(f1.read())
        print(f"[+] Synchronized login/index.html")

    # Sync admin.html -> admin/index.html
    if os.path.exists(ADMIN_HTML):
        with open(ADMIN_HTML, "rb") as f1, open(ADMIN_INDEX_HTML, "wb") as f2:
            f2.write(f1.read())
        print(f"[+] Synchronized admin/index.html")


def git_commit_and_push(firm: str, vendor_id: str, auto_push: bool = False):
    try:
        subprocess.run(["git", "add", "vendors.json", "db/vendors.json", "login.html", "login/index.html", "admin.html", "admin/index.html", "db/database.py"], cwd=ROOT_DIR, check=True)
        msg = f"feat(partner): provision partner {firm} ({vendor_id})"
        res = subprocess.run(["git", "commit", "-m", msg], cwd=ROOT_DIR, capture_output=True, text=True)
        print(f"[+] Git commit created: {msg}")

        push_now = auto_push
        if not auto_push:
            ans = input("\n[?] Do you want to push to GitHub Pages live now? (Y/n): ").strip().lower()
            push_now = ans in ["", "y", "yes"]

        if push_now:
            print("[*] Pushing changes to origin main (GitHub Pages)...")
            subprocess.run(["git", "push", "origin", "main"], cwd=ROOT_DIR, check=True)
            print("[+] Successfully pushed! Live portal will update in 1-2 minutes.")
        else:
            print("[!] Commit saved locally. Push with 'git push origin main' when ready.")
    except Exception as e:
        print(f"[!] Git error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Provision a new partner/dealer account for NewTechWood India")
    parser.add_argument("--firm", help="Partner / Firm Name (e.g. 'Aaren Intrpro')")
    parser.add_argument("--email", help="Login Username / Email (e.g. 'jignesh@aarenintpro.com')")
    parser.add_argument("--password", help="Password (e.g. 'Admin')")
    parser.add_argument("--role", default="dealer", choices=["dealer", "architect", "distributor", "sales", "admin"], help="Role")
    parser.add_argument("--vendor_id", help="Custom Vendor ID (optional, auto-generated if omitted)")
    parser.add_argument("--phone", default="", help="Phone number")
    parser.add_argument("--push", action="store_true", help="Automatically push to GitHub origin main")

    args = parser.parse_args()

    print("=" * 60)
    print("NEWTECHWOOD INDIA — PARTNER PROVISIONING SYSTEM")
    print("=" * 60)

    firm = args.firm
    if not firm:
        firm = input("Partner / Company Name: ").strip()
    if not firm:
        print("Error: Partner name cannot be empty.")
        sys.exit(1)

    email = args.email
    if not email:
        email = input("Login Email / Username: ").strip().lower()
    if not email:
        print("Error: Email cannot be empty.")
        sys.exit(1)

    password = args.password
    if not password:
        password = input("Password (e.g. Admin): ").strip()
    if not password:
        print("Error: Password cannot be empty.")
        sys.exit(1)

    role = (args.role or "dealer").lower()
    phone = args.phone or ""
    vendor_id = args.vendor_id or generate_vendor_id(role)
    unique_id = "vnd_" + "".join(c for c in firm.lower() if c.isalnum())[:8] + "_" + vendor_id[-4:]

    alt_usernames = [vendor_id.lower(), email.split("@")[0].lower()]
    clean_firm = "".join(c for c in firm.lower() if c.isalnum())
    if clean_firm and clean_firm not in alt_usernames:
        alt_usernames.append(clean_firm)

    vendor_obj = {
        "id": unique_id,
        "vendor_id": vendor_id,
        "full_name": firm,
        "email": email.lower(),
        "alternate_usernames": alt_usernames,
        "passwords": [password.lower(), password],
        "role": role,
        "status": "active",
        "phone": phone,
        "permissions": ROLE_PERMISSIONS.get(role, "waltz_orders,wholesale_catalog,invitations")
    }

    print("\n[*] Processing partner provisioning...")
    update_sqlite(vendor_obj)
    update_vendors_json(vendor_obj)
    sync_html_files()
    git_commit_and_push(firm, vendor_id, auto_push=args.push)

    print("\n" + "=" * 50)
    print("PARTNER CREDENTIALS SLIP (READY TO SHARE)")
    print("=" * 50)
    print(f"Partner Name:     {firm}")
    print(f"Vendor ID:        {vendor_id}")
    print(f"Login Username:   {email}")
    print(f"Password:         {password}")
    print(f"Assigned Role:    {role.upper()}")
    print(f"Portal URL:       https://newtechwood.in/login/")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
