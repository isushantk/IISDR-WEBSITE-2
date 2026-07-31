import re

files = ["index.html", "iisdr_website.html"]

logo1_html = """                <a href="#" target="_blank" class="partner-logo-item" title="MoU Partner"><img
                        src="images/partners/logo1.png" alt="MoU Partner Logo"></a>
"""

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for where to insert it. We'll insert it right after the start of the carousel tracks.
    # We want it to be before logo1_mou.png
    search_str1 = """                <a href="#" target="_blank" class="partner-logo-item" title="MoU Partner"><img
                        src="images/partners/logo1_mou.png" alt="MoU Partner Logo"></a>"""
    
    if search_str1 in content:
        content = content.replace(search_str1, logo1_html + search_str1)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Added logo1.png back to {filename}")

