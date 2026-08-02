import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from database import get_connection, init_db

app = Flask(__name__)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
# Set FRONTEND_URL on Railway to your exact Netlify URL, e.g.
#   https://your-site-name.netlify.app
# (no trailing slash). If it's not set, this falls back to "*" (allow any
# origin) so the app still works out of the box - tighten this once your
# Netlify URL is stable.
FRONTEND_URL = os.environ.get("FRONTEND_URL", "*")
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}}, supports_credentials=False)

# Create tables on startup if they don't exist yet (fixes UndefinedTable).
with app.app_context():
    init_db()


def row_or_400(fn):
    """Small helper to keep routes short: run fn, return (result, 400) on error."""
    try:
        return fn(), None
    except KeyError as e:
        return None, (jsonify({"error": f"Missing field: {e}"}), 400)
    except Exception as e:
        return None, (jsonify({"error": str(e)}), 400)


@app.route("/")
def home():
    return "Guest Post Management System Backend Running!"


# ================= CLIENTS =================

@app.route("/clients")
def get_clients():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients ORDER BY client_id")
        rows = cur.fetchall()
        cur.close()
        clients = [
            {**row, "created_at": str(row["created_at"])}
            for row in rows
        ]
        return jsonify(clients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.get_json(silent=True) or {}
    required = ["full_name", "email", "company_name", "phone"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO clients (full_name, email, company_name, phone)
            VALUES (%s, %s, %s, %s)
            """,
            (data["full_name"], data["email"], data["company_name"], data["phone"]),
        )
        conn.commit()
        cur.close()
        return jsonify({"message": "Client Added Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/update-client", methods=["PUT"])
def update_client():
    data = request.get_json(silent=True) or {}
    if not data.get("client_id"):
        return jsonify({"error": "Missing field: client_id"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE clients
            SET full_name=%s, email=%s, company_name=%s, phone=%s
            WHERE client_id=%s
            """,
            (
                data["full_name"],
                data["email"],
                data["company_name"],
                data["phone"],
                data["client_id"],
            ),
        )
        conn.commit()
        cur.close()
        return jsonify({"message": "Client Updated Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/delete-client", methods=["DELETE"])
def delete_client():
    data = request.get_json(silent=True) or {}
    if not data.get("client_id"):
        return jsonify({"error": "Missing field: client_id"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM clients WHERE client_id=%s", (data["client_id"],))
        conn.commit()
        cur.close()
        return jsonify({"message": "Client Deleted Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/search-client/<keyword>")
def search_client(keyword):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM clients
            WHERE full_name ILIKE %s OR email ILIKE %s
            ORDER BY client_id
            """,
            (f"%{keyword}%", f"%{keyword}%"),
        )
        rows = cur.fetchall()
        cur.close()
        clients = [{**row, "created_at": str(row["created_at"])} for row in rows]
        return jsonify(clients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# ================= ORDERS =================

@app.route("/orders")
def get_orders():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders ORDER BY order_id")
        rows = cur.fetchall()
        cur.close()
        orders = [
            {**row, "price": float(row["price"]), "created_at": str(row["created_at"])}
            for row in rows
        ]
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/add-order", methods=["POST"])
def add_order():
    data = request.get_json(silent=True) or {}
    required = ["client_id", "target_link", "anchor_text", "price", "status"]
    missing = [f for f in required if data.get(f) in (None, "")]
    if missing:
        return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

    conn = get_connection()
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
                data["status"],
            ),
        )
        conn.commit()
        cur.close()
        return jsonify({"message": "Order Added Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/update-order", methods=["PUT"])
def update_order():
    data = request.get_json(silent=True) or {}
    if not data.get("order_id"):
        return jsonify({"error": "Missing field: order_id"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE orders
            SET target_link=%s, anchor_text=%s, price=%s, status=%s
            WHERE order_id=%s
            """,
            (
                data["target_link"],
                data["anchor_text"],
                data["price"],
                data["status"],
                data["order_id"],
            ),
        )
        conn.commit()
        cur.close()
        return jsonify({"message": "Order Updated Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/delete-order", methods=["DELETE"])
def delete_order():
    data = request.get_json(silent=True) or {}
    if not data.get("order_id"):
        return jsonify({"error": "Missing field: order_id"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM orders WHERE order_id=%s", (data["order_id"],))
        conn.commit()
        cur.close()
        return jsonify({"message": "Order Deleted Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/search-order/<keyword>")
def search_order(keyword):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM orders
            WHERE CAST(order_id AS TEXT) ILIKE %s
               OR target_link ILIKE %s
               OR status ILIKE %s
            ORDER BY order_id
            """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        )
        rows = cur.fetchall()
        cur.close()
        orders = [
            {**row, "price": float(row["price"]), "created_at": str(row["created_at"])}
            for row in rows
        ]
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# ================= PAYMENTS =================

@app.route("/payments")
def get_payments():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM payments ORDER BY payment_id")
        rows = cur.fetchall()
        cur.close()
        payments = [
            {**row, "amount": float(row["amount"]), "payment_date": str(row["payment_date"])}
            for row in rows
        ]
        return jsonify(payments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/add-payment", methods=["POST"])
def add_payment():
    data = request.get_json(silent=True) or {}
    required = ["client_id", "amount", "payment_status"]
    missing = [f for f in required if data.get(f) in (None, "")]
    if missing:
        return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO payments (client_id, amount, payment_status)
            VALUES (%s, %s, %s)
            """,
            (data["client_id"], data["amount"], data["payment_status"]),
        )
        conn.commit()
        cur.close()
        return jsonify({"message": "Payment Added Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/update-payment", methods=["PUT"])
def update_payment():
    data = request.get_json(silent=True) or {}
    if not data.get("payment_id"):
        return jsonify({"error": "Missing field: payment_id"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE payments
            SET amount=%s, payment_status=%s
            WHERE payment_id=%s
            """,
            (data["amount"], data["payment_status"], data["payment_id"]),
        )
        conn.commit()
        cur.close()
        return jsonify({"message": "Payment Updated Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/delete-payment", methods=["DELETE"])
def delete_payment():
    data = request.get_json(silent=True) or {}
    if not data.get("payment_id"):
        return jsonify({"error": "Missing field: payment_id"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM payments WHERE payment_id=%s", (data["payment_id"],))
        conn.commit()
        cur.close()
        return jsonify({"message": "Payment Deleted Successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/search-payment/<keyword>")
def search_payment(keyword):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM payments
            WHERE CAST(payment_id AS TEXT) ILIKE %s
               OR CAST(client_id AS TEXT) ILIKE %s
               OR payment_status ILIKE %s
            ORDER BY payment_id
            """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        )
        rows = cur.fetchall()
        cur.close()
        payments = [
            {**row, "amount": float(row["amount"]), "payment_date": str(row["payment_date"])}
            for row in rows
        ]
        return jsonify(payments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) AS count FROM clients")
        total_clients = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) AS count FROM orders")
        total_orders = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) AS count FROM payments")
        total_payments = cur.fetchone()["count"]

        cur.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM payments")
        total_revenue = float(cur.fetchone()["total"])

        cur.close()

        return jsonify(
            {
                "total_clients": total_clients,
                "total_orders": total_orders,
                "total_payments": total_payments,
                "total_revenue": total_revenue,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
