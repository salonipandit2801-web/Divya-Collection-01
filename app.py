from flask import Flask, render_template, request, redirect, url_for
import os
import urllib.parse

app = Flask(__name__, template_folder='.')

tokens = []
next_token_no = 101
active_token = None

@app.route('/')
def index():
    return render_template('index.html.html')

@app.route('/get-token', methods=['GET', 'POST'])
def get_token():
    global next_token_no
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        if name and phone:
            token_no = next_token_no
            next_token_no += 1
            customer = {"token": token_no, "name": name, "phone": phone}
            tokens.append(customer)

            # Format 1: Success Booking Message
            raw_msg = (
                f"✨🛍️ *DIVYA COLLECTION* 🛍️✨\n"
                f"━━━━━━━━━━━━━━━━━━━\n\n"
                f"Hello {name} ,\n"
                f"Your token has been successfully booked! 🎉\n\n"
                f"🆔 *Token Number:* {token_no}\n\n"
                f"Thank you for visiting our shop! 🙏"
            )
            encoded_msg = urllib.parse.quote(raw_msg)
            whatsapp_url = f"https://wa.me/91{phone}?text={encoded_msg}"

            return render_template('get_token.html.html', success=True, token_no=token_no, whatsapp_url=whatsapp_url)
    return render_template('get_token.html.html', success=False)

@app.route('/products')
def products():
    return render_template('products.html.html')

@app.route('/contact')
def contact():
    return render_template('contact.html.html')

@app.route('/admin')
def admin():
    global active_token
    return render_template('admin.html.html', tokens=tokens, active_token=active_token)

@app.route('/next-person')
def next_person():
    global active_token
    if tokens:
        active_token = tokens.pop(0)

        # Format 2: Counter Alert Message (Sent by Admin)
        name = active_token['name']
        token_no = active_token['token']
        phone = active_token['phone']
        
        raw_msg = (
            f"✨🛍️ *DIVYA COLLECTION* 🛍️✨\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"Hello {name} ,\n"
            f"Your turn will come in 10 minutes! ⏳\n\n"
            f"🔢 *Token Number:* {token_no}\n\n"
            f"Please proceed to Counter 1. See you soon! 😊"
        )
