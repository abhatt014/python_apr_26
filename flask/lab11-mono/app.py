from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector

app=Flask(__name__,static_folder='assets')
app.secret_key = "SDFy3wegwsr34yta"

##db connection helper function
def get_db_connection():
    return mysql.connector.connect(host="localhost",user="root",password="redhat@123",database="ecom_mono")
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
        return render_template('products.html',products=products)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5001)


