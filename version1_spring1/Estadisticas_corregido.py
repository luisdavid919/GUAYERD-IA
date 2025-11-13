#!/usr/bin/env python
# coding: utf-8

"""
Script de Estadísticas Descriptivas, Análisis de Distribución, Correlaciones y Dashboard Interactivo
Versión corregida y reorganizada.
"""

# ==========================================================
# IMPORTACIONES
# ==========================================================
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
import plotly.express as px
from plotly.subplots import make_subplots

pd.set_option("display.max_columns", 100)


# ==========================================================
# FUNCIÓN PARA ENCONTRAR LA CARPETA DE DATOS
# ==========================================================
def find_data_dir(start: Path | None = None, names=('datos', 'data')) -> Path | None:
    """Busca una carpeta llamada 'datos' o 'data' en el árbol de directorios."""
    if start is None:
        start = Path.cwd()
    start = Path(start).resolve()
    for parent in [start] + list(start.parents):
        for n in names:
            candidate = parent / n
            if candidate.is_dir():
                return candidate
    return None


# ==========================================================
# CARGA DE DATASETS
# ==========================================================
archivos_info = {
    'clientes': 'limpios/df_clientes_limpio.csv',
    'productos': 'limpios/df_productos_limpio.csv',
    'ventas': 'limpios/df_ventas_limpio.csv',
    'detalle_ventas': 'limpios/df_detalle_ventas_limpio.csv'
}

dataframes = {}

def cargar_datasets():
    print("\n--- 1️⃣ CARGANDO DATASETS INDIVIDUALMENTE ---")
    data_dir = find_data_dir()
    if data_dir is None:
        raise FileNotFoundError("❌ No se encontró carpeta 'datos' o 'data' en el proyecto.")
    for nombre, archivo in archivos_info.items():
        ruta = data_dir / archivo
        try:
            df_temp = pd.read_csv(ruta)
            dataframes[nombre] = df_temp
            print(f"✅ Cargado: {nombre} ({df_temp.shape[0]} filas, {df_temp.shape[1]} columnas)")
        except FileNotFoundError:
            print(f"❌ ERROR: Archivo '{archivo}' no encontrado en {ruta}.")
        except Exception as e:
            print(f"❌ ERROR al procesar '{archivo}': {e}")

# ==========================================================
# UTILIDADES Y ANALISIS
# ==========================================================
def clasificar_distribucion(serie):
    skew = serie.skew()
    kurt = serie.kurtosis()
    if np.isnan(skew):
        return "sin variación / NaN", skew, kurt
    if abs(skew) < 0.5:
        tipo = "aprox. normal/simétrica"
    elif skew >= 0.5:
        tipo = "sesgo a la derecha (cola derecha)"
    else:
        tipo = "sesgo a la izquierda (cola izquierda)"
    return tipo, skew, kurt

def iqr_outliers(s):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    li, ls = q1 - 1.5*iqr, q3 + 1.5*iqr
    mask = (s < li) | (s > ls)
    return mask, li, ls

