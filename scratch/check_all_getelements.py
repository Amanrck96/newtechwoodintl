import re

with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
js_scripts = re.findall(r'<script(?![^>]*\bsrc\b)[^>]*>([\s\S]*?)<\/script>', html, re.IGNORECASE)
js_code = "\n".join(js_scripts)

lines = js_code.splitlines()

direct_calls = []
for idx, line in enumerate(lines, 1):
    matches = re.finditer(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)\.([a-zA-Z0-9_$]+)', line)
    for m in matches:
        el_id = m.group(1)
        prop = m.group(2)
        exists = el_id in html_ids
        direct_calls.append((idx, el_id, prop, exists, line.strip()))

print(f"Total direct calls: {len(direct_calls)}")
for idx, el_id, prop, exists, line in direct_calls:
    if not exists:
        print(f"FAILED: Line {idx}: ID '{el_id}' NOT in HTML! `{line}`")
    else:
        # print first 5 as sample
        pass
print("Done checking all direct getElementById calls.")
