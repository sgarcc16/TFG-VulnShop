import sqlite3
import hashlib
import base64
import json

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registro", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        connection = sqlite3.connect("vulnshop.db")
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
                """,
                (username, email, password_hash)
            )

            connection.commit()

        except sqlite3.IntegrityError:
            connection.close()
            return "El nombre de usuario o email ya existe."

        connection.close()

        return redirect(url_for("index"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("vulnshop.db")
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("index"))

        return "Usuario o contraseña incorrectos."

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))

@app.route("/perfil")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, username, email, role FROM users WHERE id = ?",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    connection.close()

    return render_template("profile.html", user=user)

@app.route("/productos")
def products():

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, description, price, stock FROM products"
    )

    products = cursor.fetchall()

    connection.close()

    return render_template("products.html", products=products)

@app.route("/producto/<int:product_id>")
def product_detail(product_id):

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, description, price, stock
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    connection.close()

    if product is None:
        return "Producto no encontrado", 404

    return render_template("product.html", product=product)

@app.route("/buscar")
def search():

    query = request.args.get("q", "")

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, description, price, stock
        FROM products
        WHERE name LIKE ? OR description LIKE ?
        """,
        (f"%{query}%", f"%{query}%")
    )

    products = cursor.fetchall()

    connection.close()

    return render_template(
        "search.html",
        products=products,
        query=query
    )

@app.route("/comprar/<int:product_id>", methods=["POST"])
def buy_product(product_id):

    # Comprobar que el usuario ha iniciado sesión
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Obtener la cantidad enviada por el formulario
    try:
        quantity = int(request.form["quantity"])
    except (ValueError, KeyError):
        return "Cantidad no válida", 400

    # La cantidad debe ser mayor que 0
    if quantity <= 0:
        return "Cantidad no válida", 400

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    # Buscar el producto
    cursor.execute(
        """
        SELECT id, name, price, stock
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    # Comprobar que existe
    if product is None:
        connection.close()
        return "Producto no encontrado", 404

    # Comprobar que hay suficiente stock
    if quantity > product["stock"]:
        connection.close()
        return "No hay suficiente stock disponible", 400

    # Calcular el precio en el servidor
    total_price = product["price"] * quantity

    # Crear el pedido
    cursor.execute(
        """
        INSERT INTO orders (user_id, product_id, quantity, total_price)
        VALUES (?, ?, ?, ?)
        """,
        (
            session["user_id"],
            product_id,
            quantity,
            total_price
        )
    )

    # Reducir el stock
    cursor.execute(
        """
        UPDATE products
        SET stock = stock - ?
        WHERE id = ?
        """,
        (quantity, product_id)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("orders"))

@app.route("/pedidos")
def orders():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            orders.id,
            products.name,
            orders.quantity,
            orders.total_price,
            orders.created_at
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE orders.user_id = ?
        ORDER BY orders.created_at DESC
        """,
        (session["user_id"],)
    )

    user_orders = cursor.fetchall()

    connection.close()

    return render_template(
        "orders.html",
        orders=user_orders
    )

@app.route("/pedido/<int:order_id>")
def order_detail(order_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            orders.id,
            orders.user_id,
            products.name,
            orders.quantity,
            orders.total_price,
            orders.created_at
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE orders.id = ?
        AND orders.user_id = ?
        """,
        (order_id, session["user_id"])
    )

    order = cursor.fetchone()

    connection.close()

    if order is None:
        return "Pedido no encontrado", 404

    return render_template(
        "order_detail.html",
        order=order
    )

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Acceso denegado", 403

    return render_template("admin.html")

@app.route("/admin/productos")
def admin_products():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Acceso denegado", 403

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, description, price, stock
        FROM products
        ORDER BY id
        """
    )

    products = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_products.html",
        products=products
    )

@app.route("/admin/productos/nuevo", methods=["GET", "POST"])
def admin_create_product():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Acceso denegado", 403

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]

        try:
            price = float(request.form["price"])
            stock = int(request.form["stock"])
        except ValueError:
            return "Precio o stock no válido", 400

        if price < 0 or stock < 0:
            return "Precio o stock no válido", 400

        connection = sqlite3.connect("vulnshop.db")

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO products (
                name,
                description,
                price,
                stock
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                description,
                price,
                stock
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("admin_products"))

    return render_template("admin_create_product.html")

