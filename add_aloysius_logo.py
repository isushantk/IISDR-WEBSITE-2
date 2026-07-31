import re

files = ["index.html", "iisdr_website.html"]

aloysius_html = """                <a href="https://staloysius.edu.in/" target="_blank" class="partner-logo-item" title="St. Aloysius University"><img
                        src="images/partners/college-logo.jpg" alt="St. Aloysius University Logo"></a>
"""

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add to the main list of partners
    # Look for St. Agnes and insert before it
    search_str1 = """                <a href="https://www.stagnescollege.edu.in/" target="_blank" class="partner-logo-item" title="St. Agnes College (Autonomous)"><img"""
    
    if search_str1 in content:
        content = content.replace(search_str1, aloysius_html + search_str1)
        
    # There is also a duplicated list for seamless loop in index.html (and maybe iisdr_website.html)
    # The first replacement will do all occurrences, let's just make sure it does it cleanly.
    # Wait, `.replace()` replaces ALL occurrences. So if St. Agnes is there twice, Aloysius will be inserted twice. This is correct for the seamless loop!

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Added St. Aloysius back to {filename}")

