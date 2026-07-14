import re
import os

workspace_dir = r"c:\Users\amanr\OneDrive\Documents\newtechwoodintl"

html_files_updated = 0

for root, dirs, files in os.walk(workspace_dir):
    dirs[:] = [d for d in dirs if not d.startswith('.')]

    for file in files:
        if not file.lower().endswith('.html'):
            continue

        file_path = os.path.join(root, file)

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        original = content
        modified = False

        # 1. Replace "FIND A DISTRIBUTOR" with "EXPERIENCE CENTRE" (in data-settings JSON attribute - encoded)
        if 'FIND A DISTRIBUTOR' in content:
            content = content.replace('FIND A DISTRIBUTOR', 'EXPERIENCE CENTRE')
            modified = True

        # 2. Replace "Find a Distributor" (in visible nav span text and footer links)
        if 'Find a Distributor' in content:
            content = content.replace('Find a Distributor', 'Experience Centre')
            modified = True

        # 3. Remove "Literature" sub-menu block from WHY NEWTECHWOOD? dropdown
        #    The block is: elementor-element-c663bf6 container with Literature heading + text + icon
        lit_pattern = re.compile(
            r'\s*<div class="elementor-element elementor-element-c663bf6[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>',
            re.DOTALL
        )
        new_content, count = lit_pattern.subn("", content)
        if count > 0:
            content = new_content
            modified = True

        # 4. Remove "Photo Gallery" link from footer
        if 'Photo Gallery' in content:
            content = re.sub(r'<p><a href="[^"]*galleries[^"]*">Photo Gallery</a></p>', '', content)
            content = re.sub(r'<p><a href="[^"]*photo[^"]*">Photo Gallery</a></p>', '', content)
            # Also handle relative paths
            content = re.sub(r'<p><a [^>]*>Photo Gallery</a></p>', '', content)
            modified = True

        # 5. Remove "Visualizer" link from footer
        if 'Visualizer' in content:
            content = re.sub(r'<p><a [^>]*>Visualizer</a></p>', '', content)
            modified = True

        # 6. Remove "NewTechWood India" text wherever it appears
        if 'NewTechWood India' in content or 'Newtechwood India' in content or 'NewTechwood India' in content:
            content = re.sub(r'<p><a [^>]*>[^<]*NewTechWood India[^<]*</a></p>', '', content, flags=re.IGNORECASE)
            content = re.sub(r'NewTechWood India', '', content, flags=re.IGNORECASE)
            modified = True

        if modified and content != original:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            html_files_updated += 1

print(f"Applied all 4 global changes to {html_files_updated} HTML files.")
