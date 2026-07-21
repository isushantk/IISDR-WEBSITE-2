import os
import re

# ============================================
# STANDARD NAVBAR HTML TEMPLATE
# ============================================
NAVBAR_TEMPLATE = """    <nav class="nav-bar" role="navigation" aria-label="Main navigation">
        <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
            <span></span>
            <span></span>
            <span></span>
        </button>
        <ul class="nav-links">
            <li><a href="index.html" class="nav-link-home">Home</a></li>
            <li><a href="iisdr_about_us.html" class="nav-link-about">About Us</a></li>
            <li><a href="iisdr_programs.html" class="nav-link-programs">Programs</a></li>
            <li class="nav-dropdown">
                <a href="#" class="nav-link-mou">MoU Partner</a>
                <div class="dropdown-menu">
                    <a href="https://inclusiv.in/" target="_blank">Inclusiv</a>
                    <a href="https://www.sswroshni.in/eng/" target="_blank">School of Social Work, Roshni Nilaya (SSW)</a>
                    <a href="https://sdmcbm.ac.in/" target="_blank">SDM College of Business Management PG Centre</a>
                    <a href="https://www.hsscindia.in/index.html" target="_blank">Hydrocarbon Sector Skill Council (HSCC India)</a>
                    <a href="https://www.fathermuller.edu.in/allied-health-sciences/department-of-hospital-administration.php" target="_blank">Father Muller College of Allied Health Sciences</a>
                    <a href="https://msnim.edu.in/" target="_blank">Manel Srinivas Nayak Institute of Management (MSNIM)</a>
                    <a href="https://sjec.ac.in/" target="_blank">St Joseph Engineering College (SJEC)</a>
                    <a href="https://staloysius.edu.in/" target="_blank">St. Aloysius University</a>
                </div>
            </li>
            <li><a href="iisdr_information_bulletins.html" class="nav-link-bulletins">Information Bulletins</a></li>
            <li class="nav-dropdown">
                <a href="#" class="nav-link-ejournal">E-Journal</a>
                <div class="dropdown-menu">
                    <a href="iisdr_ejournal_about_thrive.html">About THRIVE</a>
                    <a href="iisdr_journal_particulars.html">Journal Particulars</a>
                    <a href="iisdr_editorial_board.html">Editorial Board</a>
                    <a href="iisdr_author_guidelines.html">Author Guidelines</a>
                    <a href="iisdr_ejournal.html">E-Journal</a>
                    <a href="iisdr_disclaimer.html">Disclaimer</a>
                    <a href="iisdr_call_for_papers.html">Call for Papers</a>
                    <a href="iisdr_ejournal_contact_us.html">Contact Us</a>
                </div>
            </li>
            <li><a href="iisdr_certification.html" class="nav-link-certification">Certification Programs</a></li>
            <li><a href="iisdr_ejournal_contact_us.html" class="nav-link-contact">Contact Us</a></li>
        </ul>
        <div class="nav-search">
            <input type="text" placeholder="Search IISDR..." aria-label="Search website">
            <button aria-label="Submit search">🔍</button>
        </div>
    </nav>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const navToggle = document.querySelector('.nav-toggle');
            const navLinks = document.querySelector('.nav-links');
            const navSearch = document.querySelector('.nav-search');
            
            if (navToggle && navLinks && navSearch) {
                navToggle.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
                    navToggle.setAttribute('aria-expanded', !isExpanded);
                    navToggle.classList.toggle('active');
                    navLinks.classList.toggle('active');
                    navSearch.classList.toggle('active');
                });
            }
            
            // Handle mobile dropdown menus
            const dropdowns = document.querySelectorAll('.nav-dropdown');
            dropdowns.forEach(function(dropdown) {
                const trigger = dropdown.querySelector('a');
                if (trigger) {
                    trigger.addEventListener('click', function(e) {
                        if (window.innerWidth < 768) {
                            e.preventDefault();
                            e.stopPropagation();
                            
                            // Close other dropdowns
                            dropdowns.forEach(function(other) {
                                if (other !== dropdown) {
                                    other.classList.remove('active');
                                }
                            });
                            
                            dropdown.classList.toggle('active');
                        }
                    });
                }
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', function(e) {
                if (window.innerWidth < 768) {
                    if (navLinks && navLinks.classList.contains('active') && !navLinks.contains(e.target) && !navToggle.contains(e.target)) {
                        navToggle.setAttribute('aria-expanded', 'false');
                        navToggle.classList.remove('active');
                        navLinks.classList.remove('active');
                        navSearch.classList.remove('active');
                        dropdowns.forEach(function(dropdown) {
                            dropdown.classList.remove('active');
                        });
                    }
                }
            });
        });
    </script>"""

