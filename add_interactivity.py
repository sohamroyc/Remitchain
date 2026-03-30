import os
import re

html_dir = "d:/Project/Remitchain/public"

# 1. Update Send Money Multi Step Flow
send_money_file = os.path.join(html_dir, 'send_money_multi_step_flow.html')
with open(send_money_file, 'r', encoding='utf-8') as f:
    sm_content = f.read()

# Add IDs to steps
sm_content = sm_content.replace('<div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">', 
                                '<div id="step1" class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">')
sm_content = sm_content.replace('<!-- Step 2: Recipient Selection (Visualizing for Design Completeness) -->\n<div class="mt-24">', 
                                '<!-- Step 2 -->\n<div id="step2" class="mt-24" style="display:none;">')
sm_content = sm_content.replace('<!-- Step 3 Preview (Success Modal Style) -->\n<div class="mt-24 p-12 bg-white rounded-[2rem]', 
                                '<!-- Step 3 -->\n<div id="step3" class="mt-24 p-12 bg-white rounded-[2rem]" style="display:none;"')

# Add IDs to buttons
sm_content = sm_content.replace('<button class="w-full bg-primary-container text-white py-5 rounded-2xl', 
                                '<button id="btn-continue" class="w-full bg-primary-container text-white py-5 rounded-2xl')

sm_content = sm_content.replace('<div class="h-48 bg-white p-6 rounded-2xl shadow-sm flex flex-col justify-between border-2 border-transparent hover:border-secondary cursor-pointer transition-all">',
                                '<div class="recipient-card h-48 bg-white p-6 rounded-2xl shadow-sm flex flex-col justify-between border-2 border-transparent hover:border-secondary cursor-pointer transition-all">')

# Inject script
script_sm = """
<script>
document.addEventListener('DOMContentLoaded', () => {
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const step3 = document.getElementById('step3');
    
    document.getElementById('btn-continue').addEventListener('click', () => {
        step1.style.display = 'none';
        step2.style.display = 'block';
        window.scrollTo(0, 0);
    });

    const cards = document.querySelectorAll('.recipient-card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            step2.style.display = 'none';
            step3.style.display = 'block';
            window.scrollTo(0, 0);
        });
    });
});
</script>
</body>
"""
sm_content = sm_content.replace('</body>', script_sm)
with open(send_money_file, 'w', encoding='utf-8') as f:
    f.write(sm_content)

# 2. Update Main Dashboard (Currency Toggle)
dashboard_file = os.path.join(html_dir, 'main_dashboard.html')
with open(dashboard_file, 'r', encoding='utf-8') as f:
    db_content = f.read()

# Add IDs
db_content = db_content.replace('<button class="px-4 py-1.5 rounded-lg bg-white text-primary-container text-xs font-bold transition-all">AED</button>',
                                '<button id="btn-aed" class="px-4 py-1.5 rounded-lg bg-white text-primary-container text-xs font-bold transition-all">AED</button>')
db_content = db_content.replace('<button class="px-4 py-1.5 rounded-lg text-white text-xs font-medium hover:bg-white/5 transition-all">INR</button>',
                                '<button id="btn-inr" class="px-4 py-1.5 rounded-lg text-white text-xs font-medium hover:bg-white/5 transition-all">INR</button>')
db_content = db_content.replace('<span class="text-secondary-fixed">AED</span> 142,580.00',
                                '<span id="bal-currency" class="text-secondary-fixed">AED</span> <span id="bal-amount">142,580.00</span>')

script_db = """
<script>
document.addEventListener('DOMContentLoaded', () => {
    const btnAed = document.getElementById('btn-aed');
    const btnInr = document.getElementById('btn-inr');
    const balCurrency = document.getElementById('bal-currency');
    const balAmount = document.getElementById('bal-amount');

    const activeClass = "bg-white text-primary-container font-bold".split(' ');
    const inactiveClass = "text-white font-medium hover:bg-white/5".split(' ');

    btnAed.addEventListener('click', () => {
        btnAed.classList.add(...activeClass);
        btnAed.classList.remove(...inactiveClass);
        btnInr.classList.add(...inactiveClass);
        btnInr.classList.remove(...activeClass);
        balCurrency.innerText = 'AED';
        balAmount.innerText = '142,580.00';
    });
    
    btnInr.addEventListener('click', () => {
        btnInr.classList.add(...activeClass);
        btnInr.classList.remove(...inactiveClass);
        btnAed.classList.add(...inactiveClass);
        btnAed.classList.remove(...activeClass);
        balCurrency.innerText = 'INR';
        balAmount.innerText = '3,214,000.00';
    });
});
</script>
</body>
"""
db_content = db_content.replace('</body>', script_db)
with open(dashboard_file, 'w', encoding='utf-8') as f:
    f.write(db_content)

# 3. Update Auth OTP
auth_file = os.path.join(html_dir, 'authentication_phone_otp.html')
if os.path.exists(auth_file):
    with open(auth_file, 'r', encoding='utf-8') as f:
        auth_content = f.read()
    
    auth_content = auth_content.replace('<input class="w-16 h-16 sm:w-20 sm:h-24 text-center text-4xl font-headline font-extrabold bg-transparent border-b-4 border-outline focus:border-primary-container focus:ring-0 transition-colors p-0 rounded-none"',
                                        '<input class="otp-input w-16 h-16 sm:w-20 sm:h-24 text-center text-4xl font-headline font-extrabold bg-transparent border-b-4 border-outline focus:border-primary-container focus:ring-0 transition-colors p-0 rounded-none" maxlength="1"')
    
    script_auth = """
<script>
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.otp-input');
    inputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !input.value && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });
});
</script>
</body>
"""
    auth_content = auth_content.replace('</body>', script_auth)
    with open(auth_file, 'w', encoding='utf-8') as f:
        f.write(auth_content)

print("Vanilla JS added for UI interactivity.")
