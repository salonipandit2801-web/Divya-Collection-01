# -*- coding: utf-8 -*-
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

            # Using direct URL encoding strings to guarantee emoji rendering on laptop web
            encoded_msg = (
                "%E2%9C%A8%F0%9F%92%B0%20*DIVYA%20COLLECTION*%20%F0%9F%92%B0%E2%9C%A8%0A"
                "-----------------------------\n\n"
                f"Hello%20{urllib.parse.quote(name)},%0A"
                "Your%20token%20has%20been%20successfully%20booked%21%20%F0%9F%8E%89%0A%0A"
                f"%F0%9F%8A%94%20*Token%20Number%3A*%20{token_no}%0A%0A"
                "Thank%20you%20for%20visiting%20our%20shop%21%20%F0%9F%99%8F"
            )

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
    whatsapp_admin_url = None
    if active_token:
        name = active_token['name']
        token_no = active_token['token']
        phone = active_token['phone']

        # URL encoded format for admin messaging to prevent question marks
        encoded_msg_admin = (
            "%E2%9C%A8%F0%9F%92%B0%20*DIVYA%20COLLECTION*%20%F0%9F%92%B0%E2%9C%A8%0A"
            "-----------------------------\n\n"
            f"Hello%20{urllib.parse.quote(name)},%0A"
            "Your%20turn%20will%20come%20in%2010%20minutes%21%20%E2%8F%B3%0A%0A"
            f"%F0%9F%8A%94%20*Token%20Number%3A*%20{token_no}%0A%0A"
            "Please%20proceed%20to%20Counter%201.%20See%20you%20soon%21%20%F0%9F%98%8A"
        )

        whatsapp_admin_url = f"https://wa.me/91{phone}?text={encoded_msg_admin}"

    return render_template('admin.html.html', tokens=tokens, active_token=active_token, whatsapp_admin_url=whatsapp_admin_url)

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
