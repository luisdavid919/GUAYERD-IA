import os
import sys
import subprocess
import numpy as np
from flask import Flask, render_template_string

app = Flask(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_FIGURAS = os.path.join(SCRIPT_DIR, "static", "figuras")


# =====================================================
# Ejecutar scripts hijo (UTF-8)
# =====================================================
def ejecutar_script(nombre_archivo: str) -> str:
    ruta = os.path.join(SCRIPT_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return f"No se encontró el archivo: {ruta}"

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    resultado = subprocess.run(
        [sys.executable, ruta],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )

    salida = resultado.stdout
    if resultado.stderr:
        salida += "\n\n[STDERR]\n" + resultado.stderr
    return salida


# =====================================================
# Plantilla base HTML
# =====================================================
BASE_HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Tienda Aurelion - {{ titulo }}</title>
  <style>
    body {
        font-family: Arial, Helvetica, sans-serif;
        margin: 0;
        padding: 0;
        background: #f5f5f5;
    }
    header {
        background: #1f2937;
        color: #ffffff;
        padding: 1rem 2rem;
    }
    header h1 {
        margin: 0;
        font-size: 1.6rem;
    }
    nav {
        background: #111827;
        padding: 0.5rem 2rem;
    }
    nav a {
        color: #e5e7eb;
        margin-right: 1rem;
        text-decoration: none;
        font-size: 0.95rem;
    }
    nav a:hover {
        text-decoration: underline;
    }
    .card {
        background: #ffffff;
        border-radius: 8px;
        padding: 1.5rem 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin: 1.5rem 2rem;
    }
    pre {
        background: #111827;
        color: #e5e7eb;
        padding: 1rem;
        border-radius: 6px;
        overflow-x: auto;
        font-size: 0.85rem;
    }
    img {
        max-width: 100%;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 0 5px rgba(0,0,0,0.2);
    }
  </style>
</head>
<body>
  <header>
    <h1>Tienda Aurelion - Dashboard</h1>
  </header>

  <nav>
    <a href="{{ url_for('index') }}">Inicio</a>
    <a href="{{ url_for('historia') }}">Historia</a>
    <a href="{{ url_for('estructura') }}">Estructura</a>
    <a href="{{ url_for('numpy_demo') }}">NumPy</a>
    <a href="{{ url_for('limpieza') }}">Limpieza</a>
    <a href="{{ url_for('estadisticas') }}">Estadísticas</a>
    <a href="{{ url_for('modelo_original') }}">Modelo Original</a>
    <a href="{{ url_for('modelo_aumentado') }}">Modelo Aumentado</a>
  </nav>

  <div class="card">
    {{ contenido | safe }}
  </div>
</body>
</html>
"""


def render_pagina(titulo: str, contenido_html: str):
    return render_template_string(BASE_HTML, titulo=titulo, contenido=contenido_html)


# =====================================================
# RUTAS “TEÓRICAS”
# =====================================================
@app.route("/")
def index():
    html = """
    <h2>Bienvenido al Dashboard de la Tienda Aurelion</h2>
    <p>
      Desde aquí podés navegar por toda la historia del proyecto, ver la estructura
      de los datos, un ejemplo de análisis con NumPy, y ejecutar los scripts de
      limpieza, estadísticas y modelos de Machine Learning.
    </p>
    <p>
      Las figuras de Estadísticas y de los modelos se muestran <strong>dentro de esta web</strong>
      como imágenes, para que no tengas que ir cerrando ventanas de Matplotlib.
    </p>
    """
    return render_pagina("Inicio", html)


@app.route("/historia")
def historia():
    html = """
    <h2>Historia, problema y solución</h2>
    <p>
      La <strong>Tienda Aurelion</strong> es un comercio minorista que vende productos
      de consumo masivo. Cuenta con un registro histórico de ventas, clientes
      y productos, pero esos datos estaban subutilizados.
    </p>
    <h3>Problema</h3>
    <ul>
      <li>No se analizaban los tickets de venta de forma sistemática.</li>
      <li>No se identificaban fácilmente los clientes y tickets de alto valor.</li>
      <li>Faltaban herramientas para tomar decisiones basadas en datos.</li>
    </ul>
    <h3>Solución propuesta</h3>
    <ul>
      <li>Procesos de limpieza y análisis de los datos.</li>
      <li>Construcción de un dataframe a nivel ticket para estudiar el
          <strong>ticket alto</strong>.</li>
      <li>Aplicar técnicas de <strong>Machine Learning</strong> para clasificar
          tickets de alto valor.</li>
      <li>Dashboards y reportes que apoyen la toma de decisiones.</li>
    </ul>
    """
    return render_pagina("Historia", html)


@app.route("/estructura")
def estructura():
    html = """
    <h2>Estructura de los datos</h2>
    <p>El proyecto utiliza cuatro tablas principales:</p>
    <h3>1) CLIENTES</h3>
    <ul>
      <li>id_cliente</li>
      <li>nombre_cliente</li>
      <li>email</li>
      <li>ciudad</li>
      <li>fecha_alta</li>
    </ul>
    <h3>2) PRODUCTOS</h3>
    <ul>
      <li>id_producto</li>
      <li>nombre_producto</li>
      <li>categoria</li>
      <li>precio_unitario</li>
    </ul>
    <h3>3) VENTAS</h3>
    <ul>
      <li>id_venta</li>
      <li>id_cliente</li>
      <li>fecha</li>
      <li>nombre_cliente</li>
      <li>email</li>
      <li>medio_pago</li>
    </ul>
    <h3>4) DETALLE_VENTAS</h3>
    <ul>
      <li>id_venta</li>
      <li>id_producto</li>
      <li>nombre_producto</li>
      <li>cantidad</li>
      <li>precio_unitario</li>
      <li>importe</li>
    </ul>
    """
    return render_pagina("Estructura de datos", html)


@app.route("/numpy")
def numpy_demo():
    tickets = np.array([2500, 3200, 1800, 5200, 4300, 2900, 6100, 1500, 3800, 4700])
    prom = tickets.mean()
    med = float(np.median(tickets))
    std = tickets.std(ddof=1)
    minimo = tickets.min()
    maximo = tickets.max()
    umbral = float(np.percentile(tickets, 75))
    altos = tickets[tickets >= umbral]

    texto = [
        f"Montos de tickets de ejemplo: {tickets}",
        "",
        f"Promedio de ticket:  {prom:.2f}",
        f"Mediana de ticket:   {med:.2f}",
        f"Desvío estándar:     {std:.2f}",
        f"Ticket mínimo:       {minimo:.2f}",
        f"Ticket máximo:       {maximo:.2f}",
        "",
        f"Umbral de 'ticket alto' (p75): {umbral:.2f}",
        f"Tickets considerados altos: {altos}",
    ]
    salida = "\n".join(texto)

    html = f"""
    <h2>Análisis simple con NumPy</h2>
    <p>Ejemplo de cálculo de métricas sobre montos de tickets:</p>
    <pre>{salida}</pre>
    """
    return render_pagina("NumPy", html)


# =====================================================
# RUTAS QUE EJECUTAN SCRIPTS
# =====================================================
@app.route("/limpieza")
def limpieza():
    salida = ejecutar_script("limpieza-analisis_corregido.py")
    html = f"""
    <h2>Limpieza y análisis (Sprint 2)</h2>
    <p>Salida del script <code>limpieza-analisis_corregido.py</code>:</p>
    <pre>{salida}</pre>
    <p>Los CSV limpios se generan en la carpeta <strong>datos/limpios</strong>.</p>
    """
    return render_pagina("Limpieza", html)


@app.route("/estadisticas")
def estadisticas():
    salida = ejecutar_script("Estadisticas_corregido.py")

    figuras = []
    if os.path.isdir(CARPETA_FIGURAS):
        for f in sorted(os.listdir(CARPETA_FIGURAS)):
            if f.startswith("estadisticas_") and f.lower().endswith(".png"):
                figuras.append(f)

    html_imgs = "".join(
        f'<img src="/static/figuras/{f}" alt="{f}">' for f in figuras
    )

    html = f"""
    <h2>Estadísticas descriptivas (Sprint 2)</h2>
    <p>Salida del script <code>Estadisticas_corregido.py</code>:</p>
    <pre>{salida}</pre>
    <h3>Figuras generadas</h3>
    {html_imgs or "<p>No se encontraron figuras (revisá la carpeta static/figuras).</p>"}
    """
    return render_pagina("Estadísticas", html)


@app.route("/modelo_original")
def modelo_original():
    salida = ejecutar_script("ModeloML.py")

    figuras = []
    if os.path.isdir(CARPETA_FIGURAS):
        for f in sorted(os.listdir(CARPETA_FIGURAS)):
            if f.startswith("modelo_original_") and f.lower().endswith(".png"):
                figuras.append(f)

    html_imgs = "".join(
        f'<img src="/static/figuras/{f}" alt="{f}">' for f in figuras
    )

    html = f"""
    <h2>Modelo de Machine Learning (dataset original)</h2>
    <pre>{salida}</pre>
    <h3>Figuras generadas</h3>
    {html_imgs or "<p>No se encontraron figuras.</p>"}
    """
    return render_pagina("Modelo ML original", html)


@app.route("/modelo_aumentado")
def modelo_aumentado():
    salida = ejecutar_script("ModeloMLAumentado.py")

    figuras = []
    if os.path.isdir(CARPETA_FIGURAS):
        for f in sorted(os.listdir(CARPETA_FIGURAS)):
            if f.startswith("modelo_aumentado_") and f.lower().endswith(".png"):
                figuras.append(f)

    html_imgs = "".join(
        f'<img src="/static/figuras/{f}" alt="{f}">' for f in figuras
    )

    html = f"""
    <h2>Modelo de Machine Learning (dataset aumentado)</h2>
    <pre>{salida}</pre>
    <h3>Figuras generadas</h3>
    {html_imgs or "<p>No se encontraron figuras.</p>"}
    """
    return render_pagina("Modelo ML aumentado", html)


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    # Aseguramos que exista la carpeta de figuras
    os.makedirs(CARPETA_FIGURAS, exist_ok=True)
    app.run(debug=True)
