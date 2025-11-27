# ===============================================
# PROGRAMA: Tienda Aurelion
# Autor: Equipo 11
# Descripción:
#   Programa que muestra información sobre el proyecto Tienda Aurelion.
#   Incluye un menú interactivo con:
#   1. Historia, problema y solución
#   2. Estructura de los datos
#   3. Análisis simple con NumPy
#   4. Limpieza y análisis de datos (Sprint 2)
#   5. Estadísticas descriptivas (Sprint 2)
#   6. Entrenar modelos (dataset original)
#   7. Entrenar modelos (dataset aumentado)
#   8. Salir
# ===============================================

import os
import numpy as np
import subprocess
import sys

# Carpeta donde está este archivo programa.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------
# Funciones de las secciones "teóricas"
# ------------------------------------------------

def seccion_1():
    """
    Historia, problema y solución de la Tienda Aurelion.
    Solo imprime texto explicativo para la demo.
    """
    print("\n==============================")
    print(" 1. HISTORIA, PROBLEMA Y SOLUCIÓN")
    print("==============================\n")

    print("La Tienda Aurelion es un comercio minorista que vende productos")
    print("de consumo masivo. Cuenta con un registro histórico de ventas,")
    print("clientes y productos, pero esos datos estaban subutilizados.\n")

    print("PROBLEMA:")
    print("- No se analizaban los tickets de venta de forma sistemática.")
    print("- No se identificaban fácilmente los clientes y tickets de alto valor.")
    print("- Faltaban herramientas para tomar decisiones basadas en datos.\n")

    print("SOLUCIÓN PROPUESTA:")
    print("- Realizar un proceso de limpieza y análisis de los datos.")
    print("- Construir un dataframe a nivel ticket que permita estudiar el 'ticket alto'.")
    print("- Aplicar técnicas de Machine Learning para clasificar tickets de alto valor.")
    print("- Desarrollar dashboards y reportes para apoyar la toma de decisiones.\n")

    input("Presione ENTER para volver al menú...")


def seccion_2():
    """
    Estructura de los datos.
    Describe brevemente las tablas usadas en el proyecto.
    """
    print("\n==============================")
    print(" 2. ESTRUCTURA DE LOS DATOS")
    print("==============================\n")

    print("El proyecto utiliza cuatro tablas principales:\n")

    print("1) CLIENTES")
    print("   - id_cliente")
    print("   - nombre_cliente")
    print("   - email")
    print("   - ciudad")
    print("   - fecha_alta\n")

    print("2) PRODUCTOS")
    print("   - id_producto")
    print("   - nombre_producto")
    print("   - categoria")
    print("   - precio_unitario\n")

    print("3) VENTAS")
    print("   - id_venta")
    print("   - id_cliente")
    print("   - fecha")
    print("   - nombre_cliente (redundante, para análisis)")
    print("   - email (redundante, para análisis)")
    print("   - medio_pago\n")

    print("4) DETALLE_VENTAS")
    print("   - id_venta")
    print("   - id_producto")
    print("   - nombre_producto")
    print("   - cantidad")
    print("   - precio_unitario")
    print("   - importe\n")

    print("A partir de estas tablas se construye un dataframe a nivel ticket,")
    print("que permite estudiar el importe total por venta y definir si un ticket")
    print("es alto o no (variable objetivo 'ticket_alto').\n")

    input("Presione ENTER para volver al menú...")


def seccion_3():
    """
    Análisis simple con NumPy.
    Hace un ejemplo sencillo con montos de tickets.
    """
    print("\n==============================")
    print(" 3. ANÁLISIS SIMPLE CON NUMPY")
    print("==============================\n")

    # Ejemplo de montos de tickets (simulados)
    tickets = np.array([2500, 3200, 1800, 5200, 4300, 2900, 6100, 1500, 3800, 4700])
    print(f"Montos de tickets de ejemplo: {tickets}\n")

    print(f"▶ Promedio de ticket:        {tickets.mean():.2f}")
    print(f"▶ Mediana de ticket:         {np.median(tickets):.2f}")
    print(f"▶ Desvío estándar:           {tickets.std(ddof=1):.2f}")
    print(f"▶ Ticket mínimo:             {tickets.min():.2f}")
    print(f"▶ Ticket máximo:             {tickets.max():.2f}\n")

    # Ejemplo de umbral de ticket alto
    umbral = np.percentile(tickets, 75)
    print(f"Umbral de 'ticket alto' (percentil 75): {umbral:.2f}")
    print(f"Tickets considerados altos: {tickets[tickets >= umbral]}\n")

    input("Presione ENTER para volver al menú...")


# ------------------------------------------------
# Menú principal
# ------------------------------------------------

def mostrar_menu():
    print("\n==============================")
    print("   MENÚ PRINCIPAL - TIENDA AURELION")
    print("==============================")
    print("1. Historia, problema y solución")
    print("2. Estructura de los datos")
    print("3. Análisis con NumPy")
    print("4. Limpieza y Análisis (Sprint2)")
    print("5. Estadísticas Descriptivas (Sprint2)")
    print("6. Entrenar modelos (dataset original)")
    print("7. Entrenar modelos (dataset aumentado)")
    print("8. Salir")
    print("==============================")


def main():
    opcion = 0

    while opcion != 8:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opción (1-8): "))
        except ValueError:
            print("Por favor ingrese un número del 1 al 8.")
            continue

        if opcion == 1:
            seccion_1()
        elif opcion == 2:
            seccion_2()
        elif opcion == 3:
            seccion_3()
        elif opcion == 4:
            # Limpieza y análisis de los Excel originales
            ruta_script = os.path.join(SCRIPT_DIR, "limpieza-analisis_corregido.py")
            subprocess.run([sys.executable, ruta_script])
        elif opcion == 5:
            # Estadísticas descriptivas + distribuciones + correlaciones
            ruta_script = os.path.join(SCRIPT_DIR, "Estadisticas_corregido.py")
            subprocess.run([sys.executable, ruta_script])
        elif opcion == 6:
            # Entrenar modelos con el dataset original
            ruta_script = os.path.join(SCRIPT_DIR, "ModeloML.py")
            subprocess.run([sys.executable, ruta_script])
        elif opcion == 7:
            # Entrenar modelos con el dataset aumentado
            ruta_script = os.path.join(SCRIPT_DIR, "ModeloMLAumentado.py")
            subprocess.run([sys.executable, ruta_script])
        elif opcion == 8:
            print("\nGracias por usar el programa Tienda Aurelion. ¡Hasta pronto!")
        else:
            print("Opción no válida. Intente nuevamente.")


# ------------------------------------------------
# Punto de entrada
# ------------------------------------------------

if __name__ == "__main__":
    main()
