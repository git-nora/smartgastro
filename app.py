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

if __name__ == "__main__":
    print("=" * 50)
    print("  SmartGastro - Servidor Flask")
    print("  URL: http://127.0.0.1:5000")
    print("  Ctrl+C para detener")
    print("=" * 50)
    app.run(debug=True)