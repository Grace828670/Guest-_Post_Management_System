import os
import psycopg2
from psycopg2.extras import RealDictCursor

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------
# Railway/Neon expose the connection string in the DATABASE_URL environment
# variable. NEVER hardcode host/user/password here - that only works on your
# own laptop and is exactly why the deployed backend was failing.
#
# On Railway, set DATABASE_URL in the service's "Variables" tab to the
# connection string Neon gives you (Neon dashboard -> Connection Details ->
# "Pooled connection"). It looks like:
#   postgresql://user:password@ep-xxxx-pooler.region.aws.neon.tech/dbname?sslmode=require

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "Add it in Railway -> your service -> Variables, using the Neon "
        "'pooled connection' string (see README)."
    )

# Neon requires SSL. If the connection string doesn't already specify it,
# force it here so this works even if someone forgets sslmode in the URL.
if "sslmode" not in DATABASE_URL:
    separator = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL = f"{DATABASE_URL}{separator}sslmode=require"


def get_connection():
    """
    Open a brand-new connection for a single request.

    Serverless Postgres providers like Neon close idle connections, and a
    single long-lived global connection (the original bug in this project)
    will eventually throw 'connection already closed' errors. Opening a
    short-lived connection per request is the simplest reliable fix for a
    small app like this.
    """
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
# This is the actual cause of:
#   psycopg2.errors.UndefinedTable: relation "clients" does not exist
# Neon gives you an empty database - nothing creates the tables for you.
# init_db() below creates them (if they don't already exist) every time the
# app starts, so a fresh Neon database will always be ready to use.

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS clients (
    client_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
    target_link TEXT,
    anchor_text VARCHAR(255),
    price NUMERIC(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL DEFAULT 0,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'unpaid',
    payment_date TIMESTAMP NOT NULL DEFAULT NOW()
);
"""


def init_db():
    """Create all tables if they don't exist yet. Safe to call every startup."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLES_SQL)
        conn.commit()
        cur.close()
        print("Database tables verified/created successfully.")
    except Exception as e:
        conn.rollback()
        print("Error creating tables:", e)
        raise
    finally:
        conn.close()
