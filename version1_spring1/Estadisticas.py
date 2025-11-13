#!/usr/bin/env python
# coding: utf-8

# Estadísticas descriptivas básicas calculadas

# In[11]:


import pandas as pd
import numpy as np
from pathlib import Path
from IPython.display import display, Markdown, Image
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


# --- PASO 1: CONFIGURACIÓN DE RUTAS Y NOMBRES ---
archivos_info = {
    'clientes': 'limpios/df_clientes_limpio.csv',
    'productos': 'limpios/df_productos_limpio.csv',
    'ventas': 'limpios/df_ventas_limpio.csv',
    'detalle_ventas': 'limpios/df_detalle_ventas_limpio.csv'
}

dataframes = {}

print("--- 1. CARGANDO DATASETS INDIVIDUALMENTE ---")

for nombre, archivo in archivos_info.items():
    try:
        # ✅ Leer como CSV desde la carpeta detectada
        ruta = find_data_dir() / archivo
        df_temp = pd.read_csv(ruta)
        dataframes[nombre] = df_temp
        print(f"✅ Cargado: {nombre} ({df_temp.shape[0]} filas, {df_temp.shape[1]} columnas)")
    except FileNotFoundError:
        print(f"❌ ERROR: Archivo '{archivo}' no encontrado.")
    except Exception as e:
        print(f"❌ ERROR al procesar '{archivo}': {e}")


# In[12]:


# Función para detectar la carpeta 'datos'
def find_data_dir(start: Path | None = None, names=('datos', 'data')) -> Path | None:
    if start is None:
        start = Path.cwd()
    start = Path(start).resolve()
    for parent in [start] + list(start.parents):
        for n in names:
            candidate = parent / n
            if candidate.is_dir():
                return candidate
    return None


# In[13]:


import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", 100)

def es_numerica(s):
    return pd.api.types.is_numeric_dtype(s)


# Estadísticas descriptivas básicas calculadas

# 

# In[14]:


for nombre, df in dataframes.items():
    print(f"\n{'='*60}\n📊 ESTADÍSTICAS BÁSICAS — {nombre.upper()}\n{'='*60}")

    # Numéricas
    desc_num = df.select_dtypes(include=[np.number]).describe().T
    if not desc_num.empty:
        print("\n▶ Numéricas:")
        display(desc_num)

    # No numéricas
    desc_cat = df.select_dtypes(exclude=[np.number]).describe(include='all').T
    if not desc_cat.empty:
        print("\n▶ Categóricas / texto:")
        display(desc_cat)


# Identificación del tipo de distribución

# In[15]:


def clasificar_distribucion(serie):
    skew = serie.skew()
    kurt = serie.kurtosis()
    if np.isnan(skew):  # todo NaN o constante
        return "sin variación / NaN", skew, kurt
    # Heurística simple por asimetría
    if abs(skew) < 0.5:
        tipo = "aprox. normal/simétrica"
    elif skew >= 0.5:
        tipo = "sesgo a la derecha (cola derecha)"
    else:
        tipo = "sesgo a la izquierda (cola izquierda)"
    return tipo, skew, kurt

for nombre, df in dataframes.items():
    print(f"\n{'='*60}\n📈 DISTRIBUCIONES — {nombre.upper()}\n{'='*60}")

    # Numéricas: clasificación + histograma
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        s = df[col].dropna()
        tipo, skew, kurt = clasificar_distribucion(s)
        print(f"- {col}: {tipo} | skew={skew:.2f}, kurtosis={kurt:.2f}")

        # Histograma + KDE
        plt.figure()
        sns.histplot(s, kde=True, bins=30)
        plt.title(f"Distribución de {col} — {nombre}")
        plt.xlabel(col)
        plt.ylabel("Frecuencia")
        plt.show()

    # Categóricas: top 10 frecuencias
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    if len(cat_cols) > 0:
        print("\n▶ Frecuencias (top 10) en categóricas:")
        for col in cat_cols:
            vc = df[col].value_counts(dropna=False).head(10)
            print(f"\n{col} (top 10):")
            display(vc.to_frame("conteo"))


# Análisis de correlaciones entre variables principales

# In[16]:


for nombre, df in dataframes.items():
    print(f"\n{'='*60}\n🔗 CORRELACIONES — {nombre.upper()}\n{'='*60}")
    num = df.select_dtypes(include=[np.number])
    if num.shape[1] < 2:
        print("⚠️ No hay suficientes columnas numéricas para correlación.")
        continue

    corr = num.corr(numeric_only=True)
    display(corr)

    # Mapa de calor
    plt.figure(figsize=(min(10, 1.2*len(num.columns)), min(8, 0.9*len(num.columns))))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=False)
    plt.title(f"Matriz de correlación — {nombre}")
    plt.tight_layout()
    plt.show()

    # Pares con mayor correlación (en valor absoluto), sin duplicados ni diagonal
    corr_pairs = (
        corr.where(~np.eye(corr.shape[0], dtype=bool))
            .abs()
            .stack()
            .sort_values(ascending=False)
    )
    top = corr_pairs.drop_duplicates().head(10)
    if not top.empty:
        print("\n▶ Top correlaciones (|r| más alto):")
        display(top.to_frame("abs(r)"))