# ============================================
# STANDARD NAVBAR CSS BLOCK
# ============================================
NAVBAR_CSS = """
        /* ============================================
           MAIN NAVIGATION BAR (STANDARD & RESPONSIVE)
           ============================================ */
        .nav-bar {
            background-color: #003d99 !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            padding: 0 20px !important;
            border-bottom: 3px solid #ff9933 !important;
            width: 100% !important;
            position: relative !important;
            z-index: 1000 !important;
            box-sizing: border-box !important;
        }

        /* Hamburger Toggle Button */
        .nav-toggle {
            display: none !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            width: 30px !important;
            height: 20px !important;
            background: transparent !important;
            border: none !important;
            cursor: pointer !important;
            padding: 0 !important;
            z-index: 1001 !important;
            margin: 15px 0 !important;
        }

        .nav-toggle span {
            display: block !important;
            height: 3px !important;
            width: 100% !important;
            background-color: #ffffff !important;
            border-radius: 3px !important;
            transition: all 0.3s ease !important;
            transform-origin: left center !important;
        }

        /* Hamburger Animation */
        .nav-toggle.active span:nth-child(1) {
            transform: rotate(45deg) !important;
            position: relative !important;
            top: -2px !important;
            left: 2px !important;
        }

        .nav-toggle.active span:nth-child(2) {
            width: 0% !important;
            opacity: 0 !important;
        }

        .nav-toggle.active span:nth-child(3) {
            transform: rotate(-45deg) !important;
            position: relative !important;
            top: 2px !important;
            left: 2px !important;
        }

        .nav-links {
            display: flex !important;
            list-style: none !important;
            margin: 0 !important;
            padding: 0 !important;
            flex: 1 !important;
        }

        .nav-links li {
            border-right: 1px solid #002d77 !important;
            position: relative !important;
        }

        .nav-links li:last-child {
            border-right: none !important;
        }

        .nav-links a {
            display: block !important;
            padding: 15px 18px !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            text-decoration: none !important;
            border-bottom: 3px solid transparent !important;
            transition: all 0.3s ease !important;
        }

        .nav-links a:hover,
        .nav-links a.active {
            background-color: #002d77 !important;
            color: #ff9933 !important;
            border-bottom-color: #ff9933 !important;
            text-decoration: none !important;
        }

        /* Dropdown Styles */
        .nav-dropdown {
            position: relative !important;
        }

        .nav-dropdown > a {
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }

        .nav-dropdown > a::after {
            content: "▼" !important;
            font-size: 0.7rem !important;
            margin-left: 4px !important;
        }

        .dropdown-menu {
            display: none !important;
            position: absolute !important;
            top: 100% !important;
            left: 0 !important;
            background-color: #ffffff !important;
            min-width: 250px !important;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
            z-index: 1000 !important;
            border: 1px solid #cccccc !important;
            padding: 0 !important;
        }

        .dropdown-menu a {
            display: block !important;
            padding: 12px 18px !important;
            color: #003d99 !important;
            text-decoration: none !important;
            border-bottom: 1px solid #e8e8e8 !important;
            transition: all 0.3s ease !important;
            font-weight: normal !important;
            font-size: 0.9rem !important;
            text-align: left !important;
        }

        .dropdown-menu a:hover {
            background-color: #f5f5f5 !important;
            color: #ff9933 !important;
            padding-left: 22px !important;
        }

        /* Show dropdown on hover (desktop only) */
        @media (min-width: 768px) {
            .nav-dropdown:hover .dropdown-menu {
                display: block !important;
            }
        }

        .nav-search {
            padding: 12px 15px !important;
            display: flex !important;
            gap: 8px !important;
            align-items: center !important;
            border-left: 1px solid #002d77 !important;
        }

        .nav-search input {
            padding: 6px 10px !important;
            border: 1px solid #cccccc !important;
            border-radius: 2px !important;
            font-size: 0.9rem !important;
            width: 180px !important;
        }

        .nav-search button {
            background-color: #ff9933 !important;
            color: #ffffff !important;
            border: 1px solid #ff9933 !important;
            padding: 6px 12px !important;
            font-weight: bold !important;
            font-size: 0.85rem !important;
            cursor: pointer !important;
        }

        .nav-search button:hover {
            background-color: #e68a1f !important;
        }

        /* ============================================
           MOBILE RESPONSIVE STYLES (< 768px)
           ============================================ */
        @media (max-width: 767px) {
            .nav-bar {
                flex-wrap: wrap !important;
                padding: 10px 15px !important;
            }

            .nav-toggle {
                display: flex !important;
            }

            .nav-links {
                display: none !important;
                flex-direction: column !important;
                width: 100% !important;
                order: 2 !important;
                margin-top: 10px !important;
                border-top: 1px solid #002d77 !important;
            }

            .nav-links.active {
                display: flex !important;
            }

            .nav-links li {
                border-right: none !important;
                border-bottom: 1px solid #002d77 !important;
                width: 100% !important;
            }

            .nav-links li:last-child {
                border-bottom: none !important;
            }

            .nav-links a {
                padding: 12px 10px !important;
                width: 100% !important;
                box-sizing: border-box !important;
            }

            .nav-links a:hover,
            .nav-links a.active {
                border-bottom-color: transparent !important;
                background-color: #002d77 !important;
            }

            /* Dropdown behavior on mobile */
            .dropdown-menu {
                position: static !important;
                width: 100% !important;
                box-shadow: none !important;
                border: none !important;
                background-color: #002d77 !important;
                box-sizing: border-box !important;
            }

            .nav-dropdown.active .dropdown-menu {
                display: block !important;
            }

            .dropdown-menu a {
                color: #ffffff !important;
                padding: 10px 20px 10px 30px !important;
                border-bottom: 1px solid #001a44 !important;
            }

            .dropdown-menu a:hover {
                background-color: #001a44 !important;
                padding-left: 35px !important;
            }

            .nav-search {
                display: none !important;
                width: 100% !important;
                order: 3 !important;
                border-left: none !important;
                border-top: 1px solid #002d77 !important;
                padding: 15px 0 5px 0 !important;
                box-sizing: border-box !important;
            }

            .nav-search.active {
                display: flex !important;
            }

            .nav-search input {
                flex: 1 !important;
                width: auto !important;
            }
        }
"""

