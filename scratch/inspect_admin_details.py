import re

with open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- VIEW CONTAINERS ---")
views = re.findall(r'id=["\'](view-[^"\']+)["\']', text)
for v in views:
    print(" ", v)

print("\n--- SIDEBAR NAVIGATION LINKS ---")
nav_items = re.findall(r'<a[^>]*data-view=["\']([^"\']+)["\'][^>]*>(.*?)</a>', text, re.DOTALL)
if nav_items:
    for view, label in nav_items:
        clean_label = re.sub(r'<[^>]+>', '', label).strip()
        print(f"  data-view='{view}' -> '{clean_label}'")
else:
    # check onclick
    links = re.findall(r'<a[^>]*class=["\'][^"\']*nav-item[^"\']*["\'][^>]*>(.*?)</a>', text, re.DOTALL)
    for l in links:
        print("  nav-item:", re.sub(r'<[^>]+>', ' ', l).strip())

print("\n--- HOW SWITCHING WORKS ---")
# find functions that manipulate view-
view_switchers = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\([^\)]*\)\s*\{[^}]*view-[^}]*\}', text)
print("Functions mentioning view-:", view_switchers)

# Check all functions in JS
funcs_with_view = []
for line in text.splitlines():
    if 'view-' in line or 'switchView' in line or 'showView' in line:
        funcs_with_view.append(line.strip())
for l in funcs_with_view[:20]:
    print(" ", l)
