import os, re

duplicate_block = r"""\s*if \(navToggle && navLinks && navSearch\) \{\s*navToggle\.addEventListener\('click', function\(e\) \{\s*e\.stopPropagation\(\);\s*const isExpanded = navToggle\.getAttribute\('aria-expanded'\) === 'true';\s*navToggle\.setAttribute\('aria-expanded', !isExpanded\);\s*navToggle\.classList\.toggle\('active'\);\s*navLinks\.classList\.toggle\('active'\);\s*navSearch\.classList\.toggle\('active'\);\s*\}\);\s*\}"""

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check how many times the block appears
        matches = re.findall(duplicate_block, content, flags=re.MULTILINE)
        if len(matches) > 1:
            # We want to remove the SECOND occurrence (which is usually the one without the new dropdown code, or just keep the first)
            # Actually, let's just keep the first one and remove all subsequent ones
            
            parts = re.split(duplicate_block, content, flags=re.MULTILINE)
            # parts[0] + match + parts[1] + match + parts[2] ...
            # We will reconstruct it keeping only the first match
            new_content = parts[0] + matches[0]
            for part in parts[1:]:
                new_content += part
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {filename}")

