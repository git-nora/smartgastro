"""
SmartGastro - Rutas CRUD
Productos, Ventas, Proveedores y Locaciones
Hernández Andrés
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models import Producto, Venta, DetalleVenta, Proveedor, Locacion
from auth import token_requerido

routes_bp = Blueprint("routes", __name__)


# ─────────────────────────────────────────────
#                  PRODUCTOS
# ─────────────────────────────────────────────

@routes_bp.route("/api/productos", methods=["GET"])
@token_requerido
def get_productos(usuario_actual):
    productos = Producto.query.all()
    resultado = []
    for p in productos:
        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "precio": p.precio,
            "stock": p.stock,
            "stock_minimo": p.stock_minimo,
            "categoria": p.categoria,
            "stock_bajo": p.stock <= p.stock_minimo
        })
    return jsonify(resultado), 200


@routes_bp.route("/api/productos", methods=["POST"])
@token_requerido
def crear_producto(usuario_actual):
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "El body debe ser JSON"}), 400
    if not datos.get("nombre") or not datos.get("categoria"):
        return jsonify({"error": "nombre y categoria son obligatorios"}), 400
    if datos.get("precio") is None or float(datos["precio"]) < 0:
        return jsonify({"error": "precio debe ser mayor o igual a 0"}), 400

    try:
        producto = Producto(
            nombre=datos["nombre"],
            precio=float(datos["precio"]),
            stock=int(datos.get("stock", 0)),
            stock_minimo=int(datos.get("stock_minimo", 5)),
            categoria=datos["categoria"]
        )
        db.session.add(producto)
        db.session.commit()
        return jsonify({"mensaje": "Producto creado", "id": producto.id}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al crear el producto"}), 500


@routes_bp.route("/api/productos/<int:id>", methods=["PUT"])
@token_requerido
def actualizar_producto(usuario_actual, id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({"error": f"Producto {id} no encontrado"}), 404

    datos = request.get_json()
    try:
        if datos.get("nombre"):
            producto.nombre = datos["nombre"]
        if datos.get("precio") is not None:
            producto.precio = float(datos["precio"])
        if datos.get("stock") is not None:
            producto.stock = int(datos["stock"])
        if datos.get("categoria"):
            producto.categoria = datos["categoria"]
        db.session.commit()
        return jsonify({"mensaje": "Producto actualizado"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar el producto"}), 500


@routes_bp.route("/api/productos/<int:id>", methods=["DELETE"])
@token_requerido
def eliminar_producto(usuario_actual, id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({"error": f"Producto {id} no encontrado"}), 404

    try:
        db.session.delete(producto)
        db.session.commit()
        return "", 204
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar el producto"}), 500