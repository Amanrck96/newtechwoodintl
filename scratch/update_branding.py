import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def update_file(path, replacements):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)
    total_replaced = 0
    for old, new in replacements:
        cnt = content.count(old)
        if cnt > 0:
            content = content.replace(old, new)
            total_replaced += cnt
            print(f"[{path}] Replaced '{old[:40]}' ({cnt}x) -> '{new[:40]}'")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{path}] Done. Total replacements: {total_replaced}\n")

admin_replacements = [
    ('>Waltz Orders<', '>Orders<'),
    ('"Waltz Orders"', '"Orders"'),
    ("<span>Waltz Orders</span>", "<span>Orders</span>"),
    ("<h1>Waltz Orders</h1>", "<h1>Orders Management</h1>"),
    ("<!-- 5. WALTZ ORDERS -->", "<!-- 5. ORDERS -->"),
    ("VIEW 8: WALTZ ORDERS", "VIEW 8: ORDERS MANAGEMENT"),
    ("<!-- Waltz Orders Table", "<!-- Orders Table"),
    ("Waltz Order &amp; Wholesale Access", "Orders &amp; Wholesale Access"),
    ("Track Waltz material dispatches allocated to specified projects.", "Track NewTechWood material dispatches allocated to specified projects."),
    ("<strong>Waltz Orders Workflow:</strong>", "<strong>Commercial Orders Workflow:</strong>"),
    ("Waltz Commercial Orders (PO Placement &amp; Dispatches)", "Commercial Orders (PO Placement &amp; Dispatches)"),
    ("Add New Waltz Commercial Order", "Add New Commercial Order"),
    ("Waltz Commercial Order Details", "Commercial Order Details"),
    ("Waltz Orders, Wholesale Catalogs", "Orders, Wholesale Catalogs"),
    ("Waltz Orders &amp; Dispatches", "Orders &amp; Dispatches"),
    ("Configured for Dealer: Waltz commercial orders", "Configured for Dealer: Commercial material orders"),
    ("📦 Waltz Orders", "📦 Orders"),
    ("<strong>Waltz Commercial Orders:</strong>", "<strong>Commercial Orders:</strong>"),
    ("Waltz_Commercial_Orders_", "NewTechWood_Orders_"),
    ("item.activity_type === 'Waltz Order'", "item.activity_type === 'Waltz Order' || item.activity_type === 'Material Order' || item.activity_type === 'Order'"),
]

vendor_replacements = [
    ('>Waltz Orders<', '>Orders<'),
    ('"Waltz Orders"', '"Orders"'),
    ("<span>Waltz Orders</span>", "<span>Orders</span>"),
    ("<h1>Waltz Orders</h1>", "<h1>Orders Management</h1>"),
    ("<!-- 5. WALTZ ORDERS -->", "<!-- 5. ORDERS -->"),
    ("VIEW 8: WALTZ ORDERS", "VIEW 8: ORDERS MANAGEMENT"),
    ("<!-- Waltz Orders Table", "<!-- Orders Table"),
    ("Add New Waltz Commercial Order", "Add New Commercial Order"),
    ("Waltz Commercial Order Details", "Commercial Order Details"),
    ("Waltz_Commercial_Orders_", "NewTechWood_Orders_"),
    ("item.activity_type === 'Waltz Order'", "item.activity_type === 'Waltz Order' || item.activity_type === 'Material Order' || item.activity_type === 'Order'"),
]

# 1. Update admin.html
update_file('admin.html', admin_replacements)

# 2. Update admin/index.html
update_file('admin/index.html', admin_replacements)

# 3. Update admin/vendor.html
update_file('admin/vendor.html', vendor_replacements)
