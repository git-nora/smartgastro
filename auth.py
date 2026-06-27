"""
SmartGastro - Autenticación
Registro, login y protección de rutas con JWT
Lassalle Nora
"""

from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import Usuario
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint("auth", __name__)


def token_requerido(f):
    """Decorador que protege las rutas: verifica que el token JWT sea válido."""
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token no proporcionado"}), 401

        try:
            # El token viene como "Bearer <token>"
            token = token.split(" ")[1]
            datos = jwt.decode(
                token,
                os.getenv("FLASK_SECRET_KEY"),
                algorithms=["HS256"]
            )
            usuario_actual = Usuario.query.get(datos["id"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token expiró, volvé a iniciar sesión"}), 401
        except Exception:
            return jsonify({"error": "Token inválido"}), 401

        return f(usuario_actual, *args, **kwargs)
    return decorador


@auth_bp.route("/api/auth/registro", methods=["POST"])
def registro():
    """Registra un nuevo usuario con contraseña encriptada."""
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "El body debe ser JSON"}), 400
    if not datos.get("username") or not datos.get("email") or not datos.get("password"):
        return jsonify({"error": "username, email y password son obligatorios"}), 400

    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(username=datos["username"]).first():
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400
    if Usuario.query.filter_by(email=datos["email"]).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    try:
        password_hash = bcrypt.generate_password_hash(datos["password"]).decode("utf-8")
        nuevo_usuario = Usuario(
            username=datos["username"],
            email=datos["email"],
            password_hash=password_hash
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": f"Usuario '{datos['username']}' registrado correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al registrar el usuario"}), 500


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """Verifica credenciales y devuelve un token JWT."""
    datos = request.get_json()

    if not datos or not datos.get("username") or not datos.get("password"):
        return jsonify({"error": "username y password son obligatorios"}), 400

    usuario = Usuario.query.filter_by(username=datos["username"]).first()

    if not usuario or not bcrypt.check_password_hash(usuario.password_hash, datos["password"]):
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    # Generar token JWT con expiración de 8 horas
    token = jwt.encode(
        {
            "id": usuario.id,
            "username": usuario.username,
            "exp": datetime.utcnow() + timedelta(hours=8)
        },
        os.getenv("FLASK_SECRET_KEY"),
        algorithm="HS256"
    )

    return jsonify({
        "mensaje": f"Bienvenido, {usuario.username}",
        "token": token
    }), 200