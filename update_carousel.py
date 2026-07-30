import re

with open('iisdr_website.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update totalSlides
content = re.sub(r'const totalSlides = 21;', r'const totalSlides = 23;', content)

# 2. Add CSS for new slides and shift old ones
# First shift all existing slide CSS classes
for i in range(20, -1, -1):
    content = content.replace(f'.carousel-slide.slide-{i} {{', f'.carousel-slide.slide-{i+2} {{')

# Now insert slide-0 and slide-1 CSS just before slide-2
new_css = """        .carousel-slide.slide-0 {
            background: url('images/hero/hero-st-agnes-1.png') no-repeat center center;
            background-size: cover;
        }

        .carousel-slide.slide-1 {
            background: url('images/hero/hero-st-agnes-2.png') no-repeat center center;
            background-size: cover;
        }

"""
content = content.replace('.carousel-slide.slide-2 {', new_css + '.carousel-slide.slide-2 {')

# 3. Add HTML slides and shift old ones
for i in range(20, -1, -1):
    # Need to handle 'active slide-0' carefully
    if i == 0:
        content = content.replace('carousel-slide active slide-0', 'carousel-slide slide-2')
        content = content.replace('carousel-slide slide-0', 'carousel-slide slide-2')
    else:
        content = content.replace(f'carousel-slide slide-{i}', f'carousel-slide slide-{i+2}')

# Insert slide-0 and slide-1
new_html_slides = """            <div class="carousel-slide active slide-0">
            </div>
            <div class="carousel-slide slide-1">
            </div>
"""
content = content.replace('<div class="carousel-slide slide-2">', new_html_slides + '            <div class="carousel-slide slide-2">', 1)

# 4. Add dots and shift old ones
# Shift dots starting from 20 down to 0
for i in range(20, -1, -1):
    if i == 0:
        content = content.replace('goToSlide(0)', 'goToSlide(2)')
        content = content.replace('aria-label="Go to slide 0"', 'aria-label="Go to slide 2"')
        # Also remove active class from the first dot, as the new first dot will be active
        content = content.replace('class="carousel-dot active"', 'class="carousel-dot"')
    else:
        content = content.replace(f'goToSlide({i})', f'goToSlide({i+2})')
        content = content.replace(f'aria-label="Go to slide {i}"', f'aria-label="Go to slide {i+2}"')

# Insert new dots
new_dots = """            <button class="carousel-dot active" onclick="goToSlide(0)" aria-label="Go to slide 0"></button>
            <button class="carousel-dot" onclick="goToSlide(1)" aria-label="Go to slide 1"></button>
"""
content = content.replace('<button class="carousel-dot" onclick="goToSlide(2)"', new_dots + '            <button class="carousel-dot" onclick="goToSlide(2)"', 1)


with open('iisdr_website.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("iisdr_website.html updated successfully!")
