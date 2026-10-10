import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['admin.html', 'admin/index.html', 'admin/vendor.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    # find all string literals: '...' or "..." or `...` that contain 'waltz' (case-insensitive)
    str_matches = re.findall(r'([\'\"`][^\'\"\`\n]*waltz[^\'\"\`\n]*[\'\"`])', content, re.IGNORECASE)
    print(f"\n--- {fname} JS / attribute string matches ({len(str_matches)}): ---")
    for m in set(str_matches):
        print(f"  {m}")
print("\nJS Audit finished.")
