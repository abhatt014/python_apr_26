from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
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


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify(error="name, email and password are required"), 400

    hashed = generate_password_hash(password)
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed),
        )
        conn.commit()
        return jsonify(id=cur.lastrowid, name=name, email=email), 201
    except mysql.connector.IntegrityError:
        conn.rollback()
        return jsonify(error="An account with this email already exists"), 409
    finally:
        cur.close()
        conn.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or request.form
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify(error="email and password are required"), 400

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if user and check_password_hash(user["password"], password):
        return jsonify(id=user["id"], name=user["name"], email=user["email"]), 200
    return jsonify(error="invalid credentials"), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)