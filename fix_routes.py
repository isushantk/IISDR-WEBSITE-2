import glob

for file in glob.glob("*.html"):
    with open(file, "r") as f:
        content = f.read()
    
    # We want to keep the E-Journal Contact Us but also add General Contact Us, OR just update the general one.
    # Let's add the E-journal one and update the general one.
    # But wait, the current line is:
    # { keywords: ['contact', 'email', 'address'], page: 'Contact Us', url: 'iisdr_ejournal_contact_us.html' },
    # We can replace it with:
    # { keywords: ['contact', 'email', 'address'], page: 'Contact Us', url: 'iisdr_contact_us.html' },
    # { keywords: ['thrive', 'journal contact'], page: 'E-Journal Contact Us', url: 'iisdr_ejournal_contact_us.html' },
    
    old_line = "url: 'iisdr_ejournal_contact_us.html' },"
    new_lines = "url: 'iisdr_contact_us.html' },\n                    { keywords: ['thrive', 'journal contact'], page: 'E-Journal Contact Us', url: 'iisdr_ejournal_contact_us.html' },"
    
    if old_line in content:
        content = content.replace(old_line, new_lines)
        with open(file, "w") as f:
            f.write(content)
        print(f"Updated {file}")
