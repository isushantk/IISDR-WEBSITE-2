import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

target_poster_html = """                <div class="carousel-slides">
                    <div class="carousel-slide" style="background-color: #f8f9fa;">
                        <img src="images/poster-st-agnes-mou.jpeg" alt="Poster St Agnes MoU"
                            style="width: 100%; height: 100%; object-fit: fill;">
                    </div>"""

search_pattern = r'<div class="carousel-slides">\s*<div class="carousel-slide" style="background-color: #f8f9fa;">\s*<img src="images/poster-whatsapp-2026-07-16.jpeg"'

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'images/poster-st-agnes-mou.jpeg' not in content:
        if re.search(search_pattern, content):
            # We replace the starting div with the div + new poster + old poster
            new_content = re.sub(
                r'<div class="carousel-slides">\s*<div class="carousel-slide" style="background-color: #f8f9fa;">\s*<img src="images/poster-whatsapp-2026-07-16.jpeg"',
                target_poster_html + '\n                    <div class="carousel-slide" style="background-color: #f8f9fa;">\n                        <img src="images/poster-whatsapp-2026-07-16.jpeg"',
                content
            )
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added poster to {file}")
