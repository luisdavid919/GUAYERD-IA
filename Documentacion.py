print ("Bienvenido a la Documentación del Sistema de minisúper 'DIA'")
print ("***Por favor seleccione una opción a consultar, ingresando la letra correspondiente***")
valor = input(print("A. TEMA, PROBLEMA, SOLUCIÓN\nB. DATASET DE REFERENCIA\nC. INFORMACIÓN, PASOS Y PSEUDOCODIGO, DIAGRAMA DEL PROGRAMA"))
if valor == "A":
    print("""# TEMA A
    **Tenemos una tienda llamada "DÍA" operando como minisúper que comenzó a operar en enero de 2023, en Argentina. Para hacer crecer nuestro negocio, comenzamos a registrar a cada cliente que nos visitaba y su crecimiento** """)
elif valor == "B":
    print("Usted ha seleccionado la opción B.")
elif valor == "C":
    print("Usted ha seleccionado la opción C.")
else:
    print("Opción no válida.")
