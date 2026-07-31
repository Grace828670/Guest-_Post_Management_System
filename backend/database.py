import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="guestpost_db",
        user="postgres",
        password="Laiba@1122"
    )

    print("Database Connected Successfully!")

except Exception as e:
    print("Connection Error:", e)
    