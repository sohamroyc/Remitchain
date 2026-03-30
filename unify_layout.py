import os
import re

html_dir = "d:/Project/Remitchain/public"

# 1. Extract the ideal layout from main_dashboard.html
with open(os.path.join(html_dir, 'main_dashboard.html'), 'r', encoding='utf-8') as f:
    dashboard_html = f.read()

# Capture the sidebar (<aside>...</aside>)
aside_match = re.search(r'(<aside.*?</aside>)', dashboard_html, re.DOTALL)
ideal_aside = aside_match.group(1) if aside_match else ""

# Capture the mobile bottom nav (<nav class="lg:hidden fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-4 pb-8 pt-4 bg-white/80 dark:bg-[#131B2E]/80 backdrop-blur-md shadow-\[0_-10px_40px_rgba\(0,0,0,0\.04\)\] rounded-t-3xl border-t border-slate-100 dark:border-slate-800">.*?</nav>)
mobile_nav_match = re.search(r'(<nav class="lg:hidden fixed bottom-0 left-0.*?</nav>)', dashboard_html, re.DOTALL)
ideal_mobile_nav = mobile_nav_match.group(1) if mobile_nav_match else ""

files = [f for f in os.listdir(html_dir) if f.endswith('.html') and f != 'index.html' and f != 'main_dashboard.html']

for filename in files:
    filepath = os.path.join(html_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace existing <aside>...</aside> with the ideal aside
    # But wait, we need to adjust the active highlighting state based on the current page!
    
    # First, let's inject the identical aside structure
    content = re.sub(r'<aside.*?</aside>', ideal_aside.replace('\\', '\\\\'), content, flags=re.DOTALL)
    
    # Replace the mobile nav
    content = re.sub(r'<nav class="lg:hidden fixed bottom-0 left-0.*?</nav>', ideal_mobile_nav.replace('\\', '\\\\'), content, flags=re.DOTALL)
    
    # Now we must dynamically apply the active state for the current page inside the sidebar and mobile nav!
    # The active state in main_dashboard is: class="bg-[#006C49] text-white rounded-xl mx-2 px-4 py-3 flex items-center gap-3 transition-all duration-200 ease-in-out font-manrope text-sm font-medium"
    # The inactive state is: class="text-slate-300 hover:text-white hover:bg-white/10 rounded-xl mx-2 px-4 py-3 flex items-center gap-3 transition-all duration-200 ease-in-out font-manrope text-sm font-medium"
    
    # Simple trick: Make everything inactive first, then make the current page target active.
    # Turn ALL items into exact inactive classes:
    content = re.sub(r'class="bg-\[\#006C49\] text-white([^"]*?)"', r'class="text-slate-300 hover:text-white hover:bg-white/10\1"', content)
    
    # Mobile nav active state trick: scale-110 and text-[#006C49]
    content = re.sub(r'class="flex flex-col items-center justify-center text-\[\#006C49\] scale-110([^"]*?)"', r'class="flex flex-col items-center justify-center text-slate-400 dark:text-slate-500\1"', content)
    
    # Determine the target href based on filename
    target_href = filename
    
    # Set the specific active state for the current page in Desktop Nav
    content = re.sub(f'(href="{target_href}"\\s*class=")(text-slate-300 hover:text-white hover:bg-white/10)([^"]*?)(")', 
                     r'\1bg-[#006C49] text-white\3\4', content)
                     
    # Set specific active state for the current page in Mobile Nav
    content = re.sub(f'(href="{target_href}"\\s*class=")(flex flex-col items-center justify-center text-slate-400 dark:text-slate-500)([^"]*?)(")', 
                     r'\1flex flex-col items-center justify-center text-[#006C49] scale-110\3\4', content)

    # 2. Make Small Features Workable (Dropdowns, Tabs, Copy Buttons)
    if filename == "receive_money.html":
        # Add copy to clipboard logic for Account Number and IBAN
        script_receive = """
<script>
document.addEventListener('DOMContentLoaded', () => {
    // Make copy buttons work
    const copyIcons = document.querySelectorAll('.material-symbols-outlined');
    copyIcons.forEach(icon => {
        if (icon.innerText.includes('content_copy')) {
            const container = icon.closest('.flex.items-center.justify-between.bg-surface');
            if(container) {
                const textToCopy = container.querySelector('p.font-medium').innerText;
                icon.parentElement.addEventListener('click', () => {
                    navigator.clipboard.writeText(textToCopy);
                    icon.innerText = 'check';
                    icon.style.color = '#006C49';
                    setTimeout(() => { icon.innerText = 'content_copy'; icon.style.color = ''; }, 2000);
                });
            }
        }
    });
});
</script>
</body>
"""
        content = content.replace('</body>', script_receive)
        
    elif filename == "settings.html":
        # Add toggle switches logic
        script_set = """
<script>
document.addEventListener('DOMContentLoaded', () => {
    const toggles = document.querySelectorAll('input[type="checkbox"]');
    toggles.forEach(t => {
        t.addEventListener('change', (e) => {
            console.log('Toggled: ', e.target.checked);
        });
    });
});
</script>
</body>
"""
        content = content.replace('</body>', script_set)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Layout unified and small features enriched across all files.")
