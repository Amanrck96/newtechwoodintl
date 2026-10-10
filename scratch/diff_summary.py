import difflib

with open('admin.html', 'r', encoding='utf-8') as f:
    adm_lines = f.readlines()

with open('admin/vendor.html', 'r', encoding='utf-8') as f:
    vnd_lines = f.readlines()

print(f"admin.html lines: {len(adm_lines)}")
print(f"admin/vendor.html lines: {len(vnd_lines)}")

# Let's inspect major differences
diff = list(difflib.unified_diff(adm_lines, vnd_lines, fromfile='admin.html', tofile='admin/vendor.html', n=0))
print(f"Total diff lines: {len(diff)}")

# Let's see what is in vendor.html that is NOT in admin.html
added_in_vnd = [line for line in diff if line.startswith('+') and not line.startswith('+++')]
removed_from_vnd = [line for line in diff if line.startswith('-') and not line.startswith('---')]

print(f"Lines unique to vendor.html: {len(added_in_vnd)}")
print(f"Lines in admin.html but missing in vendor.html: {len(removed_from_vnd)}")

print("\nSample lines unique to vendor.html (first 25):")
for l in added_in_vnd[:25]:
    print(" ", l.strip()[:100])
