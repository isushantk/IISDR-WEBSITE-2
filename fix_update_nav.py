import re

with open('update_navigation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# In update_file inside update_navigation.py, we should strip out old scripts
fix_code = """
    # Strip out any old navigation scripts to prevent duplicates
    content = re.sub(r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{\s*const navToggle.*?\}\);\s*\}\);\s*</script>', '', content, flags=re.DOTALL)
    
    if '<nav' in content:"""

content = content.replace("if '<nav' in content:", fix_code)

with open('update_navigation.py', 'w', encoding='utf-8') as f:
    f.write(content)

