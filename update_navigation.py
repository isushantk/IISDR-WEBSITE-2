import os
import re

# ============================================
# STANDARD NAVBAR HTML TEMPLATE
# ============================================
NAVBAR_TEMPLATE = """    <nav class="nav-bar" role="navigation" aria-label="Main navigation">
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
    </nav>"""

# ============================================
# STANDARD NAVBAR CSS BLOCK
# ============================================
NAVBAR_CSS = """
        /* ============================================
           MAIN NAVIGATION BAR (STANDARD)
           ============================================ */
        .nav-bar {
            background-color: #003d99 !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            padding: 0 !important;
            border-bottom: 3px solid #ff9933 !important;
            width: 100% !important;
            position: relative !important;
            z-index: 1000 !important;
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

        .nav-dropdown:hover .dropdown-menu {
            display: block !important;
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

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update HTML
    active_link_class = get_active_class(filename)
    current_nav = NAVBAR_TEMPLATE
    if active_link_class:
        current_nav = current_nav.replace(f'class="{active_link_class}"', f'class="{active_link_class} active"')

    # Aggressive HTML replacement
    if '<nav' in content:
        content = re.sub(r'<nav.*?>.*?</nav>', current_nav, content, flags=re.DOTALL)
    else:
        # Injection fallback
        if '</header>' in content:
            content = content.replace('</header>', '</header>\n\n' + current_nav)
        elif '<!-- Announcements' in content:
            content = content.replace('<!-- Announcements', current_nav + '\n\n    <!-- Announcements')

    # 2. Aggressive CSS replacement/injection
    # Remove existing navbar/nav-bar CSS blocks if possible
    content = re.sub(r'/\* =+.*?MAIN NAVIGATION BAR.*?=+/.*?\.nav-bar \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* =+.*?DROPDOWN MENU STYLES.*?=+/.*?\.dropdown-menu \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.nav-bar \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.nav-links \{.*?\}', '', content, flags=re.DOTALL)
    
    # Inject new CSS at the end of the <style> block
    if '</style>' in content:
        content = content.replace('</style>', NAVBAR_CSS + '\n    </style>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filename}")

# Run on all HTML files
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        update_file(filename)
