import glob

# The string to search for
target_string = '                    <a href="https://staloysius.edu.in/" target="_blank">St. Aloysius University</a>'
# The replacement string which includes the target string followed by the new St. Agnes string
replacement_string = '                    <a href="https://staloysius.edu.in/" target="_blank">St. Aloysius University</a>\n                    <a href="https://www.stagnescollege.edu.in/" target="_blank">St. Agnes College (Autonomous)</a>'

html_files = glob.glob('*.html')

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if target_string in content:
        content = content.replace(target_string, replacement_string)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {file_path}")

