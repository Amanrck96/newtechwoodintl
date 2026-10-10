import sys, os
sys.stdout.reconfigure(encoding='utf-8')

def apply_newtech_branding(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dashboard top button
    content = content.replace(
        '<button class="btn-gold" onclick="switchNav(\'waltz-orders\')">\n\t\t\t\t\t\t\t<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path></svg>\n\t\t\t\t\t\t\t<span>Orders</span>\n\t\t\t\t\t\t</button>',
        '<button class="btn-gold" onclick="switchNav(\'orders\')" title="View NewTechWood Commercial Orders">\n\t\t\t\t\t\t\t<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path></svg>\n\t\t\t\t\t\t\t<span>NewTechWood Orders</span>\n\t\t\t\t\t\t</button>'
    )
    # Also handle single-line or fallback button syntax
    content = content.replace(
        'onclick="switchNav(\'waltz-orders\')">\n\t\t\t\t\t\t\t<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path></svg>\n\t\t\t\t\t\t\t<span>Orders</span>',
        'onclick="switchNav(\'orders\')" title="View NewTechWood Commercial Orders">\n\t\t\t\t\t\t\t<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path></svg>\n\t\t\t\t\t\t\t<span>NewTechWood Orders</span>'
    )

    # In sidebar:
    content = content.replace(
        '<span class="sidebar-label">Orders</span>\n\t\t\t\t\t</a>\n\t\t\t\t\t<div class="sidebar-tooltip">Orders</div>',
        '<span class="sidebar-label">NewTechWood Orders</span>\n\t\t\t\t\t</a>\n\t\t\t\t\t<div class="sidebar-tooltip">NewTechWood Orders</div>'
    )
    content = content.replace(
        '<span class="sidebar-label">Orders</span>\n\t\t\t\t\t</a>\n\t\t\t\t\t<div class="sidebar-tooltip">Waltz Orders</div>',
        '<span class="sidebar-label">NewTechWood Orders</span>\n\t\t\t\t\t</a>\n\t\t\t\t\t<div class="sidebar-tooltip">NewTechWood Orders</div>'
    )

    # In Section Header:
    content = content.replace('<h1>Orders</h1>', '<h1>NewTechWood Orders</h1>')
    content = content.replace('<h1>Orders Management</h1>', '<h1>NewTechWood Orders</h1>')

    # Modals:
    content = content.replace('Add New Commercial Order', 'Add New NewTechWood Order')
    content = content.replace('Commercial Order Details', 'NewTechWood Order Details')

    # Badges:
    content = content.replace('📦 Orders', '📦 NewTechWood Orders')

    # SwitchNav router: support 'orders', 'newtech-orders', and 'waltz-orders'
    if "if (viewId === 'orders'" not in content:
        content = content.replace(
            "if (viewId === 'waltz-orders') loadWaltzOrders();",
            "if (viewId === 'orders' || viewId === 'newtech-orders' || viewId === 'waltz-orders') loadWaltzOrders();"
        )
    if "targetSection = document.getElementById('view-' + viewId);" in content:
        content = content.replace(
            "targetSection = document.getElementById('view-' + viewId);",
            "let targetSection = document.getElementById('view-' + viewId);\n\t\t\tif (!targetSection && (viewId === 'orders' || viewId === 'newtech-orders')) targetSection = document.getElementById('view-waltz-orders');"
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath} with NewTechWood Orders branding.")

apply_newtech_branding('admin.html')
apply_newtech_branding('admin/index.html')
apply_newtech_branding('admin/vendor.html')