def get_active_class(filename):
    if filename == 'index.html': return 'nav-link-home'
    if filename == 'iisdr_about_us.html': return 'nav-link-about'
    if filename == 'iisdr_programs.html': return 'nav-link-programs'
    if filename == 'iisdr_information_bulletins.html': return 'nav-link-bulletins'
    if filename == 'iisdr_certification.html': return 'nav-link-certification'
    if filename == 'iisdr_ejournal_contact_us.html': return 'nav-link-contact'
    # Dropdown children
    if filename in ['iisdr_ejournal_about_thrive.html', 'iisdr_journal_particulars.html', 
                  'iisdr_editorial_board.html', 'iisdr_author_guidelines.html', 
                  'iisdr_ejournal.html', 'iisdr_disclaimer.html', 'iisdr_call_for_papers.html']:
        return 'nav-link-ejournal'
    return None

def clean_navbar_css(css_text):
    # We want to remove all css rules that target navbar classes.
    navbar_selectors = [
        '.nav-bar', '.nav-links', '.dropdown-menu', '.nav-dropdown',
        '.nav-search', '.nav-toggle', '.nav-mobile-toggle', '.nav-link'
    ]
    
    # 1. Strip the custom marker block if it already exists
    css_text = re.sub(r'/\* === NAVBAR STYLES START === \*/.*?/\* === NAVBAR STYLES END === \*/', '', css_text, flags=re.DOTALL)
    
    # 2. Parse character by character to safely handle nested braces (media queries)
    i = 0
    n = len(css_text)
    output = []
    
    while i < n:
        # Check for comment
        if css_text[i:i+2] == '/*':
            comment_end = css_text.find('*/', i+2)
            if comment_end == -1:
                output.append(css_text[i:])
                break
            comment = css_text[i:comment_end+2]
            # Skip comments relating to navbar
            if any(x in comment.lower() for x in ['navigation bar', 'dropdown menu', 'navbar styles']):
                pass
            else:
                output.append(comment)
            i = comment_end + 2
            continue
        
        # Whitespace / formatting
        if css_text[i].isspace():
            output.append(css_text[i])
            i += 1
            continue
            
        # Selectors / rules
        brace_start = css_text.find('{', i)
        if brace_start == -1:
            output.append(css_text[i:])
            break
            
        selector = css_text[i:brace_start].strip()
        
        # Find matching closing brace
        brace_depth = 0
        j = brace_start
        while j < n:
            if css_text[j] == '{':
                brace_depth += 1
            elif css_text[j] == '}':
                brace_depth -= 1
                if brace_depth == 0:
                    break
            j += 1
            
        if j >= n:
            output.append(css_text[i:])
            break
            
        block_content = css_text[brace_start:j+1]
        
        # Determine if we should remove this rule
        should_remove = False
        if any(cls in selector for cls in navbar_selectors):
            should_remove = True
            
        # Recursive cleaning inside media queries
        if selector.startswith('@media'):
            inner_rules = block_content[1:-1]
            cleaned_inner = clean_navbar_css(inner_rules)
            if cleaned_inner.strip() == '':
                should_remove = True
            else:
                block_content = '{' + cleaned_inner + '}'
                
        if not should_remove:
            output.append(selector + ' ' + block_content)
            
        i = j + 1
        
    return ''.join(output)

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update HTML
    active_link_class = get_active_class(filename)
    current_nav = NAVBAR_TEMPLATE
    if active_link_class:
        current_nav = current_nav.replace(f'class="{active_link_class}"', f'class="{active_link_class} active"')

    # Aggressive HTML replacement
    
    # Strip out any old navigation scripts to prevent duplicates
    content = re.sub(r'<script>\s*document\.addEventListener\('DOMContentLoaded', function\(\) \{\s*const navToggle.*?\}\);\s*\}\);\s*</script>', '', content, flags=re.DOTALL)
    
    if '<nav' in content:
        content = re.sub(r'<nav.*?>.*?</nav>', current_nav, content, flags=re.DOTALL)
    else:
        # Injection fallback
        if '</header>' in content:
            content = content.replace('</header>', '</header>\n\n' + current_nav)
        elif '<!-- Announcements' in content:
            content = content.replace('<!-- Announcements', current_nav + '\n\n    <!-- Announcements')

    # 2. CSS replacement/injection
    style_start = content.find('<style>')
    style_end = content.find('</style>')
    if style_start != -1 and style_end != -1:
        style_content = content[style_start+7:style_end]
        cleaned_style = clean_navbar_css(style_content)
        new_style_block = cleaned_style.rstrip() + "\n\n        /* === NAVBAR STYLES START === */\n" + NAVBAR_CSS.strip() + "\n        /* === NAVBAR STYLES END === */\n    "
        content = content[:style_start+7] + new_style_block + content[style_end:]
    else:
        new_style_tag = "    <style>\n        /* === NAVBAR STYLES START === */\n" + NAVBAR_CSS.strip() + "\n        /* === NAVBAR STYLES END === */\n    </style>\n</head>"
        content = content.replace('</head>', new_style_tag)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filename}")

# Run on all HTML files in current directory
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        update_file(filename)
