import sqlite3
import urllib.request
import json

conn = sqlite3.connect('db/ntw_crm.db')
cur = conn.cursor()
cur.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view')")
print("Database tables and views:")
for name, typ in cur.fetchall():
    print(f" - {typ.upper()}: {name}")

# Check order rows
cur.execute("SELECT id, order_number, project_name, client_name, final_amount, status FROM waltz_orders LIMIT 5")
print("\nSample orders in DB:")
for r in cur.fetchall():
    print(" -", r)

# Test GET /api/health
try:
    with urllib.request.urlopen('http://localhost:8000/api/health') as resp:
        print("\nGET /api/health:", resp.status, json.loads(resp.read().decode('utf-8')))
except Exception as e:
    print("\nGET /api/health error:", e)

# Test GET /api/orders
try:
    with urllib.request.urlopen('http://localhost:8000/api/orders') as resp:
        print("\nGET /api/orders:", resp.status, json.loads(resp.read().decode('utf-8')))
except Exception as e:
    print("\nGET /api/orders error:", e)

# Test GET /api/vendors
try:
    with urllib.request.urlopen('http://localhost:8000/api/vendors') as resp:
        print("\nGET /api/vendors:", resp.status, json.loads(resp.read().decode('utf-8')))
except Exception as e:
    print("\nGET /api/vendors error:", e)
