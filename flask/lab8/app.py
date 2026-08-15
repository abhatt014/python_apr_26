from flask import Flask,render_template,request
import mysql.connector

app=Flask(__name__)
db_config = {
    'host':'localhost',
    'database':'myapp',
    'user':'root',
    'password':'redhat@123'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/")
def home():
    return "<h1>Access Login page from <a href='/login'>here</a></h1>"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/processlogin",methods=['POST'])
def processlogin():
    email= request.form.get('email')
    password=request.form.get('password')

    conn=get_db_connection()
    cur=conn.cursor(dictionary=True)

    query= "select * from users where email = %s"
    cur.execute(query,(email,))
    userinfo=cur.fetchone()
    if userinfo and password == userinfo['password']:
        return render_template("dashboard.html",fullname=userinfo['fullname'],role=userinfo['role'])
    else:
        return render_template("login.html",error="unauthorized")               

@app.route("/register")
def register():
    return render_template("register.html")    


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    