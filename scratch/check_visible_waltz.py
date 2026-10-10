import re
from bs4 import BeautifulSoup

for filename in ['admin.html', 'admin/index.html', 'admin/vendor.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check all visible strings
    visible_waltz = []
    for text in soup.stripped_strings:
        if 'waltz' in text.lower():
            visible_waltz.append(text)
    
    print(f"\nVisible text containing 'waltz' in {filename}:")
    if not visible_waltz:
        print("  NONE! (Clean)")
    else:
        for t in visible_waltz:
            print("  -", repr(t))