# ==========================================================
# ANALISIS PRINCIPAL
# ==========================================================
def run_all():
    cargar_datasets()

    print("\n--- 2️⃣ ESTADÍSTICAS DESCRIPTIVAS ---")
    for nombre, df in dataframes.items():
        print(f"\n{'='*60}\n📊 ESTADÍSTICAS BÁSICAS — {nombre.upper()}\n{'='*60}")
        desc_num = df.select_dtypes(include=[np.number]).describe().T
        if not desc_num.empty:
            print("\n▶ Variables numéricas:")
            display(desc_num)
        desc_cat = df.select_dtypes(exclude=[np.number]).describe(include='all').T
        if not desc_cat.empty:
            print("\n▶ Variables categóricas / texto:")
            display(desc_cat)

    print("\n--- 3️⃣ DISTRIBUCIONES DE VARIABLES ---")
    for nombre, df in dataframes.items():
        print(f"\n{'='*60}\n📈 DISTRIBUCIONES — {nombre.upper()}\n{'='*60}")
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            s = df[col].dropna()
            tipo, skew, kurt = clasificar_distribucion(s)
            print(f"- {col}: {tipo} | skew={skew:.2f}, kurtosis={kurt:.2f}")
            plt.figure()
            sns.histplot(s, kde=True, bins=30)
            plt.title(f"Distribución de {col} — {nombre}")
            plt.xlabel(col)
            plt.ylabel("Frecuencia")
            plt.show()

    print("\n--- 4️⃣ ANÁLISIS DE CORRELACIONES ---")
    for nombre, df in dataframes.items():
        num = df.select_dtypes(include=[np.number])
        if num.shape[1] < 2:
            print(f"⚠️ {nombre}: No hay suficientes columnas numéricas para correlación.")
            continue
        corr = num.corr(numeric_only=True)
        display(corr)
        plt.figure(figsize=(min(10, 1.2*len(num.columns)), min(8, 0.9*len(num.columns))))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=False)
        plt.title(f"Matriz de correlación — {nombre}")
        plt.tight_layout()
        plt.show()

    print("\n--- 5️⃣ DETECCIÓN DE OUTLIERS ---")
    for nombre, df in dataframes.items():
        print(f"\n{'='*60}\n🚨 OUTLIERS — {nombre.upper()}\n{'='*60}")
        num_cols = [c for c in df.select_dtypes(include=[np.number]).columns if "id" not in c.lower()]
        if not num_cols:
            print("No hay columnas numéricas válidas (sin IDs).")
            continue
        resumen = []
        outlier_idx = set()
        for col in num_cols:
            s = df[col].dropna()
            mask, li, ls = iqr_outliers(s)
            idx = s.index[mask]
            resumen.append({"columna": col, "outliers": len(idx), "lim_inf": li, "lim_sup": ls})
            outlier_idx.update(idx)
            plt.figure()
            sns.boxplot(x=df[col])
            plt.title(f"Boxplot y outliers en {col} — {nombre}")
            plt.show()
        if resumen:
            print("\n▶ Resumen por columna:")
            display(pd.DataFrame(resumen).sort_values("outliers", ascending=False))
        if outlier_idx:
            print("\n▶ Filas con al menos un outlier (primeras 20):")
            display(df.loc[sorted(outlier_idx)].head(20))
        else:
            print("✅ Sin outliers detectados.")

    print("\n--- 6️⃣ CREACIÓN DE DASHBOARD INTERACTIVO ---")
    try:
        clientes = dataframes['clientes']
        ventas = dataframes['ventas']
        detalle = dataframes['detalle_ventas']
        df_ventas_cliente = pd.merge(
            ventas[['id_venta', 'id_cliente', 'fecha']],
            clientes[['id_cliente', 'ciudad']],
            on='id_cliente',
            how='left'
        )
        df_merge_full = pd.merge(
            df_ventas_cliente,
            detalle[['id_venta', 'importe', 'nombre_producto', 'cantidad']],
            on='id_venta',
            how='left'
        )
        df_merge_full['importe'] = pd.to_numeric(df_merge_full['importe'], errors='coerce').fillna(0)
        df_merge_full['cantidad'] = pd.to_numeric(df_merge_full['cantidad'], errors='coerce').fillna(0).astype(int)

        top_productos = df_merge_full.groupby('nombre_producto')['cantidad'].sum().nlargest(10).sort_values(ascending=True).reset_index()
        fig_prod = px.bar(top_productos, y='nombre_producto', x='cantidad', orientation='h', color='cantidad',
                          color_continuous_scale=px.colors.sequential.Viridis)

        top_clientes = df_merge_full.groupby('id_cliente')['importe'].sum().nlargest(10).sort_values(ascending=True).reset_index()
        fig_cli = px.bar(top_clientes, y='id_cliente', x='importe', orientation='h', color='importe',
                         color_continuous_scale=px.colors.sequential.Plasma)

        top_ciudades = df_merge_full.groupby('ciudad')['importe'].sum().nlargest(10).reset_index()
        fig_city = px.pie(top_ciudades, names='ciudad', values='importe')

        total = df_merge_full['importe'].sum()
        fig = make_subplots(rows=2, cols=2,
                            specs=[[{"rowspan": 2, "type": "xy"}, {"type": "domain"}],
                                   [None, {"type": "xy"}]],
                            column_widths=[0.6, 0.4],
                            subplot_titles=("Top 10 Productos", "Ventas por Ciudad", "Top 10 Clientes"))

        for trace in fig_prod.data: fig.add_trace(trace, row=1, col=1)
        for trace in fig_city.data: fig.add_trace(trace, row=1, col=2)
        for trace in fig_cli.data: fig.add_trace(trace, row=2, col=2)

        fig.update_layout(height=800, width=1200, showlegend=True,
                          title_text=f"📈 Dashboard de Ventas — Total: ${total:,.2f}", title_x=0.5)
        html_path = Path("dashboard_ventas_combinado.html")
        fig.write_html(str(html_path))
        print(f"\n✅ Dashboard interactivo generado: {html_path.resolve()}")
    except Exception as e:
        print(f"❌ Error al generar el dashboard: {e}")

if __name__ == "__main__":
    run_all()
