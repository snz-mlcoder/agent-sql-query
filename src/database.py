import sqlite3

def create_demo_database(db_path: str):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a sample table
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            country TEXT
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL
        );
        insert into customers (name, email, country) values
        ('John Doe', 'john.doe@example.com', 'USA'),
        ('Jane Smith', 'jane.smith@example.com', 'Canada');

        insert into products (name, category, price) values
        ('Laptop', 'Electronics', 999.99),
        ('Book', 'Education', 19.99);

        insert into orders (customer_id, product_id, quantity, total) values
        (1, 1, 1, 999.99),
        (2, 2, 2, 39.98);

    ''')
    conn.commit()
    conn.close()
