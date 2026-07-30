import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if the duplicated section exists and if college-logo is missing there
    dup_section_marker = '<!-- Duplicated for seamless loop -->'
    if dup_section_marker in content:
        # Check if college-logo is in the content after the dup marker
        post_dup = content.split(dup_section_marker)[1]
        if 'college-logo.jpg' not in post_dup:
            # We need to insert it right after the dup_section_marker
            replacement = '<!-- Duplicated for seamless loop -->\n                <a href="#" target="_blank" class="partner-logo-item" title="College MoU"><img src="images/partners/college-logo.jpg" alt="College MoU Logo"></a>'
            content = content.replace(dup_section_marker, replacement)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {file}")

