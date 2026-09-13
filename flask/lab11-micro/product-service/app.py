from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DATABASE"),
    )


def serialize_product(p):
    return {
        "id": p["id"],
        "name": p["name"],
        "price": str(p["price"]),
        "stock": p["stock"],
    }


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/products", methods=["GET"])
def list_products():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([serialize_product(p) for p in products]), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if not product:
        return jsonify(error="product not found"), 404
    return jsonify(serialize_product(product)), 200


@app.route("/products/<int:product_id>/reserve", methods=["POST"])
def reserve_stock(product_id):
    """Internal endpoint: atomically decrements stock for an order.

    Uses SELECT ... FOR UPDATE inside a transaction so concurrent orders
    can't oversell stock (a bug present in the original monolith).
    """
    data = request.get_json(silent=True) or {}
    try:
        quantity = int(data.get("quantity", 1))
    except (TypeError, ValueError):
        return jsonify(error="quantity must be an integer"), 400

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        cur.execute("SELECT * FROM products WHERE id = %s FOR UPDATE", (product_id,))
        product = cur.fetchone()

        if not product:
            conn.rollback()
            return jsonify(error="product not found"), 404

        if product["stock"] < quantity:
            conn.rollback()
            return jsonify(error="insufficient stock"), 409

        new_stock = product["stock"] - quantity
        cur.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, product_id))
        conn.commit()

        return jsonify(id=product["id"], name=product["name"], price=str(product["price"]), stock=new_stock), 200
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)