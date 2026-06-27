# 🚚 SmartGastro

> Sistema de gestión integral para foodtrucks. Controlá tu inventario, registrá ventas, gestioná proveedores y recibí alertas climáticas en tiempo real.

---

## 👥 Integrantes

- Lassalle Nora
- Hernández Andrés

---

## 📋 Descripción

SmartGastro es un MVP (Producto Mínimo Viable) desarrollado en Python con Flask, que permite a dueños de foodtrucks gestionar su negocio desde el navegador. El sistema resuelve un problema real: los foodtrucks pierden mercadería cuando llueve y se quedan sin stock en pleno evento. SmartGastro alerta cuando hay pronóstico de lluvia y permite controlar el inventario en tiempo real.

---

## 🗂️ Estructura del proyecto

smartgastro/
├── smartgastro.py        # Motor lógico consola (Primera Entrega)
├── app.py                # Servidor Flask y rutas de vistas
├── auth.py               # Autenticación JWT
├── routes.py             # Endpoints API REST
├── models.py             # Modelos SQLAlchemy
├── extensions.py         # Extensiones Flask (db, bcrypt)
├── clima.py              # Integración API OpenWeatherMap
├── templates/            # Vistas HTML con Jinja
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── productos.html
│   ├── proveedores.html
│   └── locaciones.html
├── static/
│   ├── css/estilos.css
│   └── js/
│       ├── main.js
│       └── productos.js
├── .env.example          # Variables de entorno de ejemplo
├── requirements.txt      # Dependencias del proyecto
└── README.md

---

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/git-nora/smartgastro.git
cd smartgastro
```

### 2. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiá el archivo `.env.example` y renombralo `.env`:

```bash
copy .env.example .env
```

Editá el `.env` con tus valores:

FLASK_SECRET_KEY=tu_clave_secreta
OPENWEATHER_API_KEY=tu_api_key_de_openweathermap
DATABASE_URL=sqlite:///smartgastro.db

### 4. Ejecutar el servidor

```bash
python app.py
```

Abrí el navegador en: `http://127.0.0.1:5000`

---

## 🔑 Credenciales de prueba

|    Campo   |   Valor   |
|            |           |
|  Usuario   |   Nora    |
| Contraseña |  Nora919  |

---

## 🌐 Endpoints API REST

| Método |       Endpoint        |            Descripción             |
|        |                       |                                    |
|  POST  | `/api/auth/registro`  | Registrar nuevo usuario            |
|  POST  |  `/api/auth/login`    | Iniciar sesión y obtener token JWT |
|   GET  |   `/api/productos`    | Listar productos                   |
|  POST  |   `/api/productos`    | Crear producto                     |
|   PUT  | `/api/productos/<id>` | Actualizar producto                |
| DELETE | `/api/productos/<id>` | Eliminar producto                  |
|   GET  |     `/api/ventas`     | Listar ventas                      |
|  POST  |     `/api/ventas`     | Registrar venta                    |
|   GET  |   `/api/proveedores`  | Listar proveedores                 |
|  POST  |   `/api/proveedores`  | Crear proveedor                    |
| DELETE |`/api/proveedores/<id>`| Eliminar proveedor                 |
|   GET  |   `/api/locaciones`   | Listar locaciones                  |
|  POST  |   `/api/locaciones`   | Crear locación                     |
|   GET  |      `/api/clima`     | Consultar clima actual             |

---

## 🛠️ Tecnologías utilizadas

|     Tecnología      |               Uso               |
|                     |                                 |
| Python 3.14.6       | Lenguaje principal              |
| Flask 3.0           | Framework web                   |
| SQLAlchemy          | ORM - Base de datos             |
| SQLite              | Base de datos relacional        |
| bcrypt              | Encriptación de contraseñas     |
| JWT                 | Autenticación por token         |
| Jinja2              | Motor de plantillas HTML        |
| OpenWeatherMap API  | Datos climáticos en tiempo real |
| Git / GitHub        | Control de versiones            |

---

## 🎓 Información académica

|   Campo    |             Detalle                |
|            |                                    |
| Materia    | Análisis y Metodología de Sistemas |
| Docente    | Juan Sebastián Stenico             |
| Instituto  | Universidad Da Vinci               |
| Año        | 2026                               |
| Entrega    | Segunda Entrega — SmartGastro Web  |