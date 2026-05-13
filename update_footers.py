import os
import re

# Modern CSS for the footer
MODERN_CSS = """        /* ============================================
           MODERN FOOTER STYLES
           ============================================ */
        .footer {
            background-color: #00215e;
            color: #ffffff;
            padding: 80px 20px 40px;
            margin-top: 0;
            font-family: Arial, sans-serif;
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
            max-width: 1400px;
            margin: 0 auto 60px;
        }

        .footer-section h3 {
            color: #ff9933;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 25px;
            position: relative;
            padding-bottom: 10px;
        }

        .footer-section h3::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            width: 40px;
            height: 3px;
            background-color: #ff9933;
            border-radius: 2px;
        }

        .footer-section ul {
            list-style: none;
            padding: 0;
        }

        .footer-section li {
            margin-bottom: 12px;
        }

        .footer-section a {
            color: #e0e0e0;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-block;
            font-size: 0.95rem;
        }

        .footer-section a:hover {
            color: #ff9933;
            transform: translateX(5px);
            text-decoration: none;
        }

        .footer-contact-item {
            display: flex;
            gap: 12px;
            margin-bottom: 18px;
            color: #e0e0e0;
            line-height: 1.6;
            font-size: 0.95rem;
        }

        .footer-contact-icon {
            color: #ff9933;
            font-weight: bold;
        }

        .footer-bottom {
            max-width: 1400px;
            margin: 0 auto;
            padding-top: 40px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            color: #b0b0b0;
            font-size: 0.9rem;
        }

        .footer-bottom-info {
            display: flex;
            gap: 30px;
            align-items: center;
            flex-wrap: wrap;
        }

        .footer-bottom-info span {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .visitor-badge {
            background: rgba(255, 153, 51, 0.15);
            color: #ff9933;
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid rgba(255, 153, 51, 0.3);
            font-weight: 600;
        }"""

# Standardized modern footer HTML
NEW_FOOTER = """    <footer class="footer">
        <div class="footer-content">
            <!-- Section 1: Contact Information -->
            <div class="footer-section">
                <h3>Contact Us</h3>
                <div class="footer-contact-item">
                    <span class="footer-contact-icon">📍</span>
                    <span>IISDR Mangalore</span>
                </div>
                <div class="footer-contact-item">
                    <span class="footer-contact-icon">📞</span>
                    <span><a href="tel:+917259215554">+91 7259215554</a></span>
                </div>
                <div class="footer-contact-item">
                    <span class="footer-contact-icon">✉️</span>
                    <span><a href="mailto:ddiisdr@gmail.com">ddiisdr@gmail.com</a></span>
                </div>
            </div>

            <!-- Section 2: Quick Navigation -->
            <div class="footer-section">
                <h3>Quick Navigation</h3>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="iisdr_about_us.html">About Us</a></li>
                    <li><a href="iisdr_programs.html">Programs</a></li>
                    <li><a href="iisdr_activities.html">Activities</a></li>
                    <li><a href="iisdr_certification.html">Certification</a></li>
                    <li><a href="iisdr_ejournal.html">E-Journal</a></li>
                </ul>
            </div>

            <!-- Section 3: Important Links -->
            <div class="footer-section">
                <h3>Important Links</h3>
                <ul>
                    <li><a href="iisdr_disclaimer.html">Privacy Policy</a></li>
                    <li><a href="iisdr_disclaimer.html">Terms of Use</a></li>
                    <li><a href="iisdr_disclaimer.html">Copyright Policy</a></li>
                    <li><a href="iisdr_disclaimer.html">Disclaimer</a></li>
                    <li><a href="iisdr_ejournal_contact_us.html">Grievance Redressal</a></li>
                    <li><a href="iisdr_information_bulletins.html">Right to Information (RTI)</a></li>
                </ul>
            </div>

            <!-- Section 4: Support & Policies -->
            <div class="footer-section">
                <h3>Support & Policies</h3>
                <ul>
                    <li><a href="index.html#website-policies">Website Policies</a></li>
                    <li><a href="index.html#help">Help & FAQs</a></li>
                    <li><a href="index.html#accessibility">Accessibility Statement</a></li>
                    <li><a href="index.html#sitemap">Sitemap</a></li>
                    <li><a href="index.html#feedback">Send Feedback</a></li>
                    <li><a href="index.html#report-issue">Report an Issue</a></li>
                </ul>
            </div>
        </div>

        <!-- Footer Bottom -->
        <div class="footer-bottom">
            <div>© 2026 IISDR. All rights reserved.</div>
            <div class="footer-bottom-info">
                <span>Designed by <strong>Utkarsh Engineers</strong></span>
                <span>Last Updated: <span style="color: #e0e0e0;">25 April 2026</span></span>
                <span>Visitor Count: <span id="visitor-counter" class="visitor-badge">0</span></span>
            </div>
        </div>
    </footer>"""

