import re

with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

js_scripts = re.findall(r'<script(?![^>]*\bsrc\b)[^>]*>([\s\S]*?)<\/script>', html, re.IGNORECASE)
js_code = "\n".join(js_scripts)

# Find all occurrences of document.getElementById in js_code
lines = js_code.splitlines()
print(f"Total JS lines: {len(lines)}")

null_access_risks = []
for idx, line in enumerate(lines, 1):
    # Match patterns like document.getElementById('...').someProperty
    # without preceding check or assignment
    matches = re.finditer(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)\.([a-zA-Z0-9_$]+)', line)
    for m in matches:
        el_id = m.group(1)
        prop = m.group(2)
        null_access_risks.append((idx, line.strip(), el_id, prop))

print(f"Direct unvalidated getElementById property accesses: {len(null_access_risks)}")
# Filter to those where element ID doesn't exist or might not exist
html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
for idx, line, el_id, prop in null_access_risks:
    exists = el_id in html_ids
    if not exists:
        print(f"CRITICAL: Line {idx}: ID '{el_id}' NOT in HTML! `{line}`")

print("\n--- CHECKING ALL FETCH CALLS FOR ERROR HANDLING ---")
fetch_lines = [(i+1, l.strip()) for i, l in enumerate(lines) if 'fetch(' in l]
for idx, line in fetch_lines:
    print(f"Line {idx}: {line}")

print("\n--- CHECKING LOCALSTORAGE USAGE ---")
ls_lines = [(i+1, l.strip()) for i, l in enumerate(lines) if 'localStorage' in l]
print(f"Total localStorage accesses: {len(ls_lines)}")

print("\n--- CHECKING JSON.parse WITHOUT TRY/CATCH ---")
for idx, line in enumerate(lines, 1):
    if 'JSON.parse(' in line:
        # Check context
        surrounding = "\n".join(lines[max(0, idx-5):min(len(lines), idx+5)])
        if 'try' not in surrounding:
            print(f"POTENTIAL UNHANDLED JSON.parse: Line {idx}: {line.strip()}")
