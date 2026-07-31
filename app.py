from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
    host="localhost",
    database="guestpost_db",
    user="postgres",
    password="Laiba@1122"
)


@app.route("/")
def home():
    return "Guest Post Management System Backend Running!"



# ================= LOAD CLIENTS =================

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


# ================= SEARCH CLIENT =================

@app.route("/search-client/<keyword>")
def search_client(keyword):

    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM clients
        WHERE full_name ILIKE %s
           OR email ILIKE %s
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

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
#
# ================= DELETE ORDER =================

@app.route("/delete-order", methods=["DELETE"])
def delete_order():

    data = request.get_json()

    try:

        cur = conn.cursor()

        cur.execute(
            "DELETE FROM orders WHERE order_id=%s",
            (data["order_id"],)
        )

        conn.commit()
        cur.close()

        return jsonify({"message": "Order Deleted Successfully!"})

    except Exception as e:

        conn.rollback()
        return jsonify({"error": str(e)}), 400

# ================= ADD CLIENT =================

@app.route("/add-client", methods=["POST"])
def add_client():

    data = request.get_json()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO clients(full_name,email,company_name,phone)
            VALUES(%s,%s,%s,%s)
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


# ================= UPDATE CLIENT =================

@app.route("/update-client", methods=["PUT"])
def update_client():

    data = request.get_json()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            UPDATE clients
            SET full_name=%s,
                email=%s,
                company_name=%s,
                phone=%s
            WHERE client_id=%s
            """,
            (
                data["full_name"],
                data["email"],
                data["company_name"],
                data["phone"],
                data["client_id"]
            )
        )

        conn.commit()
        cur.close()

        return jsonify({"message": "Client Updated Successfully!"})

    except Exception as e:

        conn.rollback()
        return jsonify({"error": str(e)}), 400


# ================= DELETE CLIENT =================

@app.route("/delete-client", methods=["DELETE"])
def delete_client():

    data = request.get_json()

    try:

        cur = conn.cursor()

        cur.execute(
            "DELETE FROM clients WHERE client_id=%s",
            (data["client_id"],)
        )

        conn.commit()
        cur.close()

        return jsonify({"message": "Client Deleted Successfully!"})

    except Exception as e:

        conn.rollback()
        return jsonify({"error": str(e)}), 400


# ================= ADD ORDER =================

@app.route("/add-order", methods=["POST"])
def add_order():

    data = request.get_json()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO orders(client_id,target_link,anchor_text,price,status)
            VALUES(%s,%s,%s,%s,%s)
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


# ================= LOAD ORDERS =================

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
# ================= SEARCH ORDERS =================

@app.route("/search-order/<keyword>")
def search_order(keyword):

    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM orders
        WHERE CAST(order_id AS TEXT) ILIKE %s
           OR target_link ILIKE %s
           OR status ILIKE %s
        """,
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
    )

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
# ================= UPDATE ORDER =================

@app.route("/update-order", methods=["PUT"])
def update_order():

    data = request.get_json()

    try:

        cur = conn.cursor()
        print(data)

        cur.execute(
    """
    UPDATE orders
    SET target_link=%s,
        anchor_text=%s,
        price=%s,
        status=%s
    WHERE order_id=%s
    """,
    (
        data["target_link"],
        data["anchor_text"],
        data["price"],
        data["status"],
        data["order_id"]
    )
)
        print("Updated Order ID:", data["order_id"])
        print("Rows updated:", cur.rowcount)
        conn.commit()
        cur.close()

        return jsonify({"message": "Order Updated Successfully!"})

    except Exception as e:

        conn.rollback()
        return jsonify({"error": str(e)}), 400

# ================= ADD PAYMENT =================

@app.route("/add-payment", methods=["POST"])
def add_payment():

    data = request.get_json()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO payments(client_id, amount, payment_status)
            VALUES(%s, %s, %s)
            """,
            (
                data["client_id"],
                data["amount"],
                data["payment_status"]
            )
        )

        conn.commit()
        cur.close()

        return jsonify({"message": "Payment Added Successfully!"})

    except Exception as e:

        conn.rollback()
        return jsonify({"error": str(e)}), 400


# ================= LOAD PAYMENTS =================

@app.route("/payments")
def get_payments():

    cur = conn.cursor()

    cur.execute("SELECT * FROM payments")

    rows = cur.fetchall()

    cur.close()

    payments = []

    for row in rows:

        payments.append({

            "payment_id": row[0],
            "client_id": row[1],
            "amount": float(row[2]),
            "payment_status": row[3],
            "payment_date": str(row[4])

        })

    return jsonify(payments)
# ================= SEARCH PAYMENT =================

@app.route("/search-payment/<keyword>")
def search_payment(keyword):

    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM payments
        WHERE CAST(payment_id AS TEXT) ILIKE %s
           OR CAST(client_id AS TEXT) ILIKE %s
           OR payment_status ILIKE %s
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    rows = cur.fetchall()
    cur.close()

    payments = []

    for row in rows:
        payments.append({
            "payment_id": row[0],
            "client_id": row[1],
            "amount": float(row[2]),
            "payment_status": row[3],
            "payment_date": str(row[4])
        })

    return jsonify(payments)
# ================= DELETE PAYMENT =================

@app.route("/delete-payment", methods=["DELETE"])
def delete_payment():

    data = request.get_json()

    try:

        cur = conn.cursor()

        cur.execute(
            "DELETE FROM payments WHERE payment_id=%s",
            (data["payment_id"],)
        )

        conn.commit()
        cur.close()

        return jsonify({"message": "Payment Deleted Successfully!"})

    except Exception as e:

        conn.rollback()
        return jsonify({"error": str(e)}), 400
    # ================= UPDATE PAYMENT =================

@app.route("/update-payment", methods=["PUT"])
def update_payment():

    data = request.get_json()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            UPDATE payments
            SET amount=%s,
                payment_status=%s
            WHERE payment_id=%s
            """,
            (
                data["amount"],
                data["payment_status"],
                data["payment_id"]
            )
        )

        conn.commit()
        cur.close()

        return jsonify({"message": "Payment Updated Successfully!"})

    except Exception as e:

        conn.rollback()
        return jsonify({"error": str(e)}), 400
# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    cur = conn.cursor()

    # Total Clients
    cur.execute("SELECT COUNT(*) FROM clients")
    total_clients = cur.fetchone()[0]

    # Total Orders
    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    # Total Payments
    cur.execute("SELECT COUNT(*) FROM payments")
    total_payments = cur.fetchone()[0]

    # Total Revenue
    cur.execute("SELECT COALESCE(SUM(amount), 0) FROM payments")
    total_revenue = float(cur.fetchone()[0])

    cur.close()

    return jsonify({
        "total_clients": total_clients,
        "total_orders": total_orders,
        "total_payments": total_payments,
        "total_revenue": total_revenue
    })
if __name__ == "__main__":
    app.run(debug=True)