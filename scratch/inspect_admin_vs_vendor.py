import re

with open('admin.html', 'r', encoding='utf-8') as f:
    adm = f.read()

with open('admin/vendor.html', 'r', encoding='utf-8') as f:
    vnd = f.read()

# Let's inspect differences in HTML structure
print("Title in admin.html:", re.search(r'<title>(.*?)</title>', adm).group(1))
print("Title in admin/vendor.html:", re.search(r'<title>(.*?)</title>', vnd).group(1))

# Check route guard differences
print("\nAdmin route guard:")
print(re.search(r'<!-- ROUTE GUARD:.*?-->\s*<script>(.*?)</script>', adm, re.S).group(1).strip())
print("\nVendor route guard:")
print(re.search(r'<!-- ROUTE GUARD:.*?-->\s*<script>(.*?)</script>', vnd, re.S).group(1).strip())

# Check sidebar links
adm_links = re.findall(r'<a\s+class="sidebar-link"[^>]*onclick="([^"]+)"[^>]*>(.*?)</a>', adm, re.S)
vnd_links = re.findall(r'<a\s+class="sidebar-link"[^>]*onclick="([^"]+)"[^>]*>(.*?)</a>', vnd, re.S)

print(f"\nSidebar links in admin: {len(adm_links)}")
for l in adm_links:
    text = re.sub(r'<[^>]+>', ' ', l[1]).strip()
    print(" - admin:", l[0], "-->", ' '.join(text.split()))

print(f"\nSidebar links in vendor: {len(vnd_links)}")
for l in vnd_links:
    text = re.sub(r'<[^>]+>', ' ', l[1]).strip()
    print(" - vendor:", l[0], "-->", ' '.join(text.split()))
