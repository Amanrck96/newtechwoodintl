import re

with open('admin/vendor.html', 'r', encoding='utf-8') as f:
    vnd = f.read()

# Check dashboard header buttons in vendor.html
dash_header = re.search(r'<div class="dashboard-header">.*?</div>\s*</div>', vnd, re.S)
if dash_header:
    print("Dashboard header in vendor.html:")
    print(dash_header.group(0))
else:
    print("Could not find dashboard header directly, searching for view-dashboard:")
    vdash = re.search(r'<section id="view-dashboard".*?</section>', vnd, re.S)
    if vdash:
        print(vdash.group(0)[:1500])
