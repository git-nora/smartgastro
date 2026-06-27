
"""
SmartGastro - Sistema de Gestión para Foodtrucks
POO y encapsulamiento
Materia: Análisis y Metodología de Sistemas 
Lassalle Nora - Hernández Andrés

"""

# ─────────────────────────────────────────────
#               CLASE: Producto
# ─────────────────────────────────────────────
class Producto:
    """Representa un producto/plato del menú del foodtruck."""

    def __init__(self, id_producto: int, nombre: str, precio: float, stock: int):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock  

    # ── Getters ──────────────────────────────
    def get_id(self) -> int:
        return self.__id_producto

    def get_nombre(self) -> str:
        return self.__nombre

    def get_precio(self) -> float:
        return self.__precio

    def get_stock(self) -> int:
        return self.__stock

    # ── Setters con validación ────────────────
    def set_nombre(self, nombre: str) -> None:
        if not nombre.strip():
            print("  ✗ Error: el nombre no puede estar vacío.")
            return
        self.__nombre = nombre

    def set_precio(self, precio: float) -> None:
        if precio < 0:
            print("  ✗ Error: el precio no puede ser negativo.")
            return
        self.__precio = precio

    def agregar_stock(self, cantidad: int) -> None:
        """Incrementa el stock del producto."""
        if cantidad <= 0:
            print("  ✗ Error: la cantidad a agregar debe ser mayor a 0.")
            return
        self.__stock += cantidad
        print(f"  ✓ Stock actualizado. '{self.__nombre}' ahora tiene {self.__stock} unidades.")

    def descontar_stock(self, cantidad: int) -> bool:

        """
        Descuenta stock al registrar una venta.
        Retorna True si la operación fue exitosa, False si no hay stock suficiente.
        """

        if self.__stock == 0:
            print(f"  ✗ Error: '{self.__nombre}' no tiene stock disponible.")
            return False
        if cantidad > self.__stock:
            print(f"  ✗ Error: stock insuficiente. Disponible: {self.__stock} unidades.")
            return False
        self.__stock -= cantidad
        return True

    def __str__(self) -> str:
        return (f"  ID: {self.__id_producto} | {self.__nombre:<25} "
                f"| Precio: ${self.__precio:>8.2f} | Stock: {self.__stock:>4} uds.")


# ─────────────────────────────────────────────
#                 CLASE: Venta
# ─────────────────────────────────────────────
class Venta:

    """Representa una venta registrada en el sistema."""

    def __init__(self, id_venta: int, producto: Producto, cantidad: int):
        self.__id_venta = id_venta
        self.__nombre_producto = producto.get_nombre()
        self.__cantidad = cantidad
        self.__subtotal = producto.get_precio() * cantidad

    def get_subtotal(self) -> float:
        return self.__subtotal

    def __str__(self) -> str:
        return (f"  Venta #{self.__id_venta} | {self.__nombre_producto:<25} "
                f"| Cant: {self.__cantidad} | Subtotal: ${self.__subtotal:.2f}")


# ─────────────────────────────────────────────
#              CLASE: Inventario
# ─────────────────────────────────────────────
class Inventario:

    """Gestiona los productos del foodtruck."""

    def __init__(self):
        self.__productos: dict[int, Producto] = {}
        self.__ultimo_id = 0

    def agregar_producto(self, nombre: str, precio: float, stock: int) -> Producto:
        """Crea y agrega un nuevo producto al inventario."""
        self.__ultimo_id += 1
        producto = Producto(self.__ultimo_id, nombre, precio, stock)
        self.__productos[self.__ultimo_id] = producto
        print(f"  ✓ Producto '{nombre}' agregado con ID {self.__ultimo_id}.")
        return producto

    def buscar_producto(self, id_producto: int):
        """Busca un producto por ID. Retorna el objeto o None."""
        return self.__productos.get(id_producto, None)

    def mostrar_inventario(self) -> None:
        """Imprime todos los productos del inventario."""
        if not self.__productos:
            print("  (!) El inventario está vacío.")
            return
        print(f"\n  {'ID':<5} {'Nombre':<25} {'Precio':>10} {'Stock':>8}")
        print("  " + "─" * 55)
        for producto in self.__productos.values():
            print(str(producto))
        print("  " + "─" * 55)

    def tiene_productos(self) -> bool:
        return len(self.__productos) > 0


