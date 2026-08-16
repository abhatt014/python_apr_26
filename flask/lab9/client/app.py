from flask  import Flask,render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)

# SERVER_URL = "http://localhost:5000/books"

# # #fetch all the books
# res = requests.get(SERVER_URL)
# print(res.json())

# #add new book
# new_book = {"name":"python complete refernce","author":"person2"}
# res = requests.post(SERVER_URL,json=new_book)
# print(res.json())

# #update existing book
# updates = {"name":"python crash course 2nd ed","author":"newperson"}
# res = requests.put(f"{SERVER_URL}/1",json=updates)
# print(res.json())

# # #partially update the 1st book 
# partial_update = {"author":"AmitB"}
# res = requests.patch(f"{SERVER_URL}/1",json=partial_update)
# print(res.json())

# #remove python complete reference
# res = requests.delete(f"{SERVER_URL}/2")
# print(res.json())