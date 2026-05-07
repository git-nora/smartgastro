# 🚚 SmartGastro

> Sistema de gestión integral para foodtrucks. Controlá tu inventario, registrá ventas y gestioná ubicaciones desde un solo lugar.

---

## 📋 Descripción

SmartGastro es un sistema desarrollado en Python orientado a dueños y operadores de foodtrucks que buscan reemplazar el uso de planillas Excel 
y registros en papel por una solución digital simple y accesible.

El proyecto se divide en dos fases:

- **Fase 1 (actual):** Motor lógico en consola con POO
- **Fase 2 (próximamente):** API REST con Flask + interfaz web

---

## 🗂️ Estructura del proyecto

```
smartgastro/
├── smartgastro.py                      # Motor lógico con POO (Fase 1 - consola)
├── app.py                              # Servidor Flask con endpoints REST (Fase 2)
├── SmartGastro_Postman_Collection.json # Colección de pruebas Postman
├── docs/
│   └── SmartGastro_TP.pdf              # Documento completo del TP
└── README.md                           # Este archivo
```

---

## ⚙️ Requisitos

- Python 3.10 o superior
- pip

Instalación de dependencias:

```bash
pip install flask
```

---

## 🖥️ Modo consola (Fase 1)

Ejecutá el motor lógico directamente desde la terminal:

```bash
python smartgastro.py
```

Vas a ver el menú interactivo:

```
=========================================================
  SmartGastro - Sistema de Gestión para Foodtrucks
  🚚 El Rincón del Chef | Ubicación: Feria Palermo - Stand 12
=========================================================
  1. Agregar producto al inventario
  2. Registrar venta
  3. Ver inventario actual
  4. Ver historial de ventas
  0. Salir
─────────────────────────────────────────────────────────
  Seleccioná una opción:
```

---

## 🌐 Modo API REST (Fase 2)

### Levantar el servidor Flask

```bash
python app.py
```

El servidor queda corriendo en `http://127.0.0.1:5000`. Para detenerlo: **Ctrl + C**

### Endpoints disponibles

| Método   | Endpoint              | Descripción                              |
| `GET`    | `/api/productos`      | Lista todos los productos del inventario |
| `POST`   | `/api/productos`      | Agrega un nuevo producto                 |
| `DELETE` | `/api/productos/<id>` | Elimina un producto por ID               |
| `PATCH`  | `/api/pedidos/<id>`   | Actualiza el estado de un pedido         |

### Ejemplos de uso

**GET — Ver todos los productos**
```
GET http://127.0.0.1:5000/api/productos
```
```json
[
  {"id": 1, "nombre": "Hamburguesa Clásica", "precio": 3500.0, "stock": 20},
  {"id": 2, "nombre": "Papas Fritas", "precio": 1500.0, "stock": 30}
]
```

**POST — Agregar un producto**
```
POST http://127.0.0.1:5000/api/productos
Content-Type: application/json
```
```json
{
  "nombre": "Hamburguesa Doble",
  "precio": 4800,
  "stock": 20,
  "categoria": "comida"
}
```
Respuesta: `201 Created`
```json
{"id": 4, "nombre": "Hamburguesa Doble", "precio": 4800.0, "stock": 20}
```

**PATCH — Cambiar estado de un pedido**
```
PATCH http://127.0.0.1:5000/api/pedidos/1
Content-Type: application/json
```
```json
{"estado": "listo"}
```
Estados válidos: `pendiente` · `en_preparacion` · `listo` · `entregado`

**DELETE — Eliminar un producto**
```
DELETE http://127.0.0.1:5000/api/productos/1
```
Respuesta: `204 No Content`

---

## 🧪 Pruebas con Postman

1. Abrí Postman
2. **File > Import** → seleccioná `SmartGastro_Postman_Collection.json`
3. Levantá el servidor con `python app.py`
4. Ejecutá las requests desde la colección importada

---

## 🏗️ Arquitectura y clases

```
Foodtruck
├── Inventario
│   └── Producto (×N)
│       ├── get_id(), get_nombre(), get_precio(), get_stock()
│       ├── agregar_stock(cantidad)
│       └── descontar_stock(cantidad) → bool
└── Venta (×N)
    └── get_subtotal()
```

Todos los atributos son **privados** (`__atributo`) y se acceden mediante getters y setters con validación.

---

## 📐 Modelado (ver PDF para detalle completo)

- **DFD Nivel 0:** 4 entidades externas (Cliente, Operador, Proveedor, API Clima)
- **DFD Nivel 1:** 4 procesos (Gestionar Inventario, Registrar Venta, Generar Reporte, Gestionar Ubicación)
- **DER:** 5 entidades (Foodtruck, Producto, Venta, Detalle\_Venta, Ubicacion)
- **Historias de Usuario:** HU-01 a HU-06 con criterios de aceptación

---

## 📦 Tecnologías

| Tecnología         | Uso                              |
| Python 3.10+       | Lenguaje principal               |
| Flask              | Servidor API REST (Fase 2)       |
| Postman            | Pruebas de endpoints             |
| OpenWeatherMap API | Alertas climáticas (planificado) |

---

## 👥 Equipo


- Integrante 1 — [Lassalle Nora]
- Integrante 2 — [Hernandez Andrés]

---

## 🎓 Información académica

| Campo      | Detalle                            |
| Materia    | Análisis y Metodología de Sistemas |
| Docente    | Juan Sebastián Stenico             |
| Instituto  | Universidad Da Vinci               |
| Año        | 2026                               |
| Entrega    | Trabajo Práctico — Primer Entrega  |
