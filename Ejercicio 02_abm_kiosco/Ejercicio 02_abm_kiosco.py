import functools

# Decorador personalizado para loguear las operaciones

def log_operacion(operacion):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n>>> Iniciando operación: {operacion}")
            resultado = func(*args, **kwargs)
            print(f">>> Operación '{operacion}' finalizada exitosamente.")
            return resultado
        return wrapper
    return decorador


class Producto:
    """Representa un producto del kiosco."""

    def __init__(self, codigo_barras, nombre, precio, stock_disponible):
        self._codigo_barras = codigo_barras
        self.nombre = nombre
        self.precio = precio
        self.stock_disponible = stock_disponible

    @property
    def codigo_barras(self):
        return self._codigo_barras

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = valor

    @property
    def stock_disponible(self):
        return self._stock_disponible

    @stock_disponible.setter
    def stock_disponible(self, valor):
        if valor < 0:
            raise ValueError("El stock disponible no puede ser negativo.")
        self._stock_disponible = valor

    def __str__(self):
        return (
            f"[Código: {self._codigo_barras}] {self.nombre} | "
            f"${self.precio:.2f} | Stock: {self.stock_disponible}"
        )


class Inventario:
    """Clase para manejar el inventario del kiosco."""

    def __init__(self):
        self.productos = {}

    @log_operacion("Alta de Producto")
    def alta_producto(self, codigo_barras, nombre, precio, stock_disponible):
        if codigo_barras in self.productos:
            print(f"Error: Ya existe un producto con el código de barras {codigo_barras}.")
            return False

        try:
            nuevo_producto = Producto(codigo_barras, nombre, precio, stock_disponible)
            self.productos[codigo_barras] = nuevo_producto
            print(f"Producto agregado al inventario: {nuevo_producto.nombre}.")
            return True
        except ValueError as e:
            print(f"Error de validación: {e}")
            return False

    @log_operacion("Mostrar Inventario")
    def mostrar_inventario(self):
        if not self.productos:
            print("No hay productos registrados en el inventario por ahora.")
            return

        print("\n--- Inventario del Kiosco ---")
        for producto in self.productos.values():
            print(producto)
        print("-----------------------------")

    @log_operacion("Modificar Stock o Precio")
    def modificar_stock_o_precio(self, codigo_barras, nuevo_precio=None, nuevo_stock=None):
        if codigo_barras not in self.productos:
            print(f"Error: No se encontró un producto con el código de barras {codigo_barras}.")
            return False

        producto = self.productos[codigo_barras]

        try:
            if nuevo_precio is not None:
                producto.precio = nuevo_precio
            if nuevo_stock is not None:
                producto.stock_disponible = nuevo_stock
            print(f"Producto {producto.nombre} actualizado correctamente.")
            return True
        except ValueError as e:
            print(f"Error de validación al actualizar: {e}")
            return False

    @log_operacion("Baja de Producto")
    def baja_producto(self, codigo_barras):
        if codigo_barras in self.productos:
            producto = self.productos.pop(codigo_barras)
            print(f"Producto eliminado del inventario: {producto.nombre}.")
            return True
        else:
            print(f"Error: No se encontró un producto con el código de barras {codigo_barras}.")
            return False


def mostrar_menu():
    print("\n" + "=" * 35)
    print(" 🛒 SISTEMA ABM DE KIOSCO 🛒 ")
    print("=" * 35)
    print("[1] Agregar Producto (Alta)")
    print("[2] Mostrar Inventario (Lectura)")
    print("[3] Modificar Stock o Precio (Modificación)")
    print("[4] Eliminar Producto (Baja)")
    print("[5] Salir")
    print("=" * 35)


def main():
    inventario = Inventario()

    # Cargamos datos de prueba
    inventario.alta_producto("123456", "Gaseosa 500ml", 450.0, 20)
    inventario.alta_producto("789012", "Chocolate", 250.0, 15)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            codigo_barras = input("Ingrese el código de barras del producto: ").strip()
            if codigo_barras in inventario.productos:
                print(f"Error: Ya existe un producto con el código de barras {codigo_barras}.")
                continue

            nombre = input("Ingrese el nombre del producto: ").strip()
            try:
                precio = float(input("Ingrese el precio: "))
                stock_disponible = int(input("Ingrese stock disponible: "))
                inventario.alta_producto(codigo_barras, nombre, precio, stock_disponible)
            except ValueError:
                print("Error: El precio debe ser numérico y el stock debe ser un número entero válido.")

        elif opcion == "2":
            inventario.mostrar_inventario()

        elif opcion == "3":
            codigo_barras = input("Ingrese el código de barras del producto a modificar: ").strip()
            if codigo_barras not in inventario.productos:
                print(f"Error: No se encontró un producto con el código de barras {codigo_barras}.")
                continue

            precio_str = input("Nuevo precio (presione Enter para dejar sin cambios): ").strip()
            stock_str = input("Nuevo stock disponible (presione Enter para dejar sin cambios): ").strip()

            try:
                nuevo_precio = float(precio_str) if precio_str else None
                nuevo_stock = int(stock_str) if stock_str else None
                inventario.modificar_stock_o_precio(codigo_barras, nuevo_precio, nuevo_stock)
            except ValueError:
                print("Error: El precio debe ser numérico y el stock debe ser un número entero válido.")

        elif opcion == "4":
            codigo_barras = input("Ingrese el código de barras del producto a eliminar: ").strip()
            inventario.baja_producto(codigo_barras)

        elif opcion == "5":
            print("Saliendo del sistema... ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, seleccione un número del 1 al 5.")


if __name__ == "__main__":
    main()
