
import sqlite3

DATABASE = "products.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    if count == 0:
        sample_products = [
            ("Laptop", "Dell laptop", 55000, 10),
            ("Smartphone", "Samsung smartphone", 25000, 20),
            ("Headphones", "Wireless headphones", 3000, 15)
        ]

        conn.executemany("""
            INSERT INTO products (name, description, price, stock)
            VALUES (?, ?, ?, ?)
        """, sample_products)

    conn.commit()
    conn.close()


def get_all_products():
    conn = get_connection()

    products = conn.execute(
        "SELECT * FROM products"
    ).fetchall()

    conn.close()

    return [dict(product) for product in products]


def get_product(product_id):
    conn = get_connection()

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    conn.close()

    return dict(product) if product else None


def add_product(name, description, price, stock):
    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO products (name, description, price, stock)
        VALUES (?, ?, ?, ?)
    """, (name, description, price, stock))

    conn.commit()
    product_id = cursor.lastrowid
    conn.close()

    return get_product(product_id)
