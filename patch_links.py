import os
import re

html_dir = "d:/Project/Remitchain/public"

files = [f for f in os.listdir(html_dir) if f.endswith('.html') and f != 'index.html']

for filename in files:
    filepath = os.path.join(html_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic replace for Desktop SideNavBar
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>dashboard</span>\s*<span>Dashboard</span>)', r'\g<1>main_dashboard.html\3', content, flags=re.IGNORECASE)
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>send</span>\s*<span>Send Money</span>)', r'\g<1>send_money_multi_step_flow.html\3', content, flags=re.IGNORECASE)
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>history</span>\s*<span>Transactions</span>)', r'\g<1>transaction_history.html\3', content, flags=re.IGNORECASE)
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>group</span>\s*<span>Beneficiaries</span>)', r'\g<1>beneficiaries_management.html\3', content, flags=re.IGNORECASE)
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>event_repeat</span>\s*<span>Scheduled Transfers</span>)', r'\g<1>scheduled_transfers.html\3', content, flags=re.IGNORECASE)
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>settings</span>\s*<span>Settings</span>)', r'\g<1>settings.html\3', content, flags=re.IGNORECASE)

    # Mobile nav bar
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>dashboard</span>\s*<span[^>]*?>Dashboard</span>)', r'\g<1>main_dashboard.html\3', content, flags=re.IGNORECASE)
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>paid</span>\s*<span[^>]*?>Send</span>)', r'\g<1>send_money_multi_step_flow.html\3', content, flags=re.IGNORECASE)
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>history</span>\s*<span[^>]*?>History</span>)', r'\g<1>transaction_history.html\3', content, flags=re.IGNORECASE)
    content = re.sub(r'(<a[^>]*?href=["\'])([^"\']*?)(["\'][^>]*?>\s*<span[^>]*?>settings</span>\s*<span[^>]*?>Settings</span>)', r'\g<1>settings.html\3', content, flags=re.IGNORECASE)

    # Convert generic <button> tags indicating navigation to <a> tags (like the Dashboard quick actions)
    # Ex: send
    content = re.sub(r'<button([^>]*?)>\s*(<div[^>]*?>\s*<span[^>]*?>send</span>\s*</div>)\s*<span[^>]*?>Send</span>\s*</button>', 
                     r'<a href="send_money_multi_step_flow.html"\1>\2<span class="text-sm font-bold tracking-tight">Send</span></a>', content, flags=re.IGNORECASE)
    # Receive
    content = re.sub(r'<button([^>]*?)>\s*(<div[^>]*?>\s*<span[^>]*?>download</span>\s*</div>)\s*<span[^>]*?>Receive</span>\s*</button>', 
                     r'<a href="receive_money.html"\1>\2<span class="text-sm font-bold tracking-tight">Receive</span></a>', content, flags=re.IGNORECASE)
                     
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done updating hyperlinks")
