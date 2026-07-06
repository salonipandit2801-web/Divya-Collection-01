from flask import Flask, render_template, request, redirect, url_for
import os
import urllib.parse

# आपण फ्लॅस्कला सांगतोय की templates फोल्डर बाहेरच आहे (root मध्ये)
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

            raw_msg = f"Hello {name}, Your token is {token_no}!"
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
