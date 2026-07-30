import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

broken_images = []

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check img tags
    img_matches = re.findall(r'<img[^>]+src=["\'](.*?)["\']', content)
    for src in img_matches:
        if src.startswith('http') or src.startswith('data:'):
            continue
        if not os.path.exists(src):
            broken_images.append((file, src))

    # Check url() in CSS
    url_matches = re.findall(r'url\([\'"]?(.*?)[\'"]?\)', content)
    for url in url_matches:
        if url.startswith('http') or url.startswith('data:'):
            continue
        if not os.path.exists(url):
            broken_images.append((file, url))

if broken_images:
    print("Broken images found:")
    for file, src in set(broken_images):
        print(f"File: {file} -> Image: {src}")
else:
    print("All image references are valid locally.")
