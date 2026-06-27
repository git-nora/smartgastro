"""
SmartGastro - Aplicacion Web
Segunda Entrega - AyMS 2026
Lassalle Nora - Hernandez Andres
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuracion desde variables de entorno
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Extensiones
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

if __name__ == "__main__":
    print("=" * 50)
    print("  SmartGastro - Servidor Flask")
    print("  URL: http://127.0.0.1:5000")
    print("  Ctrl+C para detener")
    print("=" * 50)
    app.run(debug=True)