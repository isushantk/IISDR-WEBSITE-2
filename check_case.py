import os
import re

def get_actual_filename(path):
    dir_name = os.path.dirname(path)
    base_name = os.path.basename(path)
    if not dir_name:
        dir_name = '.'
    try:
        files = os.listdir(dir_name)
    except FileNotFoundError:
        return None
    for f in files:
        if f.lower() == base_name.lower():
            if f != base_name:
                return f
    return None

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

mismatches = []

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check img tags
    img_matches = re.findall(r'<img[^>]+src=["\'](.*?)["\']', content)
    # Check url() in CSS
    url_matches = re.findall(r'url\([\'"]?(.*?)[\'"]?\)', content)
    
    for src in img_matches + url_matches:
        if src.startswith('http') or src.startswith('data:') or src.startswith('#'):
            continue
        actual = get_actual_filename(src)
        if actual:
            mismatches.append((file, src, actual))

if mismatches:
    print("Case mismatches found:")
    for file, src, actual in set(mismatches):
        print(f"File: {file} -> src: {src} -> Actual: {actual}")
else:
    print("No case mismatches found.")