# Visitor counter init script
VISITOR_INIT = """        // ============================================
        // VISITOR COUNTER (Dynamic Simulation)
        // ============================================
        function initializeVisitorCounter() {
            const COUNTER_KEY = 'iisdr_final_visitor_count'; 
            const START_COUNT = 0;
            let visitorCount = localStorage.getItem(COUNTER_KEY);
            if (visitorCount === null) {
                visitorCount = START_COUNT;
            } else {
                visitorCount = parseInt(visitorCount) + 1;
            }
            function updateDisplay(count) {
                const el = document.getElementById('visitor-counter');
                if (el) {
                    el.textContent = count.toLocaleString('en-IN');
                }
                localStorage.setItem(COUNTER_KEY, count);
            }
            updateDisplay(visitorCount);
            setInterval(() => {
                visitorCount++;
                updateDisplay(visitorCount);
            }, Math.floor(Math.random() * (60000 - 30000 + 1)) + 30000);
        }
        window.addEventListener('load', initializeVisitorCounter);"""

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace Footer HTML
    # Match both <footer...>...</footer> and <div class="footer">...</div> (crude but usually works for these files)
    if '<footer>' in content or '<footer ' in content:
        content = re.sub(r'<footer.*?>.*?</footer>', NEW_FOOTER, content, flags=re.DOTALL)
    elif '<div class="footer">' in content:
        # For div-based footers, we assume it's a block near the end
        content = re.sub(r'<div class="footer">.*?</div>\s*</div>', NEW_FOOTER, content, flags=re.DOTALL)
        # If that didn't work (due to nested divs), try a simpler one
        if NEW_FOOTER not in content:
             content = re.sub(r'<div class="footer">.*?</div>\s*<script', NEW_FOOTER + '\n    <script', content, flags=re.DOTALL)
    
    # Fallback: if still no footer but we have a bottom-footer-like structure
    if NEW_FOOTER not in content and '© 2026 IISDR' in content:
         # Try to find the block containing the copyright
         content = re.sub(r'<div class="footer-bottom">.*?</div>', NEW_FOOTER, content, flags=re.DOTALL)


    # 2. Update/Inject CSS
    if '</style>' in content:
        # Check if footer styles already exist to prevent duplicates
        if '.footer {' in content:
            # Replace existing footer styles (crude but usually works if they are together)
            # We look for .footer { and try to find a reasonable end point or just append at end of style
            # For safety, we'll just remove anything between .footer { and the next major block
            # But wait, it's safer to just append the MODERN_CSS at the end of the style block 
            # and let it override if the previous styles are still there.
            content = content.replace('</style>', MODERN_CSS + '\n    </style>')
        else:
            content = content.replace('</style>', MODERN_CSS + '\n    </style>')
    else:
        # Inject style block before </head>
        content = content.replace('</head>', '    <style>\n' + MODERN_CSS + '\n    </style>\n</head>')
    
    # 3. Clean and Inject Visitor Script
    # Remove existing visitor counter script if it exists
    content = re.sub(r'<script.*?>.*?initializeVisitorCounter.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'window\.addEventListener\(\'load\', initializeVisitorCounter\);', '', content)
    
    if '</body>' in content:
        # Check if there is already a script block to append to
        script_match = re.search(r'<script.*?>', content)
        if script_match:
            # Find the last </script> tag
            last_script_end = content.rfind('</script>')
            if last_script_end != -1:
                 content = content[:last_script_end] + VISITOR_INIT + '\n' + content[last_script_end:]
            else:
                 content = content.replace('</body>', '    <script>\n' + VISITOR_INIT + '\n    </script>\n</body>')
        else:
            content = content.replace('</body>', '    <script>\n' + VISITOR_INIT + '\n    </script>\n</body>')

    # 4. Standardize Mangaluru -> Mangalore
    content = content.replace('Mangaluru', 'Mangalore')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

directory = '.'
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        print(f"Updating {filename}...")
        update_file(os.path.join(directory, filename))
print("Update complete!")
