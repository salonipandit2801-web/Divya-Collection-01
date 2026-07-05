from flask import Flask, render_template, request, redirect, url_for
import os
import urllib.parse

app = Flask(__name__)

# Global variables
tokens = []
next_token_no = 101
active_token = None

# --- 1. HOME PAGE ---
@app.route('/')
def index():
    return render_template('index.html.html')

# --- 2. GET TOKEN PAGE ---
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

            # Creating WhatsApp Link for Confirmation
            raw_msg = (
                f"✨🛍️ *DIVYA COLLECTION* 🛍️✨\n"
                f"━━━━━━━━━━━━━━━━━━━\n\n"
                f"Hello {name},\n"
                f"Your token has been successfully booked! 🎉\n\n"
                f"🆔 *Token Number:* {token_no}\n\n"
                f"Thank you for visiting our shop! 🙏"
            )
            encoded_msg = urllib.parse.quote(raw_msg)
            formatted_phone = f"91{phone}" if len(phone) == 10 else phone
            whatsapp_url = f"https://wa.me/{formatted_phone}?text={encoded_msg}"

            return render_template('get_token.html.html', success=True, token_no=token_no, whatsapp_url=whatsapp_url)

    return render_template('get_token.html.html', success=False)

# --- 3. PRODUCTS PAGE ---
@app.route('/products')
def products():
    return render_template('products.html.html')

# --- 4. CONTACT PAGE ---
@app.route('/contact')
def contact():
    return render_template('contact.html.html')

# --- 5. ADMIN PANEL ---
@app.route('/admin')
def admin():
    global active_token
    shop_details = {"name": "Divya Collection"}
    return render_template('admin.html.html', tokens=tokens, active_token=active_token, shop_details=shop_details)

# --- 6. NEXT PERSON BUTTON ---
@app.route('/next-person')
def next_person():
    global active_token
    if tokens:
        active_token = tokens.pop(0)
    else:
        active_token = None
        
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
