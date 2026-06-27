"""
SmartGastro - Aplicación Web
Segunda Entrega - AyMS 2026
Lassalle Nora - Hernández Andrés
"""

from flask import Flask
from extensions import db, bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    from models import Usuario, Producto, Venta, DetalleVenta, Proveedor, Locacion
    db.create_all()
    from auth import auth_bp
    app.register_blueprint(auth_bp)
    from routes import routes_bp
    app.register_blueprint(routes_bp)

    from flask import render_template, redirect, url_for, request, session, flash

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        from extensions import bcrypt
        from models import Usuario
        usuario = Usuario.query.filter_by(username=request.form["username"]).first()
        if usuario and bcrypt.check_password_hash(usuario.password_hash, request.form["password"]):
            import jwt
            from datetime import datetime, timedelta
            token = jwt.encode(
                {"id": usuario.id, "username": usuario.username,
                 "exp": datetime.utcnow() + timedelta(hours=8)},
                os.getenv("FLASK_SECRET_KEY"), algorithm="HS256"
            )
            session["token"] = token
            session["username"] = usuario.username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "token" not in session:
        return redirect(url_for("login"))
    from models import Producto, Venta, Proveedor
    from clima import obtener_clima
    from datetime import date
    clima = obtener_clima("Buenos Aires")
    total_productos = Producto.query.count()
    total_ventas = Venta.query.filter(
        db.func.date(Venta.fecha_hora) == date.today()
    ).count()
    total_proveedores = Proveedor.query.count()
    productos_stock_bajo = Producto.query.filter(
        Producto.stock <= Producto.stock_minimo
    ).all()
    return render_template("dashboard.html",
        clima=clima,
        total_productos=total_productos,
        total_ventas=total_ventas,
        total_proveedores=total_proveedores,
        productos_stock_bajo=productos_stock_bajo
    )

@app.route("/productos")
def vista_productos():
    if "token" not in session:
        return redirect(url_for("login"))
    from models import Producto
    productos = Producto.query.all()
    return render_template("productos.html", productos=productos)

@app.route("/proveedores")
def vista_proveedores():
    if "token" not in session:
        return redirect(url_for("login"))
    from models import Proveedor
    proveedores = Proveedor.query.all()
    return render_template("proveedores.html", proveedores=proveedores)

@app.route("/locaciones")
def vista_locaciones():
    if "token" not in session:
        return redirect(url_for("login"))
    from models import Locacion
    locaciones = Locacion.query.all()
    return render_template("locaciones.html", locaciones=locaciones)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    print("=" * 50)
    print("  SmartGastro - Servidor Flask")
    print("  URL: http://127.0.0.1:5000")
    print("  Ctrl+C para detener")
    print("=" * 50)
    app.run(debug=True)