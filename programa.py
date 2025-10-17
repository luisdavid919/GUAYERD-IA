# ===============================================
# PROGRAMA: Tienda Aurelion
# Autor: Equipo 11
# Descripción:
#   Programa que muestra información sobre el proyecto Tienda Aurelion.
#   Incluye un menú interactivo con tres secciones:
#   1. Historia, problema y solución
#   2. Estructura de los datos
#   3. Análisis simple con NumPy
# ===============================================

import numpy as np

# ------------------------------------------------
# Funciones de las secciones
# ------------------------------------------------

def mostrar_menu():
    print("\n==============================")
    print("   MENÚ PRINCIPAL - TIENDA AURELION")
    print("==============================")
    print("1. Historia, problema y solución")
    print("2. Estructura de los datos")
    print("3. Análisis con NumPy")
    print("4. Salir")
    print("==============================")

def seccion_1():
    print("\n SECCIÓN 1: HISTORIA, PROBLEMA Y SOLUCIÓN")
    print("Tienda Aurelion es una empresa dedicada a la venta de productos de consumo masivo.")
    print("El crecimiento de su base de clientes y productos generó grandes volúmenes de información,")
    print("dificultando el análisis de ventas y la toma de decisiones.")
    print("El objetivo del proyecto es organizar los datos mediante un modelo relacional,")
    print("permitiendo identificar patrones de compra, optimizar el inventario y mejorar la rentabilidad.\n")

def seccion_2():
    print("\n SECCIÓN 2: ESTRUCTURA DE LOS DATOS, ESCALAS Y RELACIONES")
    print("El modelo relacional de Tienda Aurelion está compuesto por cuatro tablas principales.\n")

    # Tabla: CLIENTES
    print("=== TABLA: CLIENTES ===")
    print("Campos:")
    print("+------------------+-------------+-----------+")
    print("| Campo            | Tipo        | Escala    |")
    print("+------------------+-------------+-----------+")
    print("| id_cliente       | int         | Nominal   |")
    print("| nombre_cliente   | str         | Nominal   |")
    print("| email            | str         | Nominal   |")
    print("| ciudad           | str         | Nominal   |")
    print("| fecha_alta       | date        | Intervalo |")
    print("+------------------+-------------+-----------+")
    print("PK: id_cliente")
    print("FK: (ninguna - tabla maestra para Ventas)\n")

    # Tabla: PRODUCTOS
    print("=== TABLA: PRODUCTOS ===")
    print("Campos:")
    print("+------------------+-------------+-----------+")
    print("| Campo            | Tipo        | Escala    |")
    print("+------------------+-------------+-----------+")
    print("| id_producto      | int         | Nominal   |")
    print("| nombre_producto  | str         | Nominal   |")
    print("| categoria        | str         | Nominal   |")
    print("| precio_unitario  | float       | Razón     |")
    print("+------------------+-------------+-----------+")
    print("PK: id_producto")
    print("FK: (ninguna - tabla maestra para Detalle_Ventas)\n")

    # Tabla: VENTAS
    print("=== TABLA: VENTAS ===")
    print("Campos:")
    print("+------------------+-------------+-----------+")
    print("| Campo            | Tipo        | Escala    |")
    print("+------------------+-------------+-----------+")
    print("| id_venta         | int         | Nominal   |")
    print("| fecha            | date        | Intervalo |")
    print("| id_cliente       | int         | Nominal   |")
    print("| medio_pago       | str         | Nominal   |")
    print("+------------------+-------------+-----------+")
    print("PK: id_venta")
    print("FK: id_cliente → Clientes(id_cliente)\n")

    # Tabla: DETALLE_VENTAS
    print("=== TABLA: DETALLE_VENTAS ===")
    print("Campos:")
    print("+------------------+-------------+-----------+")
    print("| Campo            | Tipo        | Escala    |")
    print("+------------------+-------------+-----------+")
    print("| id_venta         | int         | Nominal   |")
    print("| id_producto      | int         | Nominal   |")
    print("| cantidad         | int         | Razón     |")
    print("| importe          | float       | Razón     |")
    print("+------------------+-------------+-----------+")
    print("PK compuesta: (id_venta, id_producto)")
    print("FK1: id_venta → Ventas(id_venta)")
    print("FK2: id_producto → Productos(id_producto)\n")

    print("Relaciones principales entre tablas:")
    print("Clientes (1) ───< Ventas (N)")
    print("Ventas (1) ───< Detalle_Ventas (N)")
    print("Productos (1) ───< Detalle_Ventas (N)")
    print("\nEsta estructura permite obtener información cruzada sobre clientes, productos y comportamiento de ventas.\n")

def seccion_3():
    print("\nSECCIÓN 3: ANÁLISIS CON NUMPY")
    
    # Simulación de importes de ventas (en pesos)
    importes = np.array([2500, 3200, 4100, 1800, 5000, 2750, 3600])
    print(f"\nImportes: {importes}")

    # Cálculos
    total = np.sum(importes)
    promedio = np.mean(importes)

    print(f"\nTotal de ventas: ${total:.2f}")
    print(f"Promedio de venta: ${promedio:.2f}")

    # Evaluaciones condicionales
    if promedio > 3000:
        print("Promedio de precios: ALTO.")
    else:
        print("Promedio de precios: BAJO.")

    if total > 20000:
        print("Buen nivel de ventas general.")
    else:
        print("Nivel de ventas moderado.")

# ------------------------------------------------
# Ejecución principal
# ------------------------------------------------

def main():
    opcion = 0

    while opcion != 4:
        mostrar_menu()
        opcion = int(input("Seleccione una opción (1-4): "))

        if opcion == 1:
            seccion_1()
        elif opcion == 2:
            seccion_2()
        elif opcion == 3:
            seccion_3()
        elif opcion == 4:
            print("\nGracias por usar el programa Tienda Aurelion. ¡Hasta pronto!")
        else:
            print(" Opción no válida. Intente nuevamente.")

# ------------------------------------------------
# Punto de entrada
# ------------------------------------------------

if __name__ == "__main__":
    main()
