import pandas as pd

# --- Función para mostrar información general ---
def mostrar_informacion_general():
    print("\n=== INFORMACIÓN GENERAL DEL PROYECTO ===")
    print("Este programa lee 4 tablas: clientes, productos, ventas y detalle_ventas.")
    print("Permite visualizar relaciones básicas y validar que los datos se cargan correctamente.\n")

# --- Función para cargar y mostrar info básica de los archivos ---
def cargar_datos():
    try:
        clientes = pd.read_excel("clientes.xlsx")
        productos = pd.read_excel("productos.xlsx")
        ventas = pd.read_excel("ventas.xlsx")
        detalle_ventas = pd.read_excel("detalle_ventas.xlsx")

        print("Datos cargados correctamente ")
        print(f"Clientes: {len(clientes)} filas")
        print(f"Productos: {len(productos)} filas")
        print(f"Ventas: {len(ventas)} filas")
        print(f"Detalle de ventas: {len(detalle_ventas)} filas\n")
        print ("Formato tabla es\n")
        print("""| Tabla | Campo | Tipo de Dato |
|-------|-------|--------------|
| **Clientes** | id_cliente | Nominal (identificador) |
| | nombre_cliente | Nominal |
| | email | Nominal |
| | ciudad | Nominal |
| | fecha_alta | Intervalo (fecha) |
| **Productos** | id_producto | Nominal (identificador) |
| | nombre_producto | Nominal |
| | categoria | Nominal *(u ordinal si existe jerarquía)* |
| | precio_unitario | Razón |
| **Ventas** | id_venta | Nominal (identificador) |
| | fecha | Intervalo (fecha) |
| | id_cliente | Nominal (FK) |
| | medio_pago | Nominal |
| **Detalle_Ventas** | id_venta | Nominal (FK) |
| | id_producto | Nominal (FK) |
| | cantidad | Razón (discreta) |
| | importe | Razón |""")
    except Exception as e:
        print("Error al cargar los archivos:", e)

# --- Menú principal ---
def menu():
    while True:
        print("===== MENÚ PRINCIPAL =====")
        print("1. Acceder a la información general")
        print("2. Cargar y mostrar datos")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_informacion_general()
        elif opcion == "2":
            cargar_datos()
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.\n")

if __name__ == "__main__":
    menu()
