from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

import os

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(
    DATABASE_URL,
    sslmode="require"
)

@app.route("/")
def home():
    return "Guest Post Management System Backend Running!"


@app.route("/clients")
def get_clients():
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    cur.close()

    clients = []

    for row in rows:
        clients.append({
            "client_id": row[0],
            "full_name": row[1],
            "email": row[2],
            "company_name": row[3],
            "phone": row[4],
            "created_at": str(row[5])
        })

    return jsonify(clients)

@app.route("/add-order", methods=["POST"])
def add_order():

    data = request.get_json()

    try:
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO orders (client_id, target_link, anchor_text, price, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["client_id"],
                data["target_link"],
                data["anchor_text"],
                data["price"],
                data["status"]
            )
        )

        conn.commit()
        cur.close()

        return jsonify({"message": "Order Added Successfully!"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.get_json()

    try:
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO clients (full_name, email, company_name, phone)
            VALUES (%s, %s, %s, %s)
            """,
            (
                data["full_name"],
                data["email"],
                data["company_name"],
                data["phone"]
            )
        )

        conn.commit()
        cur.close()

        return jsonify({"message": "Client Added Successfully!"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400


@app.route("/orders")
def get_orders():
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    cur.close()

    orders = []

    for row in rows:
        orders.append({
            "order_id": row[0],
            "client_id": row[1],
            "target_link": row[2],
            "anchor_text": row[3],
            "price": float(row[4]),
            "status": row[5],
            "created_at": str(row[6])
        })

    return jsonify(orders)


if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)