@app.route("/admin/productos/<int:product_id>/editar", methods=["GET", "POST"])
def admin_edit_product(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Acceso denegado", 403

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, description, price, stock
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:
        connection.close()
        return "Producto no encontrado", 404

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]

        try:
            price = float(request.form["price"])
            stock = int(request.form["stock"])
        except ValueError:
            connection.close()
            return "Precio o stock no válido", 400

        if price < 0 or stock < 0:
            connection.close()
            return "Precio o stock no válido", 400

        cursor.execute(
            """
            UPDATE products
            SET name = ?,
                description = ?,
                price = ?,
                stock = ?
            WHERE id = ?
            """,
            (
                name,
                description,
                price,
                stock,
                product_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("admin_products"))

    connection.close()

    return render_template(
        "admin_edit_product.html",
        product=product
    )

@app.route("/admin/productos/<int:product_id>/eliminar", methods=["POST"])
def admin_delete_product(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Acceso denegado", 403

    connection = sqlite3.connect("vulnshop.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:
        connection.close()
        return "Producto no encontrado", 404

    cursor.execute(
        """
        DELETE FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("admin_products"))

@app.route("/admin/usuarios")
def admin_users():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Acceso denegado", 403

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, email, role
        FROM users
        ORDER BY id
        """
    )

    users = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_users.html",
        users=users
    )

@app.route("/admin/usuarios/<int:user_id>/rol", methods=["POST"])
def admin_change_role(user_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Acceso denegado", 403

    new_role = request.form.get("role")

    if new_role not in ["user", "admin"]:
        return "Rol no válido", 400

    # Evitar que el administrador cambie su propio rol
    if user_id == session["user_id"]:
        return "No puedes modificar tu propio rol", 400

    connection = sqlite3.connect("vulnshop.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:
        connection.close()
        return "Usuario no encontrado", 404

    cursor.execute(
        """
        UPDATE users
        SET role = ?
        WHERE id = ?
        """,
        (new_role, user_id)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("admin_users"))

@app.route("/lab/sqli")
def vulnerable_search():

    query = request.args.get("q", "")

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    sql = f"""
        SELECT id, name, description, price, stock
        FROM products
        WHERE name LIKE '%{query}%'
        OR description LIKE '%{query}%'
    """

    try:
        cursor.execute(sql)
        products = cursor.fetchall()

    except sqlite3.Error as error:
        connection.close()
        return f"Error SQL: {error}", 500

    connection.close()

    return render_template(
        "vulnerable_search.html",
        products=products,
        query=query
    )

@app.route("/lab/idor/pedido/<int:order_id>")
def vulnerable_order_detail(order_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            orders.id,
            orders.user_id,
            products.name,
            orders.quantity,
            orders.total_price,
            orders.created_at
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE orders.id = ?
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    connection.close()

    if order is None:
        return "Pedido no encontrado", 404

    return render_template(
        "vulnerable_order_detail.html",
        order=order
    )

@app.route("/lab/config")
def vulnerable_config():

    config_info = {
        "environment": "development",
        "debug": True,
        "database": "vulnshop.db",
        "secret_key": app.secret_key,
        "framework": "Flask"
    }

    return config_info

@app.route("/lab/crypto/register", methods=["GET", "POST"])
def vulnerable_crypto_register():

    message = None

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return "Usuario y contraseña obligatorios", 400

        weak_hash = hashlib.md5(
            password.encode("utf-8")
        ).hexdigest()

        connection = sqlite3.connect("vulnshop.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lab_users_weak_crypto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )

        try:

            cursor.execute(
                """
                INSERT INTO lab_users_weak_crypto (
                    username,
                    password_hash
                )
                VALUES (?, ?)
                """,
                (username, weak_hash)
            )

            connection.commit()

            message = "Usuario de laboratorio registrado correctamente."

        except sqlite3.IntegrityError:

            connection.close()

            return "El usuario ya existe", 400

        connection.close()

    return render_template(
        "vulnerable_crypto_register.html",
        message=message
    )

@app.route(
    "/lab/insecure-design/producto/<int:product_id>",
    methods=["GET", "POST"]
)
def vulnerable_purchase(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("vulnshop.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, description, price, stock
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:
        connection.close()
        return "Producto no encontrado", 404

    if request.method == "POST":

        try:
            quantity = int(request.form["quantity"])
            client_price = float(request.form["unit_price"])

        except (ValueError, KeyError):
            connection.close()
            return "Datos no válidos", 400

        if quantity <= 0:
            connection.close()
            return "Cantidad no válida", 400

        if quantity > product["stock"]:
            connection.close()
            return "No hay suficiente stock disponible", 400

        total_price = client_price * quantity

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
                session["user_id"],
                product_id,
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
            (quantity, product_id)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("orders"))

    connection.close()

    return render_template(
        "vulnerable_purchase.html",
        product=product
    )

@app.route("/lab/auth/login", methods=["GET", "POST"])
def vulnerable_auth_login():

    message = None

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        connection = sqlite3.connect("vulnshop.db")
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, username, password, role
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        connection.close()

        if user is None:

            message = "El usuario no existe."

        elif not check_password_hash(
            user["password"],
            password
        ):

            message = "La contraseña es incorrecta."

        else:

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("index"))

    return render_template(
        "vulnerable_auth_login.html",
        message=message
    )

@app.route("/lab/integrity", methods=["GET", "POST"])
def vulnerable_integrity():

    coupon_data = {
        "campaign": "WELCOME",
        "discount": 10
    }

    default_token = base64.urlsafe_b64encode(
        json.dumps(coupon_data).encode("utf-8")
    ).decode("utf-8")

    result = None

    if request.method == "POST":

        token = request.form.get("coupon_token", "")

        try:

            decoded_data = base64.urlsafe_b64decode(
                token.encode("utf-8")
            ).decode("utf-8")

            coupon = json.loads(decoded_data)

            discount = coupon["discount"]
            campaign = coupon["campaign"]

            result = (
                f"Cupón {campaign} aceptado. "
                f"Descuento aplicado: {discount}%"
            )

        except Exception:

            result = "Cupón no válido."

    return render_template(
        "vulnerable_integrity.html",
        token=default_token,
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)