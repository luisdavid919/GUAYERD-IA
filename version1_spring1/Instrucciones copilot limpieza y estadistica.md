1. Manejo de rutas dinámicas
Instrucción:

Asegurar que las rutas de los datasets sean dinámicas y compatibles en diferentes entornos.
Acción realizada:

Implementé el uso de Path de la biblioteca pathlib para manejar rutas dinámicas.
Creé una función find_data_dir para detectar automáticamente la carpeta datos o data en el directorio del proyecto.
2. Visualizaciones
Instrucción:

Crear visualizaciones para:
Los 10 productos más vendidos.
Los 10 clientes con mayor gasto total.
Las 10 ciudades con mayores ventas totales.
Acción realizada:

Implementé la visualización de los 10 productos más vendidos utilizando bibliotecas como pandas y plotly.express.
Pendiente: Visualizaciones para los clientes y las ciudades.
3. Integración en un dashboard
Instrucción:

Integrar las visualizaciones en un dashboard y exportarlo como un archivo HTML.
Acción realizada:

Pendiente: Crear el dashboard y exportarlo.
4. Refactorización para rutas absolutas
Instrucción:

Garantizar que el código funcione con rutas absolutas para mayor confiabilidad.
Acción realizada:

Refactoricé el código para usar Path(__file__).parent en scripts de Python.
En el caso de Jupyter Notebooks, ajusté el código para usar os.getcwd() en lugar de __file__, ya que esta variable no está disponible en notebooks.
5. Corrección de errores
Instrucción:

Resolver errores relacionados con columnas faltantes, estructura de los datasets y manejo de rutas.
Acción realizada:

Ajusté el código para calcular totales dinámicamente y manejar errores de columnas faltantes.
Verifiqué la estructura de los datasets y corregí problemas de compatibilidad.
6. Tareas pendientes
Instrucción:

Completar las siguientes tareas:
Crear visualización para los 10 clientes con mayor gasto total.
Crear visualización para las 10 ciudades con mayores ventas totales.
Integrar las visualizaciones en un dashboard y exportarlo como HTML.


