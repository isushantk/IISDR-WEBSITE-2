import os, re

# The block we want to remove duplicates of
duplicate_regex = r"\s*// Handle mobile dropdown menus\s*const dropdowns = document\.querySelectorAll\('\.nav-dropdown'\);\s*dropdowns\.forEach\(function\(dropdown\) \{\s*const trigger = dropdown\.querySelector\('a'\);\s*if \(trigger\) \{\s*trigger\.addEventListener\('click', function\(e\) \{\s*if \(window\.innerWidth < 768\) \{\s*e\.preventDefault\(\);\s*e\.stopPropagation\(\);\s*// Close other dropdowns\s*dropdowns\.forEach\(function\(other\) \{\s*if \(other !== dropdown\) \{\s*other\.classList\.remove\('active'\);\s*\}\s*\}\);\s*dropdown\.classList\.toggle\('active'\);\s*\}\s*\}\);\s*\}\s*\}\);\s*// Close menu when clicking outside\s*document\.addEventListener\('click', function\(e\) \{\s*if \(window\.innerWidth < 768\) \{\s*if \(navLinks && navLinks\.classList\.contains\('active'\) && !navLinks\.contains\(e\.target\) && !navToggle\.contains\(e\.target\)\) \{\s*navToggle\.setAttribute\('aria-expanded', 'false'\);\s*navToggle\.classList\.remove\('active'\);\s*navLinks\.classList\.remove\('active'\);\s*navSearch\.classList\.remove\('active'\);\s*dropdowns\.forEach\(function\(dropdown\) \{\s*dropdown\.classList\.remove\('active'\);\s*\}\);\s*\}\s*\}\s*\}\);"

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        matches = re.findall(duplicate_regex, content, flags=re.MULTILINE)
        if len(matches) > 1:
            parts = re.split(duplicate_regex, content, flags=re.MULTILINE)
            # Keep only the first occurrence
            new_content = parts[0] + matches[0]
            for part in parts[1:]:
                new_content += part
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {filename}")

