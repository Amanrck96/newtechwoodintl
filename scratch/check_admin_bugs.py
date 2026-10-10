import re
import sys

def check_html_file(filepath):
    print(f"\n==========================================")
    print(f"AUDITING FILE: {filepath}")
    print(f"==========================================")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Collect all HTML IDs
    html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
    print(f"Found {len(html_ids)} unique HTML element IDs.")

    # 2. Extract embedded JS
    js_scripts = re.findall(r'<script(?![^>]*\bsrc\b)[^>]*>([\s\S]*?)<\/script>', html, re.IGNORECASE)
    js_code = "\n".join(js_scripts)
    print(f"Extracted {len(js_scripts)} inline script blocks ({len(js_code)} chars of JS).")

    # 3. Find document.getElementById calls
    get_elem_calls = re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', js_code)
    missing_ids = {}
    for gid in get_elem_calls:
        if gid not in html_ids:
            missing_ids[gid] = missing_ids.get(gid, 0) + 1

    print(f"document.getElementById referenced {len(set(get_elem_calls))} unique IDs.")
    print(f"Missing IDs in DOM (potential null dereferences): {len(missing_ids)}")
    for gid, cnt in sorted(missing_ids.items()):
        print(f"  [MISSING ID] '{gid}' (referenced {cnt} times)")

    # 4. Find all inline handlers: onclick="func(...)", onchange="...", etc.
    handler_calls = re.findall(r'\bon[a-zA-Z]+=["\']([^"\']+)["\']', html)
    func_names = []
    for h in handler_calls:
        # e.g., "switchTab('overview')", "closeModal()", "event.stopPropagation(); deleteOrder(123)"
        matches = re.findall(r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(', h)
        for m in matches:
            if m not in ('alert', 'confirm', 'prompt', 'console', 'log', 'parseInt', 'parseFloat', 'Boolean', 'String', 'Number', 'Date', 'Array', 'Object', 'Math', 'RegExp', 'encodeURIComponent', 'decodeURIComponent', 'event'):
                func_names.append(m)

    # 5. Collect all JS defined functions/variables
    defined_funcs = set(re.findall(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(', js_code))
    defined_funcs.update(re.findall(r'(?:window\.|const\s+|let\s+|var\s+)([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:function|\()', js_code))
    defined_funcs.update(re.findall(r'window\.([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=', js_code))

    print(f"Found {len(defined_funcs)} defined JS functions/top-level assignments.")
    missing_handlers = set()
    for fn in func_names:
        if fn not in defined_funcs:
            missing_handlers.add(fn)

    print(f"Inline event functions missing from JS definitions: {len(missing_handlers)}")
    for mh in sorted(missing_handlers):
        print(f"  [UNDEFINED HANDLER] '{mh}'")

    # 6. Check for syntax/runtime risks like null.property
    # Look for calls like document.getElementById('...').innerHTML or .value or .classList
    unsafe_patterns = re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)\s*\.([a-zA-Z0-9_$]+)', js_code)
    unsafe_on_missing = [p for p in unsafe_patterns if p[0] not in html_ids]
    print(f"Unsafe direct property accesses on MISSING elements: {len(unsafe_on_missing)}")
    for missing_id, prop in unsafe_on_missing:
        print(f"  [CRASH RISK] document.getElementById('{missing_id}').{prop} will throw TypeError: null has no properties!")

    # 7. Check switchTab vs view IDs
    switch_tabs = set(re.findall(r'switchTab\(["\']([^"\']+)["\']\)', html))
    view_ids = set(re.findall(r'id=["\']view-([^"\']+)["\']', html))
    print(f"\nTabs referenced in switchTab: {len(switch_tabs)}")
    print(f"View elements (view-*): {len(view_ids)}")
    missing_views = [t for t in switch_tabs if t not in view_ids]
    if missing_views:
        print(f"  [MISSING VIEW CONTAINERS] {missing_views}")
    else:
        print("  All switchTab targets have corresponding #view-[tab] elements! Validated.")

    # 8. Check all modals and modal openers/closers
    modal_ids = set(re.findall(r'id=["\']([a-zA-Z0-9_\-]*modal[a-zA-Z0-9_\-]*)["\']', html, re.IGNORECASE))
    print(f"\nModal elements found: {len(modal_ids)}")
    for mid in sorted(modal_ids):
        print(f"  - Modal: {mid}")

    # 9. Search for undefined variables, broken template strings, or invalid JS
    # Look for ${something} outside template strings or improper syntax
    # Also inspect all functions called by onclick
    return missing_ids, missing_handlers, unsafe_on_missing

if __name__ == '__main__':
    check_html_file('admin.html')
    check_html_file('admin/vendor.html')
