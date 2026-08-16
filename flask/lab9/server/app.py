from flask import Flask,request,jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app, resources={r"/books/*": {"origins": "http://127.0.0.1:5001"}}) 
database = {
    1:{"name":"python crash course","author":"person1"}
}
# handle GET :get all data
@app.route('/books',methods=['GET'])
def get_books():
    return jsonify(database)

# handle POST :Create new  data
@app.route('/books',methods=['POST'])
def create_book():
    data = request.get_json()
    newid = max(database.keys())+1
    database[newid] = data
    return database[newid]
# handle PUT :update existing data
@app.route('/books/<int:id>',methods=['PUT'])
def update_book(id):
    data = request.get_json()
    database[id] = data
    return database[id]
# handle PATCH :partially update existing data
@app.route('/books/<int:id>',methods=['PATCH'])
def partial_update_book(id):
    data = request.get_json()
    for key,value in data.items():
        database[id][key] = value
        return database[id]
# handle DELETE :delete existing data
@app.route('/books/<int:id>',methods=['DELETE'])
def delete_book(id):
    if id not in database:
        return jsonify({"error":"book not found"})
    else:
        del database[id]
        return jsonify({"success":"book deleted"})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)