# Detección de outliers

# In[17]:


def iqr_outliers(s):
    """Devuelve máscara booleana de outliers y límites inferior/superior según el método IQR."""
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    mask = (s < lim_inf) | (s > lim_sup)
    return mask, lim_inf, lim_sup

for nombre, df in dataframes.items():
    print(f"\n{'='*60}\n🚨 OUTLIERS (IQR) — {nombre.upper()}\n{'='*60}")

    # ✅ Seleccionamos solo columnas numéricas que no sean IDs
    num_cols = [
        c for c in df.select_dtypes(include=[np.number]).columns
        if "id" not in c.lower()
    ]

    if len(num_cols) == 0:
        print("No hay columnas numéricas válidas (sin IDs).")
        continue

    resumen = []
    outlier_indices_global = set()

    for col in num_cols:
        s = df[col].dropna()
        if s.empty:
            continue

        mask, li, ls = iqr_outliers(s)
        idx = s.index[mask]
        resumen.append({
            "columna": col,
            "outliers": len(idx),
            "lim_inf": li,
            "lim_sup": ls
        })
        outlier_indices_global.update(idx)

        # Boxplot visual
        plt.figure()
        sns.boxplot(x=df[col])
        plt.title(f"Boxplot y outliers en {col} — {nombre}")
        plt.show()

    if resumen:
        print("\n▶ Resumen por columna:")
        display(pd.DataFrame(resumen).sort_values("outliers", ascending=False))

    if outlier_indices_global:
        print("\n▶ Filas con al menos un outlier (primeras 20):")
        display(df.loc[sorted(outlier_indices_global)].head(20))
    else:
        print("✅ Sin outliers según criterio IQR.")


# In[18]:


import pandas as pd
import plotly.express as px
import panel as pn

# 1. Instalación (descomentar y ejecutar si es la primera vez)
# !pip install plotly pandas panel

# 2. Activar Panel para su uso en Jupyter
pn.extension()

# Asumo que 'dataframes' está cargado con las claves 'ventas', 'clientes', y 'detalle_ventas'.

# --- 3. FUSIÓN DE DATAFRAMES NECESARIA (CORREGIDO) ---
try:
    # **CORRECCIÓN CLAVE:** La columna de fecha en 'ventas' se llama 'fecha', no 'fecha_venta'.
    # 1. Unir ventas con clientes para obtener la ciudad
    df_ventas_cliente = pd.merge(
        dataframes['ventas'][['id_venta', 'id_cliente', 'fecha']], # <-- CORREGIDO AQUÍ
        dataframes['clientes'][['id_cliente', 'ciudad']],
        on='id_cliente',
        how='left'
    )
    # 2. Unir el resultado con el detalle de ventas para obtener el importe, producto y cantidad
    df_merge_full = pd.merge(
        df_ventas_cliente,
        dataframes['detalle_ventas'][['id_venta', 'importe', 'nombre_producto', 'cantidad']],
        on='id_venta',
        how='left'
    )
    print("✅ Fusión de DataFrames completada (df_merge_full).")
except Exception as e:
    print(f"❌ Error al fusionar DataFrames: {e}")
    raise

# --- 4. GENERACIÓN DE GRÁFICOS INTERACTIVOS (PLOTLY) ---

# A. GRÁFICO: Top 10 Productos Más Vendidos (en Cantidad)
top_productos = (
    df_merge_full.groupby('nombre_producto')['cantidad']
    .sum()
    .nlargest(10)
    .sort_values(ascending=True)
    .reset_index()
)
fig_productos = px.bar(
    top_productos, y='nombre_producto', x='cantidad', orientation='h',
    title='🥇 Top 10 Productos Más Vendidos (Cantidad)', color='cantidad',
    color_continuous_scale=px.colors.sequential.Viridis
).update_layout(yaxis_title="Producto", xaxis_title="Cantidad Vendida")


# B. GRÁFICO: Top 10 Clientes con Mayor Gasto Total
top_clientes = (
    df_merge_full.groupby('id_cliente')['importe']
    .sum()
    .nlargest(10)
    .sort_values(ascending=True)
    .reset_index()
)
fig_clientes = px.bar(
    top_clientes, y='id_cliente', x='importe', orientation='h',
    title='💰 Top 10 Clientes por Gasto Total', color='importe',
    color_continuous_scale=px.colors.sequential.Plasma
).update_layout(yaxis_title="ID Cliente", xaxis_title="Gasto Total ($)")
fig_clientes.update_traces(hovertemplate='Gasto Total: $%{x:.2f}<extra></extra>')


# C. GRÁFICO: Top 10 Ciudades con Más Ventas (en Total)
top_ciudades = (
    df_merge_full.groupby('ciudad')['importe']
    .sum()
    .nlargest(10)
    .reset_index()
)
fig_ciudades = px.pie(
    top_ciudades, names='ciudad', values='importe',
    title='🏙️ Distribución de Ventas por Ciudad (Top 10)',
)
fig_ciudades.update_traces(textposition='inside', textinfo='percent+label')

