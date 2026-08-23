from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

# Docker handles DNS. We use container names as URLs.
USER_API = "http://user-service:5000/api"
PRODUCT_API = "http://product-service:5000/api"
ORDER_API = "http://order-service:5000/api"

@app.route('/')
def home():
    return redirect(url_for('products') if 'user_id' in session else url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Send credentials to User Service
        resp = requests.post(f"{USER_API}/login", json={
            "email": request.form['email'], 
            "password": request.form['password']
        })
        
        if resp.status_code == 200:
            user = resp.json()
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('products'))
        else:
            flash("Invalid email or password", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Fetch products from Product Service
    resp = requests.get(f"{PRODUCT_API}/products")
    products_list = resp.json() if resp.status_code == 200 else []
    
    return render_template('products.html', products=products_list)

@app.route('/order/<int:product_id>', methods=['POST'])
def place_order(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Ask Order Service to create the order
    resp = requests.post(f"{ORDER_API}/orders", json={
        "user_id": session['user_id'],
        "product_id": product_id
    })
    
    if resp.status_code == 201:
        data = resp.json()
        flash(f"Successfully ordered {data['product_name']}!", "success")
    else:
        error_msg = resp.json().get('error', 'Failed to place order')
        flash(error_msg, "danger")
        
    return redirect(url_for('products'))

@app.route('/orders')
def my_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Fetch orders from Order Service
    resp = requests.get(f"{ORDER_API}/orders/user/{session['user_id']}")
    orders_list = resp.json() if resp.status_code == 200 else []
    
    return render_template('orders.html', orders=orders_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)