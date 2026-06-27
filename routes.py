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
    
# ─────────────────────────────────────────────
#                    VENTAS
# ─────────────────────────────────────────────

@routes_bp.route("/api/ventas", methods=["GET"])
@token_requerido
def get_ventas(usuario_actual):
    ventas = Venta.query.all()
    resultado = []
    for v in ventas:
        detalles = []
        for d in v.detalles:
            detalles.append({
                "id_producto": d.id_producto,
                "cantidad": d.cantidad,
                "subtotal": d.subtotal
            })
        resultado.append({
            "id": v.id,
            "fecha_hora": v.fecha_hora.strftime("%d/%m/%Y %H:%M"),
            "total": v.total,
            "detalles": detalles
        })
    return jsonify(resultado), 200


@routes_bp.route("/api/ventas", methods=["POST"])
@token_requerido
def crear_venta(usuario_actual):
    datos = request.get_json()

    if not datos or not datos.get("detalles"):
        return jsonify({"error": "Se requiere al menos un producto en la venta"}), 400

    try:
        total = 0
        detalles_objects = []

        for item in datos["detalles"]:
            producto = Producto.query.get(item["id_producto"])
            if not producto:
                return jsonify({"error": f"Producto {item['id_producto']} no encontrado"}), 404
            if producto.stock < item["cantidad"]:
                return jsonify({"error": f"Stock insuficiente para {producto.nombre}"}), 400

            subtotal = producto.precio * item["cantidad"]
            total += subtotal
            producto.stock -= item["cantidad"]

            detalles_objects.append(DetalleVenta(
                id_producto=producto.id,
                cantidad=item["cantidad"],
                subtotal=subtotal
            ))

        venta = Venta(total=total, id_locacion=datos.get("id_locacion"))
        db.session.add(venta)
        db.session.flush()

        for detalle in detalles_objects:
            detalle.id_venta = venta.id
            db.session.add(detalle)

        db.session.commit()
        return jsonify({"mensaje": "Venta registrada", "id": venta.id, "total": total}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al registrar la venta"}), 500


# ─────────────────────────────────────────────
#                 PROVEEDORES
# ─────────────────────────────────────────────

@routes_bp.route("/api/proveedores", methods=["GET"])
@token_requerido
def get_proveedores(usuario_actual):
    proveedores = Proveedor.query.all()
    resultado = []
    for p in proveedores:
        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "contacto": p.contacto,
            "telefono": p.telefono,
            "email": p.email
        })
    return jsonify(resultado), 200


@routes_bp.route("/api/proveedores", methods=["POST"])
@token_requerido
def crear_proveedor(usuario_actual):
    datos = request.get_json()

    if not datos or not datos.get("nombre"):
        return jsonify({"error": "El nombre del proveedor es obligatorio"}), 400

    try:
        proveedor = Proveedor(
            nombre=datos["nombre"],
            contacto=datos.get("contacto"),
            telefono=datos.get("telefono"),
            email=datos.get("email")
        )
        db.session.add(proveedor)
        db.session.commit()
        return jsonify({"mensaje": "Proveedor creado", "id": proveedor.id}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al crear el proveedor"}), 500


@routes_bp.route("/api/proveedores/<int:id>", methods=["DELETE"])
@token_requerido
def eliminar_proveedor(usuario_actual, id):
    proveedor = Proveedor.query.get(id)
    if not proveedor:
        return jsonify({"error": f"Proveedor {id} no encontrado"}), 404

    try:
        db.session.delete(proveedor)
        db.session.commit()
        return "", 204
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar el proveedor"}), 500


# ─────────────────────────────────────────────
#                   LOCACIONES
# ─────────────────────────────────────────────

@routes_bp.route("/api/locaciones", methods=["GET"])
@token_requerido
def get_locaciones(usuario_actual):
    locaciones = Locacion.query.all()
    resultado = []
    for l in locaciones:
        resultado.append({
            "id": l.id,
            "nombre": l.nombre,
            "direccion": l.direccion,
            "fecha": l.fecha.strftime("%d/%m/%Y")
        })
    return jsonify(resultado), 200


@routes_bp.route("/api/locaciones", methods=["POST"])
@token_requerido
def crear_locacion(usuario_actual):
    datos = request.get_json()

    if not datos or not datos.get("nombre") or not datos.get("fecha"):
        return jsonify({"error": "nombre y fecha son obligatorios"}), 400

    try:
        from datetime import datetime
        fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
        locacion = Locacion(
            nombre=datos["nombre"],
            direccion=datos.get("direccion"),
            fecha=fecha
        )
        db.session.add(locacion)
        db.session.commit()
        return jsonify({"mensaje": "Locación creada", "id": locacion.id}), 201
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Usá YYYY-MM-DD"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al crear la locación"}), 500