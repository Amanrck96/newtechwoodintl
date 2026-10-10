import re

with open('admin.html', 'r', encoding='utf-8') as f:
    adm = f.read()

with open('admin/vendor.html', 'r', encoding='utf-8') as f:
    vnd = f.read()

print("admin.html length:", len(adm))
print("admin/vendor.html length:", len(vnd))

adm_sections = re.findall(r'<section\s+id=["\']([^"\']+)["\']', adm)
vnd_sections = re.findall(r'<section\s+id=["\']([^"\']+)["\']', vnd)

print("\nadmin.html sections:")
for s in adm_sections:
    print(" -", s)

print("\nadmin/vendor.html sections:")
for s in vnd_sections:
    print(" -", s)

# Find modals in both
adm_modals = re.findall(r'id=["\']([^"\']*modal[^"\']*)["\']', adm, re.I)
vnd_modals = re.findall(r'id=["\']([^"\']*modal[^"\']*)["\']', vnd, re.I)

print("\nadmin.html modals:", set(adm_modals))
print("admin/vendor.html modals:", set(vnd_modals))

# Missing in vendor:
print("\nModals in admin but not vendor:", set(adm_modals) - set(vnd_modals))