print("✅ Gráficos Plotly generados exitosamente.")


# In[22]:


import pandas as pd
import plotly.express as px
from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

# Carga de DataFrames (Asegúrate que los archivos estén en la misma carpeta)
try:
    clientes = pd.read_csv('df_clientes_limpio.csv')
    ventas = pd.read_csv('df_ventas_limpio.csv')
    detalle_ventas = pd.read_csv('df_detalle_ventas_limpio.csv')
except Exception as e:
    print(f"❌ Error al cargar archivos CSV: {e}")
    raise

# --- 1. FUSIÓN DE DATAFRAMES Y PREPROCESAMIENTO (CORREGIDO) ---
try:
    # 1.1 Fusión de DataFrames (usando 'fecha' y 'ciudad')
    df_ventas_cliente = pd.merge(
        ventas[['id_venta', 'id_cliente', 'fecha']],
        clientes[['id_cliente', 'ciudad']],
        on='id_cliente',
        how='left'
    )
    df_merge_full = pd.merge(
        df_ventas_cliente,
        detalle_ventas[['id_venta', 'importe', 'nombre_producto', 'cantidad']],
        on='id_venta',
        how='left'
    )
    
    # 1.2 Limpieza de columnas clave
    # Convertir a numérico y manejar NaNs (para evitar el IndexError en el KPI)
    df_merge_full['importe'] = pd.to_numeric(df_merge_full['importe'], errors='coerce').fillna(0.0)
    df_merge_full['cantidad'] = df_merge_full['cantidad'].fillna(0).astype(int)
    
except Exception as e:
    print(f"❌ Error durante la fusión o preprocesamiento: {e}")
    raise


# --- 2. GENERACIÓN DE GRÁFICOS INTERACTIVOS (PLOTLY) ---

# A. Top 10 Productos Más Vendidos (en Cantidad)
top_productos = df_merge_full.groupby('nombre_producto')['cantidad'].sum().nlargest(10).sort_values(ascending=True).reset_index()
fig_productos = px.bar(
    top_productos, y='nombre_producto', x='cantidad', orientation='h',
    color='cantidad', color_continuous_scale=px.colors.sequential.Viridis
)

# B. Top 10 Clientes con Mayor Gasto Total
top_clientes = df_merge_full.groupby('id_cliente')['importe'].sum().nlargest(10).sort_values(ascending=True).reset_index()
fig_clientes = px.bar(
    top_clientes, y='id_cliente', x='importe', orientation='h',
    color='importe', color_continuous_scale=px.colors.sequential.Plasma
)

# C. Top 10 Ciudades con Más Ventas (en Total)
top_ciudades = df_merge_full.groupby('ciudad')['importe'].sum().nlargest(10).reset_index()
fig_ciudades = px.pie(
    top_ciudades, names='ciudad', values='importe',
)


# --- 3. COMBINACIÓN DE GRÁFICOS EN HTML (DASHBOARD) ---

# Cálculo del KPI principal
venta_total_general = df_merge_full['importe'].sum()

# 3.1. Crear la figura de subplots (diseño 2x2: un gráfico grande, dos pequeños)
fig = make_subplots(
    rows=2, cols=2,
    # El gráfico de productos ocupa 2 filas, el de torta usa el tipo 'domain'
    specs=[[{"rowspan": 2, "type": "xy"}, {"type": "domain"}],
           [None, {"type": "xy"}]],
    column_widths=[0.6, 0.4],
    subplot_titles=("🥇 Top 10 Productos Más Vendidos (Cantidad)",
                    "🏙️ Distribución de Ventas por Ciudad (Top 10)",
                    "💰 Top 10 Clientes por Gasto Total")
)

# 3.2. Agregar los traces a los subplots
for trace in fig_productos.data: # A
    fig.add_trace(trace, row=1, col=1)

for trace in fig_ciudades.data: # C
    fig.add_trace(trace, row=1, col=2)

for trace in fig_clientes.data: # B
    fig.add_trace(trace, row=2, col=2)

# 3.3. Actualizar el diseño y agregar el KPI al título
fig.update_layout(
    height=800,
    width=1200,
    showlegend=True,
    title_text=f"## 📈 Dashboard de Estadísticas Clave de Ventas - Venta Total: ${venta_total_general:,.2f}",
    title_x=0.5
)
# Ajuste de ejes
fig.update_yaxes(title_text="Producto", row=1, col=1)
fig.update_xaxes(title_text="Cantidad Vendida", row=1, col=1)
fig.update_yaxes(title_text="ID Cliente", row=2, col=2)
fig.update_xaxes(title_text="Gasto Total ($)", row=2, col=2)


# 3.4. Guardar la figura combinada en un archivo HTML
html_path = "dashboard_ventas_combinado.html"
fig.write_html(html_path)

print(f"\n✅ Dashboard interactivo guardado en: {html_path}")
print("\n¡Descarga el archivo y ábrelo en tu navegador!")

