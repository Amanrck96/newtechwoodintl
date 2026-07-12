import os
import re

BASE_URL = 'https://www.newtechwoodintl.com'

def fix_html(html_content):
    """Fix root-relative and relative wp-content/wp-includes paths to absolute URLs"""
    # Fix root-relative paths like src="/wp-content/..." -> src="https://www.newtechwoodintl.com/wp-content/..."
    html_content = html_content.replace('src="/wp-content/', f'src="{BASE_URL}/wp-content/')
    html_content = html_content.replace("src='/wp-content/", f"src='{BASE_URL}/wp-content/")
    html_content = html_content.replace('href="/wp-content/', f'href="{BASE_URL}/wp-content/')
    html_content = html_content.replace("href='/wp-content/", f"href='{BASE_URL}/wp-content/")
    html_content = html_content.replace('src="/wp-includes/', f'src="{BASE_URL}/wp-includes/')
    html_content = html_content.replace("src='/wp-includes/", f"src='{BASE_URL}/wp-includes/")
    html_content = html_content.replace('href="/wp-includes/', f'href="{BASE_URL}/wp-includes/')
    html_content = html_content.replace("href='/wp-includes/", f"href='{BASE_URL}/wp-includes/")
    
    # Fix relative paths (no leading slash) - for older files
    html_content = html_content.replace("href='wp-content/", f"href='{BASE_URL}/wp-content/")
    html_content = html_content.replace('href="wp-content/', f'href="{BASE_URL}/wp-content/')
    html_content = html_content.replace("href='wp-includes/", f"href='{BASE_URL}/wp-includes/")
    html_content = html_content.replace('href="wp-includes/', f'href="{BASE_URL}/wp-includes/')
    html_content = html_content.replace("href='wp-json/", f"href='{BASE_URL}/wp-json/")
    html_content = html_content.replace('href="wp-json/', f'href="{BASE_URL}/wp-json/')
    
    html_content = html_content.replace("src='wp-content/", f"src='{BASE_URL}/wp-content/")
    html_content = html_content.replace('src="wp-content/', f'src="{BASE_URL}/wp-content/')
    html_content = html_content.replace("src='wp-includes/", f"src='{BASE_URL}/wp-includes/")
    html_content = html_content.replace('src="wp-includes/', f'src="{BASE_URL}/wp-includes/')
    
    # Fix CSS url() references  
    html_content = html_content.replace("url('wp-content/", f"url('{BASE_URL}/wp-content/")
    html_content = html_content.replace('url("wp-content/', f'url("{BASE_URL}/wp-content/')
    html_content = html_content.replace("url('/wp-content/", f"url('{BASE_URL}/wp-content/")
    html_content = html_content.replace('url("/wp-content/', f'url("{BASE_URL}/wp-content/')
    html_content = html_content.replace("url('wp-includes/", f"url('{BASE_URL}/wp-includes/")
    html_content = html_content.replace('url("wp-includes/', f'url("{BASE_URL}/wp-includes/')
    
    # Fix srcset attributes with relative/root-relative paths
    html_content = re.sub(r'srcset="(wp-content/)', lambda m: f'srcset="{BASE_URL}/' + m.group(1), html_content)
    html_content = re.sub(r'srcset="(/wp-content/)', lambda m: f'srcset="{BASE_URL}' + m.group(1), html_content)
    # Fix srcset mid-values like "... 300w, wp-content/..."
    html_content = re.sub(r',\s*wp-content/', lambda m: m.group().replace('wp-content/', BASE_URL + '/wp-content/'), html_content)
    html_content = re.sub(r',\s*/wp-content/', lambda m: m.group().replace('/wp-content/', BASE_URL + '/wp-content/'), html_content)
    
    return html_content

def count_issues(html):
    """Count remaining relative/root-relative wp- paths"""
    count = 0
    count += html.count("'wp-content/") + html.count('"wp-content/')
    count += html.count("'wp-includes/") + html.count('"wp-includes/')
    count += html.count("'/wp-content/") + html.count('"/wp-content/')
    count += html.count("'/wp-includes/") + html.count('"/wp-includes/')
    count += html.count("url('wp-content/") + html.count('url("wp-content/')
    count += html.count("url('/wp-content/") + html.count('url("/wp-content/')
    return count

# Find all index.html files
html_files = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            html_files.append(os.path.join(root, f))

print(f'Found {len(html_files)} HTML files')

fixed_files = 0
total_replacements = 0

for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        before_count = count_issues(content)
        # Also check for root-relative wp- paths  
        root_rel_count = content.count('src="/wp-content/') + content.count('href="/wp-content/') + \
                         content.count('src="/wp-includes/') + content.count('href="/wp-includes/')
        
        total_issues = before_count + root_rel_count
        
        if total_issues > 0:
            fixed = fix_html(content)
            after_count = count_issues(fixed) + \
                          fixed.count('src="/wp-content/') + fixed.count('href="/wp-content/')
            replacements = total_issues - after_count
            
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(fixed)
            
            total_replacements += replacements
            fixed_files += 1
            if fixed_files <= 20:
                print(f'  Fixed {filepath}: {replacements} replacements (before: {total_issues}, after: {after_count})')
    except Exception as e:
        print(f'  Error with {filepath}: {e}')

print(f'\nTotal: Fixed {fixed_files} files, {total_replacements} URL replacements')

# Verify index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()
root_remaining = idx_content.count('src="/wp-content/') + idx_content.count('href="/wp-content/')
print(f'\nindex.html root-relative refs remaining: {root_remaining}')
