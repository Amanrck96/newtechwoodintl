import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = "${c.permissions.split(',').map(p => ' • ' + p.replace('_', ' ').toUpperCase()).join('\\n')}"
replacement = """${c.permissions.split(',').map(p => {
\t\t\t\t\tconst k = p.trim();
\t\t\t\t\tif (k === 'waltz_orders' || k === 'orders') return ' • NEWTECHWOOD ORDERS & DISPATCHES';
\t\t\t\t\tif (k === 'gopro_cad') return ' • GO PRO CAD & BIM LIBRARY';
\t\t\t\t\tif (k === 'pipeline_specs') return ' • PROJECT SPECS & BOQ';
\t\t\t\t\tif (k === 'wholesale_catalog') return ' • WHOLESALE CATALOG & PRICELISTS';
\t\t\t\t\tif (k === 'meetings') return ' • CONSULTATIONS & SAMPLES';
\t\t\t\t\tif (k === 'invitations') return ' • VIP PASSES & INVITATIONS';
\t\t\t\t\treturn ' • ' + k.replace(/_/g, ' ').replace(/waltz/gi, 'NewTechWood').toUpperCase();
\t\t\t\t}).join('\\n')}"""

assert target in content, "Target capability formatting string not found"
content = content.replace(target, replacement)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('admin/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated admin.html and admin/index.html capability slip formatting!")
