from flask import Flask, request, jsonify
import mysql.connector
import os
import requests

app = Flask(__name__)

PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://product-service:5003")


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DATABASE"),
    )


def serialize_order(o):
    return {
        "id": o["id"],
        "product_name": o["product_name"],
        "product_price": str(o["product_price"]),
        "total_price": str(o["total_price"]),
        "order_date": o["order_date"].isoformat() if o["order_date"] else None,
    }


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or request.form
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id or not product_id:
        return jsonify(error="user_id and product_id are required"), 400

    # Ask product-service to atomically reserve one unit of stock.
    try:
        reserve_resp = requests.post(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}/reserve",
            json={"quantity": 1},
            timeout=5,
        )
    except requests.RequestException:
        return jsonify(error="product service unavailable"), 503

    if reserve_resp.status_code == 404:
        return jsonify(error="product not found"), 404
    if reserve_resp.status_code == 409:
        return jsonify(error="insufficient stock"), 409
    if reserve_resp.status_code != 200:
        return jsonify(error="could not reserve product"), 502

    product = reserve_resp.json()

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO orders (user_id, product_id, product_name, product_price, total_price) "
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, product_id, product["name"], product["price"], product["price"]),
        )
        conn.commit()
        order_id = cur.lastrowid
    finally:
        cur.close()
        conn.close()

    # NOTE: if the process crashed between the reserve call above and this
    # insert, stock would be decremented with no order recorded. A production
    # system would use a saga/outbox pattern to make this fully consistent;
    # flagged here rather than silently glossed over.
    return jsonify(id=order_id, message="Order placed successfully!"), 201


@app.route("/orders", methods=["GET"])
def list_orders():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify(error="user_id query param is required"), 400

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id, product_name, product_price, total_price, order_date "
        "FROM orders WHERE user_id = %s ORDER BY order_date DESC",
        (user_id,),
    )
    orders = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([serialize_order(o) for o in orders]), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)