# app.py
from flask import Flask, jsonify # jsonify can also be used for more control
app = Flask(__name__)

@app.route('/api/user_data')
def get_user_data():
    user = {
    "id": 1,
    "username": "flaskdev",
    "email": "dev@example.com",
    "isActive": True
    }
    return user # Flask auto-converts this dict to JSON

@app.route('/api/items')
def get_items():
    items_list = ["apple", "banana", "cherry"]
    # For more complex scenarios or to explicitly set status codes with JSON:
    return jsonify(items=items_list, count=len(items_list)), 200 # Returns JSON and HTTP 200 OK

@app.route('/add/<a>/<b>')
def add_numbers_api(a, b):
    try:
        num_a = int(a)
        num_b = int(b)
        result_sum = num_a + num_b
        response = {
        'input_a': num_a,
        'input_b': num_b,
        'result': result_sum,
        'operation': 'addition'
        }
        return response # Flask auto-converts this dict to JSON
    except ValueError:
        error_response = {
        'error': 'Invalid input. Please provide integers for a and b.'
        }
        return error_response, 400 # Return JSON error and HTTP 400 Bad Request status
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)