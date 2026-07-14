import os
import re

workspace_dir = r"c:\Users\amanr\OneDrive\Documents\newtechwoodintl"

# 1. Read the clean header and footer from index.html
index_path = os.path.join(workspace_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

header_match = re.search(r'(<header\s+data-elementor-type="header".*?</header>)', index_content, re.DOTALL)
footer_match = re.search(r'(<footer\s+data-elementor-type="footer".*?</footer>)', index_content, re.DOTALL)

if not header_match or not footer_match:
    print("Error: Could not extract header or footer from index.html")
    exit(1)

clean_header = header_match.group(1)
clean_footer = footer_match.group(1)

print(f"Clean Header length: {len(clean_header)}")
print(f"Clean Footer length: {len(clean_footer)}")

# Quick sanity checks
assert 'Literature' not in clean_header, "ERROR: Literature still in header!"
assert 'EXPERIENCE CENTRE' in clean_header, "ERROR: EXPERIENCE CENTRE missing from header!"
assert 'Literature' not in clean_footer, "ERROR: Literature still in footer!"
assert 'Photo Gallery' not in clean_footer, "ERROR: Photo Gallery still in footer!"
assert 'Visualizer' not in clean_footer, "ERROR: Visualizer still in footer!"
print("Sanity checks passed!")

# Regex patterns to find header and footer in other files
header_regex = re.compile(r'<header\s+data-elementor-type="header".*?</header>', re.DOTALL)
footer_regex = re.compile(r'<footer\s+data-elementor-type="footer".*?</footer>', re.DOTALL)

files_updated = 0

for root, dirs, files in os.walk(workspace_dir):
    dirs[:] = [d for d in dirs if not d.startswith('.')]

    for file in files:
        if not file.lower().endswith('.html'):
            continue

        file_path = os.path.join(root, file)

        # Skip index.html — it's the source of truth
        if file_path == index_path:
            continue

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        original_content = content
        modified = False

        # Replace header
        if header_regex.search(content):
            content = header_regex.sub(clean_header, content)
            modified = True

        # Replace footer
        if footer_regex.search(content):
            content = footer_regex.sub(clean_footer, content)
            modified = True

        if modified and content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            files_updated += 1

print(f"Successfully synced header/footer to {files_updated} HTML files.")
