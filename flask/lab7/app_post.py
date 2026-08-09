from flask import Flask, render_template, request # Import request
app = Flask(__name__)

@app.route('/')
def form_page():
    return render_template('index.html') # Serve the page with the form

@app.route('/submit', methods=['POST']) # This route handles the GET request from the first form
def handle_submission_get():
    # 'user_name' matches the 'name' attribute of the input field in the HTML form
    name_from_form = request.form.get('user_name')
    if name_from_form:
        return f"<h1>Hello, {name_from_form}! (Submitted via POST)</h1>"
    else:
        return "<h1>Please enter a name in the form!</h1>"

if __name__ == '__main__':
    app.run(debug=True)

