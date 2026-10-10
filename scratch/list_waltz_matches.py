import re

for filename in ['admin.html', 'admin/index.html', 'admin/vendor.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    waltz_matches = re.findall(r'.{0,40}waltz.{0,40}', content, re.IGNORECASE)
    print(f"\n==============================")
    print(f"File: {filename} (Total waltz matches: {len(waltz_matches)})")
    print(f"==============================")
    for m in waltz_matches[:15]:
        print(" ->", m.strip())
