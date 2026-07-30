import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'(<div class="carousel-container">.*?)(<button class="carousel-arrow prev")', content, re.DOTALL)
    if match:
        container_content = match.group(1)
        
        counter = [0]
        def slide_replacer(m):
            old_class = m.group(1)
            if 'active' in old_class:
                new_class = f'carousel-slide active slide-{counter[0]}'
            else:
                new_class = f'carousel-slide slide-{counter[0]}'
            
            counter[0] += 1
            return f'class="{new_class}"'

        new_container = re.sub(r'class="(carousel-slide[^"]+slide-\d+)"', slide_replacer, container_content)
        
        content = content.replace(container_content, new_container)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {file}")

