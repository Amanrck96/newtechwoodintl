import re

with open('admin.html', 'r', encoding='utf-8') as f:
    adm = f.read()

with open('admin/vendor.html', 'r', encoding='utf-8') as f:
    vnd = f.read()

print("Comparing admin.html and admin/vendor.html:")

# Functions defined in admin.html
adm_funcs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', adm))
vnd_funcs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', vnd))

print(f"Functions in admin.html: {len(adm_funcs)}")
print(f"Functions in vendor.html: {len(vnd_funcs)}")

missing_in_vnd = adm_funcs - vnd_funcs
print("\nFunctions in admin.html but missing in vendor.html:")
for fn in sorted(missing_in_vnd):
    print(" -", fn)

missing_in_adm = vnd_funcs - adm_funcs
print("\nFunctions in vendor.html but missing in admin.html:")
for fn in sorted(missing_in_adm):
    print(" -", fn)
