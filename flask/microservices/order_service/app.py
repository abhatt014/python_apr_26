import os, requests
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"), database=os.environ.get("DB_NAME")
    )

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data['user_id']
    product_id = data['product_id']
    
    # 1. Talk to Product Service to deduct stock and get price
    # Container name acts as the domain name!
    prod_resp = requests.post(f"http://product-service:5000/api/products/{product_id}/deduct")
    
    if prod_resp.status_code != 200:
        return jsonify(prod_resp.json()), prod_resp.status_code
        
    product_data = prod_resp.json()
    
    # 2. Save order
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, product_id, total_price) VALUES (%s, %s, %s)",
        (user_id, product_id, product_data['price'])
    )
    db.commit()
    cursor.close()
    db.close()
    
    return jsonify({"message": "Order placed", "product_name": product_data['name']}), 201

@app.route('/api/orders/user/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    # Joining with products table (In strict microservices, this would be another API call)
    cursor.execute("""
        SELECT o.id, p.name as product_name, o.total_price, o.order_date 
        FROM orders o JOIN products p ON o.product_id = p.id WHERE o.user_id = %s
    """, (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)