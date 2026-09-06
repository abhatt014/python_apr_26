from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector

app=Flask(__name__,static_folder='assets')
app.secret_key = "SDFy3wegwsr34yta"

##db connection helper function
def get_db_connection():
    return mysql.connector.connect(host="localhost",user="appuser",password="apppassword",database="ecom_mono")
##route
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('products'))
    else:
        return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('products'))
        else: 
            return render_template('login.html')    
    if request.method == 'POST':            
        email=request.form.get('email')
        password=request.form.get('password')
        db = get_db_connection()
        cur = db.cursor(dictionary=True)
        cur.execute("select * from users where email = %s and password = %s",(email,password))
        user=cur.fetchone()
        db.close()
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('products')) 
        else:
            return  render_template('login.html',error="invalid credentials")  


@app.route('/register',methods=['GET','POST'])

def register():
    if request.method == 'GET':
        return render_template('register.html')        
    if request.method == 'POST':
        name= request.form.get('name')
        email= request.form.get('email')
        password=request.form.get('password')
        conn=get_db_connection()
        cur=conn.cursor(dictionary=True)
        query= "insert into users (name,email,password) values (%s,%s,%s);"
        cur.execute(query,(name,email,password))
        conn.commit()
        return render_template("login.html",register_success="successfully registerd")


@app.route('/products')
def products():
    if 'user_id' in session:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        db.close()
        message = request.args.get('message')
        return render_template('products.html',products=products,message=message if 'message' in request.args else None)
    else:
        return redirect(url_for('login'))

@app.route('/order/<int:prod_id>', methods=['POST'])
def order(prod_id):
    if 'user_id'  not in session:
        # Process the order for the given product ID
        return redirect(url_for('login'),error="Please login to place an order")
    else:
        user_id = session['user_id']
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (prod_id,))
        product = cursor.fetchone()
        if product:
            # update the stock of the product
            new_stock = product['stock'] - 1
            cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, prod_id))

            # Insert the order into the orders table
            cursor.execute("INSERT INTO orders (user_id, product_id,total_price) VALUES (%s, %s,%s)", (user_id, prod_id, product['price']))
            db.commit()

            message = "Order placed successfully!"
        else:
            message = "Product not found."
        cursor.close()
        db.close()
        return redirect(url_for('products', message=message))    

@app.route('/orders')
def orders():

    #list all orders
    if 'user_id' in session:
        user_id = session['user_id']
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT o.id, p.name AS product_name, p.price AS product_price, o.total_price FROM orders o JOIN products p ON o.product_id = p.id WHERE o.user_id = %s", (user_id,))
        orders = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('orders.html', orders=orders)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5001)


