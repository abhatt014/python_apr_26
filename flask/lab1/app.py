# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to homepage</h1>"

@app.route('/contact')
def contact():
    return "<h3>Welcome to Contact US Page</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
