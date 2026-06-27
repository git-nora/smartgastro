"""
SmartGastro - Modelos de base de datos
Lassalle Nora - Hernández Andrés
"""

from extensions import db
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Usuario {self.username}>"


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    categoria = db.Column(db.String(50), nullable=False)

    ventas = db.relationship("DetalleVenta", backref="producto", lazy=True)

    def __repr__(self):
        return f"<Producto {self.nombre}>"


class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    id_locacion = db.Column(db.Integer, db.ForeignKey("locaciones.id"), nullable=True)

    detalles = db.relationship("DetalleVenta", backref="venta", lazy=True)

    def __repr__(self):
        return f"<Venta #{self.id} - ${self.total}>"


class DetalleVenta(db.Model):
    __tablename__ = "detalle_ventas"

    id = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey("ventas.id"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<DetalleVenta venta={self.id_venta} producto={self.id_producto}>"


class Proveedor(db.Model):
    __tablename__ = "proveedores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"<Proveedor {self.nombre}>"


class Locacion(db.Model):
    __tablename__ = "locaciones"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)
    fecha = db.Column(db.Date, nullable=False)

    ventas = db.relationship("Venta", backref="locacion", lazy=True)

    def __repr__(self):
        return f"<Locacion {self.nombre} - {self.fecha}>"