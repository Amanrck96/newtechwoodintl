import re

with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all inline event handlers
events = re.findall(r'\bon([a-z]+)=["\']([^"\']+)["\']', html, re.IGNORECASE)
print(f"Total inline event bindings: {len(events)}")

# Collect all JS functions defined in script blocks
js_scripts = re.findall(r'<script(?![^>]*\bsrc\b)[^>]*>([\s\S]*?)<\/script>', html, re.IGNORECASE)
js_all = "\n".join(js_scripts)

# Match function declarations and window.func assignments
defined_funcs = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', js_all))
defined_funcs.update(re.findall(r'(?:window\.|const\s+|let\s+|var\s+)([a-zA-Z0-9_$]+)\s*=\s*(?:function|\()', js_all))
defined_funcs.update(re.findall(r'window\.([a-zA-Z0-9_$]+)\s*=', js_all))

builtins = {'alert', 'confirm', 'prompt', 'print', 'focus', 'blur', 'close', 'open', 'scroll', 'scrollTo', 'setTimeout', 'clearTimeout', 'setInterval', 'clearInterval', 'event', 'console', 'this', 'parent', 'top', 'location', 'history'}

missing = set()
for ev_name, ev_code in events:
    # extract function calls like `doSomething(1, 'abc')`
    calls = re.findall(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(', ev_code)
    for c in calls:
        if c not in defined_funcs and c not in builtins:
            # check if it's JS keyword like if/return
            if c not in {'if', 'for', 'while', 'switch', 'return', 'typeof', 'void'}:
                missing.add((c, ev_code))

if missing:
    print(f"MISSING HANDLER FUNCTIONS ({len(missing)}):")
    for fn, code in sorted(missing):
        print(f"  - Function '{fn}' called in `{code}`")
else:
    print("ALL inline event handler functions are properly defined in JavaScript! 100% verified.")
