import re

files = ["index.html", "iisdr_website.html"]

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update totalSlides
    content = re.sub(r'const totalSlides = 23;', r'const totalSlides = 22;', content)

    # 2. Remove CSS for slide-0
    # Use re.sub to remove exactly the block
    content = re.sub(r'[ \t]*\.carousel-slide\.slide-0 \{\s*background: url\(\'images/hero/hero-st-agnes-1\.png\'\) no-repeat center center;\s*background-size: cover;\s*\}\s*', '', content)

    # 3. Shift CSS classes down by 1
    # Replace .carousel-slide.slide-X { with .carousel-slide.slide-{X-1} {
    for i in range(1, 23):
        content = re.sub(rf'\.carousel-slide\.slide-{i}\b', f'.carousel-slide.slide-{i-1}', content)

    # 4. Remove HTML for slide-0
    # Looking for: <div class="carousel-slide active slide-0">\n            </div>\n
    content = re.sub(r'[ \t]*<div class="carousel-slide active slide-0">\s*</div>\n', '', content)
    # Also handle if it's just <div class="carousel-slide active slide-0"></div>
    content = re.sub(r'[ \t]*<div class="carousel-slide active slide-0"></div>\n', '', content)

    # 5. Shift HTML classes down by 1
    # For i=1, make it active
    content = re.sub(r'carousel-slide slide-1\b', 'carousel-slide active slide-0', content)
    for i in range(2, 23):
        content = re.sub(rf'carousel-slide slide-{i}\b', f'carousel-slide slide-{i-1}', content)

    # 6. Remove first dot
    content = re.sub(r'[ \t]*<button class="carousel-dot active" onclick="goToSlide\(0\)" aria-label="Go to slide 0"></button>\n', '', content)

    # 7. Shift dots
    # i=1 becomes active dot 0
    content = re.sub(r'class="carousel-dot" onclick="goToSlide\(1\)" aria-label="Go to slide 1"', 'class="carousel-dot active" onclick="goToSlide(0)" aria-label="Go to slide 0"', content)
    for i in range(2, 23):
        content = re.sub(rf'goToSlide\({i}\)', f'goToSlide({i-1})', content)
        content = re.sub(rf'Go to slide {i}\b', f'Go to slide {i-1}', content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filename}")
