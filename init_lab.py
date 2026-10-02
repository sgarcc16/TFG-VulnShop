import sqlite3

from werkzeug.security import generate_password_hash


connection = sqlite3.connect("vulnshop.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()


# --------------------------------------------------
# Usuarios de laboratorio
# --------------------------------------------------

lab_users = [
    (
        "labadmin",
        "labadmin@vulnshop.local",
        generate_password_hash("Admin123!"),
        "admin"
    ),
    (
        "user1",
        "user1@vulnshop.local",
        generate_password_hash("User1Pass!"),
        "user"
    ),
    (
        "user2",
        "user2@vulnshop.local",
        generate_password_hash("User2Pass!"),
        "user"
    )
]


for username, email, password, role in lab_users:

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user is None:

        cursor.execute(
            """
            INSERT INTO users (
                username,
                email,
                password,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                email,
                password,
                role
            )
        )


connection.commit()


# --------------------------------------------------
# Obtener usuarios
# --------------------------------------------------

cursor.execute(
    """
    SELECT id
    FROM users
    WHERE username = ?
    """,
    ("user1",)
)

user1 = cursor.fetchone()


cursor.execute(
    """
    SELECT id
    FROM users
    WHERE username = ?
    """,
    ("user2",)
)

user2 = cursor.fetchone()


# --------------------------------------------------
# Obtener productos
# --------------------------------------------------

cursor.execute(
    """
    SELECT id, price
    FROM products
    WHERE name = ?
    """,
    ("Teclado mecánico",)
)

keyboard = cursor.fetchone()


cursor.execute(
    """
    SELECT id, price
    FROM products
    WHERE name = ?
    """,
    ("Ratón gaming",)
)

mouse = cursor.fetchone()


# --------------------------------------------------
# Pedido inicial de user1
# --------------------------------------------------

if user1 is not None and keyboard is not None:

    cursor.execute(
        """
        SELECT id
        FROM orders
        WHERE user_id = ?
        LIMIT 1
        """,
        (user1["id"],)
    )

    existing_order = cursor.fetchone()

    if existing_order is None:

        quantity = 1
        total_price = keyboard["price"] * quantity

        cursor.execute(
            """
            INSERT INTO orders (
                user_id,
                product_id,
                quantity,
                total_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user1["id"],
                keyboard["id"],
                quantity,
                total_price
            )
        )

        cursor.execute(
            """
            UPDATE products
            SET stock = stock - ?
            WHERE id = ?
            """,
            (
                quantity,
                keyboard["id"]
            )
        )


# --------------------------------------------------
# Pedido inicial de user2
# --------------------------------------------------

if user2 is not None and mouse is not None:

    cursor.execute(
        """
        SELECT id
        FROM orders
        WHERE user_id = ?
        LIMIT 1
        """,
        (user2["id"],)
    )

    existing_order = cursor.fetchone()

    if existing_order is None:

        quantity = 2
        total_price = mouse["price"] * quantity

        cursor.execute(
            """
            INSERT INTO orders (
                user_id,
                product_id,
                quantity,
                total_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user2["id"],
                mouse["id"],
                quantity,
                total_price
            )
        )

        cursor.execute(
            """
            UPDATE products
            SET stock = stock - ?
            WHERE id = ?
            """,
            (
                quantity,
                mouse["id"]
            )
        )


connection.commit()
connection.close()

print("Datos del laboratorio inicializados correctamente.")