import os
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"), database=os.environ.get("DB_NAME")
    )

@app.route('/api/products', methods=['GET'])
def get_products():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(products), 200

@app.route('/api/products/<int:product_id>/deduct', methods=['POST'])
def deduct_stock(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    if product['stock'] <= 0:
        return jsonify({"error": "Out of stock"}), 400
        
    cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = %s", (product_id,))
    db.commit()
    cursor.close()
    db.close()
    
    return jsonify({"message": "Stock deducted", "price": product['price'], "name": product['name']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)