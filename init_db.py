import sqlite3

connection = sqlite3.connect("vulnshop.db")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        total_price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")

cursor.execute("SELECT COUNT(*) FROM products")
product_count = cursor.fetchone()[0]

if product_count == 0:

    initial_products = [
        (
            "Teclado mecánico",
            "Teclado mecánico RGB para gaming",
            59.99,
            10
        ),
        (
            "Ratón gaming",
            "Ratón óptico con seis botones",
            34.99,
            15
        ),
        (
            "Monitor 24 pulgadas",
            "Monitor Full HD de 24 pulgadas",
            149.99,
            5
        )
    ]

    cursor.executemany(
        """
        INSERT INTO products (
            name,
            description,
            price,
            stock
        )
        VALUES (?, ?, ?, ?)
        """,
        initial_products
    )

connection.commit()
connection.close()

print("Base de datos inicializada correctamente.")