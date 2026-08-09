from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    current_day = datetime.today().strftime("%A")
    user_name = "DevOps Learner"
    items = ["Learn Flask", "Build an API", "Deploy an App"]
    # Pass variables to the template
    return render_template('index.html',
                           day=current_day,
                           name=user_name,
                           tasks=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
