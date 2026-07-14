import re
import os

workspace_dir = r"c:\Users\amanr\OneDrive\Documents\newtechwoodintl"

# 1. Update intercomSettings to hide default launcher
settings_pattern = re.compile(
    r'window\.intercomSettings = \{\s*api_base: "https://api-iam\.intercom\.io",\s*app_id: "a174cd76",?\s*};',
    re.DOTALL
)

new_settings = (
    'window.intercomSettings = {\n'
    '    api_base: "https://api-iam.intercom.io",\n'
    '    app_id: "a174cd76",\n'
    '    hide_default_launcher: true\n'
    '  };'
)

# 2. Custom launcher div to inject before </body>
custom_launcher = (
    '\n\t<!-- Custom Floating Intercom Messenger Trigger -->\n'
    '\t<div id="custom-intercom-launcher" style="position:fixed;bottom:24px;right:24px;z-index:9999;cursor:pointer;background:#fff;border-radius:50%;box-shadow:0 4px 12px rgba(0,0,0,0.15);width:60px;height:60px;display:flex;align-items:center;justify-content:center;transition:transform 0.2s ease,box-shadow 0.2s ease;" onclick="if(window.Intercom){Intercom(\'show\');}" onmouseover="this.style.transform=\'scale(1.08)\';this.style.boxShadow=\'0 6px 16px rgba(0,0,0,0.2)\';" onmouseout="this.style.transform=\'scale(1)\';this.style.boxShadow=\'0 4px 12px rgba(0,0,0,0.15)\';">\n'
    '\t  <img src="/wp-content/uploads/lumber-life-logo.png" alt="Lumber Life" style="width:38px;height:38px;object-fit:contain;" />\n'
    '\t</div>\n'
)

html_files_updated = 0

for root, dirs, files in os.walk(workspace_dir):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for file in files:
        if file.lower().endswith('.html'):
            file_path = os.path.join(root, file)
            
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            modified = False
            
            # Hide default launcher
            if 'hide_default_launcher' not in content:
                new_content, count = settings_pattern.subn(new_settings, content)
                if count > 0:
                    content = new_content
                    modified = True
            
            # Inject custom launcher button right before </body>
            if 'id="custom-intercom-launcher"' not in content:
                if '</body>' in content:
                    content = content.replace('</body>', custom_launcher + '</body>', 1)
                    modified = True
                    
            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                html_files_updated += 1

print(f"Configured custom Intercom launcher on {html_files_updated} HTML files.")