# ─────────────────────────────────────────────
#              CLASE: Foodtruck
# ─────────────────────────────────────────────
class Foodtruck:

    """Entidad principal que agrupa inventario y registro de ventas."""

    def __init__(self, nombre: str, ubicacion: str):
        self.__nombre = nombre
        self.__ubicacion = ubicacion
        self.__inventario = Inventario()
        self.__ventas: list[Venta] = []
        self.__ultimo_id_venta = 0

    def get_nombre(self) -> str:
        return self.__nombre

    def get_ubicacion(self) -> str:
        return self.__ubicacion

    def get_inventario(self) -> Inventario:
        return self.__inventario

    def registrar_venta(self, id_producto: int, cantidad: int) -> None:

        """Registra una venta: busca el producto, valida stock y descuenta."""

        producto = self.__inventario.buscar_producto(id_producto)
        if producto is None:
            print(f"  ✗ Error: no existe un producto con ID {id_producto}.")
            return

        exito = producto.descontar_stock(cantidad)
        if exito:
            self.__ultimo_id_venta += 1
            venta = Venta(self.__ultimo_id_venta, producto, cantidad)
            self.__ventas.append(venta)
            print(f"  ✓ Venta registrada. Subtotal: ${venta.get_subtotal():.2f}")

    def mostrar_ventas(self) -> None:

        """Muestra el historial de ventas y el total acumulado."""

        if not self.__ventas:
            print("  (!) No se han registrado ventas.")
            return
        print(f"\n  {'Detalle de Ventas':^55}")
        print("  " + "─" * 55)
        total = 0.0
        for venta in self.__ventas:
            print(str(venta))
            total += venta.get_subtotal()
        print("  " + "─" * 55)
        print(f"  {'TOTAL RECAUDADO:':>45} ${total:.2f}")

    def __str__(self) -> str:
        return f"🚚 {self.__nombre} | Ubicación: {self.__ubicacion}"


# ─────────────────────────────────────────────
#    FUNCIONES DE MENÚ (entradas del usuario)
# ─────────────────────────────────────────────

def pedir_entero(mensaje: str) -> int:

    """Solicita un entero al usuario con validación de tipo."""

    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  ✗ Ingresá un número entero válido.")


def pedir_float(mensaje: str) -> float:

    """Solicita un número decimal al usuario con validación."""

    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("  ✗ Ingresá un número válido (usá punto para decimales).")


def menu_agregar_producto(ft: Foodtruck) -> None:
    print("\n  ┌─── Agregar Producto ───────────────────────┐")
    nombre = input("  │ Nombre del producto: ").strip()
    if not nombre:
        print("  ✗ El nombre no puede estar vacío.")
        return
    precio = pedir_float("  │ Precio ($): ")
    if precio < 0:
        print("  ✗ El precio no puede ser negativo.")
        return
    stock = pedir_entero("  │ Stock inicial (unidades): ")
    if stock < 0:
        print("  ✗ El stock no puede ser negativo.")
        return
    print("  └────────────────────────────────────────────┘")
    ft.get_inventario().agregar_producto(nombre, precio, stock)


def menu_registrar_venta(ft: Foodtruck) -> None:
    print("\n  ┌─── Registrar Venta ────────────────────────┐")
    if not ft.get_inventario().tiene_productos():
        print("  (!) Primero agregá productos al inventario.")
        return
    ft.get_inventario().mostrar_inventario()
    id_prod = pedir_entero("  │ ID del producto a vender: ")
    cantidad = pedir_entero("  │ Cantidad vendida: ")
    if cantidad <= 0:
        print("  ✗ La cantidad debe ser mayor a 0.")
        return
    print("  └────────────────────────────────────────────┘")
    ft.registrar_venta(id_prod, cantidad)


def imprimir_encabezado(ft: Foodtruck) -> None:
    print("\n" + "═" * 57)
    print(f"  SmartGastro - Sistema de Gestión para Foodtrucks")
    print(f"  {ft}")
    print("═" * 57)


def menu_principal(ft: Foodtruck) -> None:

    """Bucle principal del sistema."""

    while True:
        imprimir_encabezado(ft)
        print("  1. Agregar producto al inventario")
        print("  2. Registrar venta")
        print("  3. Ver inventario actual")
        print("  4. Ver historial de ventas")
        print("  0. Salir")
        print("─" * 57)

        opcion = input("  Seleccioná una opción: ").strip()

        if opcion == "1":
            menu_agregar_producto(ft)
        elif opcion == "2":
            menu_registrar_venta(ft)
        elif opcion == "3":
            print()
            ft.get_inventario().mostrar_inventario()
        elif opcion == "4":
            print()
            ft.mostrar_ventas()
        elif opcion == "0":
            print("\n  ✓ Cerrando SmartGastro. ¡Hasta la próxima!\n")
            break
        else:
            print("  ✗ Opción inválida. Ingresá un número del 0 al 4.")

        input("\n  Presioná Enter para continuar...")


# ─────────────────────────────────────────────
#               PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    
    # Inicialización del foodtruck con datos de ejemplo

    mi_foodtruck = Foodtruck(
        nombre="El Rincón del Chef",
        ubicacion="Feria Palermo - Stand 12"
    )

    # Productos de ejemplo precargados para facilitar la demostración

    inventario = mi_foodtruck.get_inventario()
    inventario.agregar_producto("Hamburguesa Clásica", 3500.0, 20)
    inventario.agregar_producto("Papas Fritas", 1500.0, 30)
    inventario.agregar_producto("Gaseosa 500ml", 800.0, 40)
    inventario.agregar_producto("Hamburguesa Doble", 4800.0, 15)

    print("\n  ✓ Sistema iniciado con productos de ejemplo precargados.")

    # Inicio del menú iterativo

    menu_principal(mi_foodtruck)
