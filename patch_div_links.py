import os
import re

html_dir = "d:/Project/Remitchain/public"
files = [f for f in os.listdir(html_dir) if f.endswith('.html') and f != 'index.html']

def convert_to_link(match, target_url):
    # Match contains: 1: '<div' or '<a', 2: ' class="... cursor-pointer"', 3: '...', 4: '</div>' or '</a>'
    # We want to replace `<div` with `<a href="target_url"`.
    # And `</div>` with `</a>`
    prefix = match.group(1)
    attrs = match.group(2)
    inner = match.group(3)
    
    # if it's already an <a> tag, ensure href is correct
    if prefix.lower().startswith('<a'):
        # Strip existing href if present in attrs (simplistic)
        attrs = re.sub(r'href=["\'].*?["\']', '', attrs)
        return f'<a href="{target_url}" {attrs}>{inner}</a>'
    else:
        # It's a div
        return f'<a href="{target_url}" {attrs}>{inner}</a>'

for filename in files:
    filepath = os.path.join(html_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic function to replace either <div ...> ... </div> or <a ...> ... </a> for the nav items
    nav_mappings = [
        (r'dashboard', 'Dashboard', 'main_dashboard.html'),
        (r'send', 'Send Money', 'send_money_multi_step_flow.html'),
        (r'history', 'Transactions', 'transaction_history.html'),
        (r'group', 'Beneficiaries', 'beneficiaries_management.html'),
        (r'event_repeat', 'Scheduled Transfers', 'scheduled_transfers.html'),
        (r'settings', 'Settings', 'settings.html'),
        # Mobile specific variants
        (r'paid', 'Send', 'send_money_multi_step_flow.html'),
        (r'history', 'History', 'transaction_history.html'),
    ]

    for icon, text, url in nav_mappings:
        # Regex to match the wrapping element in the sidebar or mobile nav
        # Pattern looks for an element containing the specific icon and text.
        # It handles both <div...>...</div> and <a...>...</a>
        pattern = r'(<(?:div|a))([^>]*?(?:cursor-pointer|transition-transform|hover:bg-white/10|bg-\[\#006C49\]|scale-110)[^>]*?)>(\s*<span[^>]*?>' + icon + r'</span>\s*<span[^>]*?>' + text + r'</span>\s*)</(?:div|a)>'
        
        # We process matches one by one to avoid breaking the file
        def repl(m):
            return convert_to_link(m, url)
        
        content = re.sub(pattern, repl, content, flags=re.IGNORECASE)

    # Some files might have slightly different classes, so let's do a wider fallback for missing ones:
    for icon, text, url in nav_mappings:
        wider_pattern = r'(<(?:div|a))([^>]*?)>(\s*<span[^>]*?data-icon="' + icon + r'"[^>]*?>.*?</span>\s*<span[^>]*?>' + text + r'</span>\s*)</(?:div|a)>'
        content = re.sub(wider_pattern, repl, content, flags=re.IGNORECASE | re.DOTALL)


    # Also fix any "buttons" for receive/send inside the main content if they are <div> or <button>
    content = re.sub(r'<button([^>]*?)>\s*(<div[^>]*?>\s*<span[^>]*?>send</span>\s*</div>)\s*<span[^>]*?>Send</span>\s*</button>', 
                     r'<a href="send_money_multi_step_flow.html"\1>\2<span class="text-sm font-bold tracking-tight">Send</span></a>', content, flags=re.IGNORECASE)
                     
    content = re.sub(r'<button([^>]*?)>\s*(<div[^>]*?>\s*<span[^>]*?>download</span>\s*</div>)\s*<span[^>]*?>Receive</span>\s*</button>', 
                     r'<a href="receive_money.html"\1>\2<span class="text-sm font-bold tracking-tight">Receive</span></a>', content, flags=re.IGNORECASE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Linked all DIV/A tags seamlessly")
