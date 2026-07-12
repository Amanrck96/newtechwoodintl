with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

print('=== Checking URL patterns in index.html ===')
print('File size:', len(content))
print()

# Check for wp-content relative refs
wp_content_count = content.count("'wp-content/") + content.count('"wp-content/')
wp_includes_count = content.count("'wp-includes/") + content.count('"wp-includes/')
print(f'Relative wp-content refs: {wp_content_count}')
print(f'Relative wp-includes refs: {wp_includes_count}')
print()

# Find first few examples
idx = content.find("wp-content/")
if idx >= 0:
    print('Sample wp-content context:')
    print(repr(content[max(0,idx-30):idx+60]))
print()

# Check absolute refs
abs_count = content.count('https://www.newtechwoodintl.com/wp-content/')
print(f'Absolute https://www.newtechwoodintl.com/wp-content/ refs: {abs_count}')

# Check for src= patterns
src_patterns = re.findall(r'src=["\'][^"\']+["\']', content)
print(f'\nTotal src= patterns: {len(src_patterns)}')
print('First 5 src= values:')
for s in src_patterns[:5]:
    print(f'  {s[:100]}')
