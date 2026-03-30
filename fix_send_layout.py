import os
import re

html_dir = "d:/Project/Remitchain/public"

# Read ideal layout pieces from main_dashboard.html
with open(os.path.join(html_dir, 'main_dashboard.html'), 'r', encoding='utf-8') as f:
    dashboard_html = f.read()

# Capture sidebar
aside_match = re.search(r'(<aside.*?</aside>)', dashboard_html, re.DOTALL)
ideal_aside = aside_match.group(1)

# Capture top header
header_match = re.search(r'(<header.*?</header>)', dashboard_html, re.DOTALL)
ideal_header = header_match.group(1)

# Capture mobile bottom nav
mobile_nav_match = re.search(r'(<nav class="lg:hidden fixed bottom-0 left-0.*?</nav>)', dashboard_html, re.DOTALL)
ideal_mobile_nav = mobile_nav_match.group(1)

# Update send_money_multi_step_flow.html
send_file = os.path.join(html_dir, 'send_money_multi_step_flow.html')
with open(send_file, 'r', encoding='utf-8') as f:
    send_content = f.read()

# 1. Remove the old top <nav>
send_content = re.sub(r'<nav class="bg-white.*?</nav>', '', send_content, flags=re.DOTALL)

# 2. Inject <aside> right after <body...>
send_content = re.sub(r'(<body[^>]*>)', r'\1\n' + ideal_aside.replace('\\', '\\\\'), send_content)

# 3. Add lg:ml-64 to <main> and inject <header> right after <main...>
def modify_main(match):
    # match.group(1) is the original <main ...> piece.
    # Add lg:ml-64 if not present
    main_tag = match.group(0)
    if 'lg:ml-64' not in main_tag:
        main_tag = main_tag.replace('class="', 'class="lg:ml-64 ')
    return main_tag + '\n' + ideal_header

send_content = re.sub(r'<main[^>]*>', modify_main, send_content)

# 4. Replace the mobile bottom nav
send_content = re.sub(r'<div class="lg:hidden fixed bottom-0 left-0[^>]*>.*?</div>', '', send_content, flags=re.DOTALL)
send_content = re.sub(r'</body>', ideal_mobile_nav.replace('\\', '\\\\') + '\n</body>', send_content)

# 5. Fix Active State for Send Money
filename = 'send_money_multi_step_flow.html'
# Turn all aside items into inactive classes
send_content = re.sub(r'class="bg-\[\#006C49\] text-white([^"]*?)"', r'class="text-slate-300 hover:text-white hover:bg-white/10\1"', send_content)
# Turn all mobile items into inactive
send_content = re.sub(r'class="flex flex-col items-center justify-center text-\[\#006C49\] scale-110([^"]*?)"', r'class="flex flex-col items-center justify-center text-slate-400 dark:text-slate-500\1"', send_content)

# Make send money active
send_content = re.sub(r'(href="send_money_multi_step_flow\.html"\s*class=")(text-slate-300 hover:text-white hover:bg-white/10)([^"]*?)(")', 
                    r'\1bg-[#006C49] text-white\3\4', send_content)
                    
send_content = re.sub(r'(href="send_money_multi_step_flow\.html"\s*class=")(flex flex-col items-center justify-center text-slate-400 dark:text-slate-500)([^"]*?)(")', 
                    r'\1flex flex-col items-center justify-center text-[#006C49] scale-110\3\4', send_content)

# Update the header title text for Send Money
send_content = send_content.replace('<h2 class="text-xl font-bold font-headline tracking-tight text-primary">Dashboard</h2>',
                                    '<h2 class="text-xl font-bold font-headline tracking-tight text-primary">Send Money</h2>')

with open(send_file, 'w', encoding='utf-8') as f:
    f.write(send_content)

print("Fixed Send Money page layout!")
