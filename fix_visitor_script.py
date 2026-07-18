import os, re

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if the raw text "// VISITOR COUNTER (Dynamic Simulation)" appears OUTSIDE a script tag
        # To be safe, let's just remove ALL instances of the visitor counter code
        
        # Remove the raw visitor counter text that might be floating around
        content = re.sub(r'// ============================================\s*// VISITOR COUNTER \(Dynamic Simulation\).*?window\.addEventListener\(\'load\', initializeVisitorCounter\);', '', content, flags=re.DOTALL)
        
        # Also remove empty script tags that might have been left behind
        content = re.sub(r'<script>\s*</script>', '', content)
        
        # Now append the visitor counter properly before </body>
        visitor_script = """
    <script>
        // ============================================
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
        window.addEventListener('load', initializeVisitorCounter);
    </script>
"""
        content = content.replace('</body>', visitor_script + '</body>')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

print("Fixed visitor scripts!")
