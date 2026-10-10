import re

with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find view-dashboard section
dash_match = re.search(r'<section id="view-dashboard"[^>]*>([\s\S]*?)</section>', html)
if dash_match:
    dash_html = dash_match.group(1)
    stat_ids = re.findall(r'id=["\']([^"\']+)["\']', dash_html)
    print("IDs in view-dashboard:")
    for sid in sorted(stat_ids):
        print(f"  - {sid}")
else:
    print("Could not find view-dashboard section")
