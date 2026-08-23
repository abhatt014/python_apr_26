from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_super_secret_key' # Required for session management and flash messages

# ==========================================
# DATABASE CONNECTION HELPER
# ==========================================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Change to your MySQL username
        password="redhat@123",  # Change to your MySQL password
        database="ecommerce"
    )

# ==========================================
# ROUTES
# ==========================================
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('products'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('products'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        # Note: In production, NEVER use plain text passwords. Use werkzeug.security hashes.
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        
        if user:
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
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products_list = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('products.html', products=products_list)

@app.route('/order/<int:product_id>', methods=['POST'])
def place_order(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        # 1. Check Stock and Price
        cursor.execute("SELECT name, price, stock FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            flash("Product not found.", "danger")
        elif product['stock'] <= 0:
            flash(f"Sorry, {product['name']} is out of stock.", "danger")
        else:
            # 2. Update stock and create order (Simulated Transaction)
            new_stock = product['stock'] - 1
            cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, product_id))
            
            cursor.execute(
                "INSERT INTO orders (user_id, product_id, total_price) VALUES (%s, %s, %s)",
                (user_id, product_id, product['price'])
            )
            db.commit()
            flash(f"Successfully ordered {product['name']}!", "success")
            
    except mysql.connector.Error as err:
        db.rollback()
        flash(f"Database error: {err}", "danger")
    finally:
        cursor.close()
        db.close()
        
    return redirect(url_for('products'))

@app.route('/orders')
def my_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Join orders with products to get product names
    query = """
        SELECT o.id, p.name as product_name, o.total_price, o.order_date 
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.user_id = %s
        ORDER BY o.order_date DESC
    """
    cursor.execute(query, (session['user_id'],))
    orders_list = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template('orders.html', orders=orders_list)

if __name__ == '__main__':
    app.run(debug=True, port=5001,host='0.0.0.0')