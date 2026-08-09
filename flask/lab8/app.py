from flask import flask
app=flask(__name__)
@app.route(/login)
def login():
    return render_template(login.html)
@app.route(/register)
def register():
    return render_template(register.html)    
@app.route(/dashboard)
def dashboard():
    return render_template(dashboard.html)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    