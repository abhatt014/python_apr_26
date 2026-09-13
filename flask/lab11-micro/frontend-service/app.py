from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os

app = Flask(__name__, static_folder='assets')
# Load the secret key from the environment instead of hardcoding it in source.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth-service:5002")
PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://product-service:5003")
ORDER_SERVICE_URL = os.environ.get("ORDER_SERVICE_URL", "http://order-service:5004")


@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('products'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('products'))
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        resp = requests.post(
            f"{AUTH_SERVICE_URL}/login",
            json={"email": email, "password": password},
            timeout=5,
        )
    except requests.RequestException:
        return render_template('login.html', error="Login is temporarily unavailable. Please try again shortly."), 503

    if resp.status_code == 200:
        user = resp.json()
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('products'))

    error = resp.json().get('error', 'Invalid credentials') if resp.content else 'Invalid credentials'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        resp = requests.post(
            f"{AUTH_SERVICE_URL}/register",
            json={"name": name, "email": email, "password": password},
            timeout=5,
        )
    except requests.RequestException:
        return render_template('register.html', error="Registration is temporarily unavailable. Please try again shortly."), 503

    if resp.status_code == 201:
        return render_template('login.html', register_success="Successfully registered")

    error = resp.json().get('error', 'Registration failed') if resp.content else 'Registration failed'
    return render_template('register.html', error=error)


@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        resp = requests.get(f"{PRODUCT_SERVICE_URL}/products", timeout=5)
        product_list = resp.json() if resp.status_code == 200 else []
    except requests.RequestException:
        product_list = []

    message = request.args.get('message')
    return render_template('products.html', products=product_list, message=message)


@app.route('/order/<int:prod_id>', methods=['POST'])
def order(prod_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        resp = requests.post(
            f"{ORDER_SERVICE_URL}/orders",
            json={"user_id": session['user_id'], "product_id": prod_id},
            timeout=5,
        )
        body = resp.json() if resp.content else {}
        message = body.get('message') if resp.status_code == 201 else body.get('error', 'Could not place order')
    except requests.RequestException:
        message = "Ordering is temporarily unavailable. Please try again shortly."

    return redirect(url_for('products', message=message))


@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        resp = requests.get(
            f"{ORDER_SERVICE_URL}/orders",
            params={"user_id": session['user_id']},
            timeout=5,
        )
        order_list = resp.json() if resp.status_code == 200 else []
    except requests.RequestException:
        order_list = []

    return render_template('orders.html', orders=order_list)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == "__main__":
    # debug=True removed: it exposes the Werkzeug interactive debugger
    # (a remote-code-execution risk) if it ever reaches a real deployment.
    app.run(host='0.0.0.0', port=5001)