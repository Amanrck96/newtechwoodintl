import sys, os
sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', '.gemini', 'node_modules', '__pycache__', 'venv', '.temp']):
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.py', '.sql')):
            tf = os.path.join(root, f)
            with open(tf, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read().lower()
                cnt = c.count('waltz')
                if cnt > 0:
                    print(f"{tf}: {cnt} occurrences")
