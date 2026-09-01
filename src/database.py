import sqlite3

DATABASE_PATH = "data/database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    connection.commit()
    connection.close()


def insert_sample_data():
    connection = get_connection()
    cursor = connection.cursor()

    customers = [
        (1, "Rahul", "Mumbai"),
        (2, "Priya", "Pune"),
        (3, "Amit", "Delhi"),
        (4, "Sneha", "Bangalore"),
        (5, "Arjun", "Mumbai")
    ]

    cursor.executemany("""
        INSERT INTO customers (customer_id, name, city)
        VALUES (?, ?, ?)
    """, customers)

    products = [
        (1, "Laptop", "Electronics", 60000),
        (2, "Headphones", "Electronics", 3000),
        (3, "Keyboard", "Electronics", 2000),
        (4, "Shoes", "Fashion", 2500),
        (5, "Backpack", "Fashion", 1500)
    ]

    cursor.executemany("""
        INSERT INTO products (product_id, product_name, category, price)
        VALUES (?, ?, ?, ?)
    """, products)

    orders = [
        (101, 1, "2026-08-01", 63000),
        (102, 2, "2026-08-02", 5500),
        (103, 1, "2026-08-05", 4000),
        (104, 3, "2026-08-07", 62500),
        (105, 4, "2026-08-10", 8500),
        (106, 5, "2026-08-12", 7500)
    ]

    cursor.executemany("""
        INSERT INTO orders (order_id, customer_id, order_date, total_amount)
        VALUES (?, ?, ?, ?)
    """, orders)

    order_items = [
        (101, 1, 1, 60000),
        (101, 2, 1, 3000),
        (102, 2, 1, 3000),
        (102, 3, 1, 2000),
        (102, 5, 1, 500),
        (103, 4, 1, 2500),
        (103, 5, 1, 1500),
        (104, 1, 1, 60000),
        (104, 3, 1, 2000),
        (104, 2, 1, 500),
        (105, 4, 2, 2500),
        (105, 5, 1, 1500),
        (106, 2, 2, 3000),
        (106, 5, 1, 1500)
    ]

    cursor.executemany("""
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    """, order_items)

    connection.commit()
    connection.close()

    print("Sample data inserted successfully!")

def execute_query(sql):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sql)

        results = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        return column_names, results

    finally:
        connection.close

def execute_write_query(sql):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(sql)

    conn.commit()

    conn.close()

def execute_schema_query(sql):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(sql)

    connection.commit()
    connection.close()

def get_database_schema():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    schema = {}

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = cursor.fetchall()

        schema[table_name] = [
            column[1]
            for column in columns
        ]

    connection.close()

    return schema