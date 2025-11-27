#!/usr/bin/env python
# coding: utf-8

"""
Script de Estadísticas Descriptivas, Distribuciones, Correlaciones y Dashboard.
Versión adaptada para integrarse con programa_web.py:

- No usa plt.show() (no abre ventanas).
- Guarda todas las figuras en static/figuras con prefijo 'estadisticas_'.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", 100)

# Carpeta donde se guardan las figuras para la web
BASE_DIR = Path(__file__).resolve().parent
CARPETA_FIGURAS = BASE_DIR / "static" / "figuras"
CARPETA_FIGURAS.mkdir(parents=True, exist_ok=True)

# Limpio figuras viejas de estadísticas
for f in CARPETA_FIGURAS.glob("estadisticas_*.png"):
    try:
        f.unlink()
    except Exception:
        pass


# ==========================================================
# LOCALIZAR CARPETA DE DATOS
# ==========================================================
def find_data_dir(start: Path | None = None, names=("datos", "data")) -> Path | None:
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


# Archivos esperados (relativos a la carpeta de datos)
ARCHIVOS_INFO = {
    "clientes": "limpios/df_clientes_limpio.csv",
    "productos": "limpios/df_productos_limpio.csv",
    "ventas": "limpios/df_ventas_limpio.csv",
    "detalle_ventas": "limpios/df_detalle_ventas_limpio.csv",
}

DATAFRAMES: dict[str, pd.DataFrame] = {}


# ==========================================================
# CARGA DE DATASETS
# ==========================================================
def cargar_datasets():
    print("\n--- 1️⃣ CARGANDO DATASETS INDIVIDUALMENTE ---")
    data_dir = find_data_dir()
    if data_dir is None:
        raise FileNotFoundError(
            "❌ No se encontró carpeta 'datos' o 'data' en el proyecto."
        )

    for nombre, archivo in ARCHIVOS_INFO.items():
        ruta = data_dir / archivo
        try:
            df_temp = pd.read_csv(ruta)
            DATAFRAMES[nombre] = df_temp
            print(
                f"✅ Cargado: {nombre} ({df_temp.shape[0]} filas, {df_temp.shape[1]} columnas)"
            )
        except FileNotFoundError:
            print(f"❌ ERROR: Archivo '{archivo}' no encontrado en {ruta}.")
        except Exception as e:
            print(f"❌ ERROR al procesar '{archivo}': {e}")


# ==========================================================
# UTILIDADES
# ==========================================================
def clasificar_distribucion(serie: pd.Series):
    skew = serie.skew()
    kurt = serie.kurtosis()
    if np.isnan(skew):
        return "sin variación / NaN", skew, kurt
    if abs(skew) < 0.5:
        tipo = "aprox. normal/simétrica"
    elif skew > 0:
        tipo = "sesgo a la derecha (cola derecha)"
    else:
        tipo = "sesgo a la izquierda (cola izquierda)"
    return tipo, skew, kurt


# ==========================================================
# 2) ESTADÍSTICAS BÁSICAS
# ==========================================================
def estadisticas_basicas():
    print("\n--- 2️⃣ ESTADÍSTICAS DESCRIPTIVAS BÁSICAS ---")
    for nombre, df in DATAFRAMES.items():
        print(
            f"\n{'='*60}\n📊 ESTADÍSTICAS BÁSICAS — {nombre.upper()}\n{'='*60}"
        )
        desc_num = df.select_dtypes(include=[np.number]).describe().T
        if not desc_num.empty:
            print("\n▶ Variables numéricas:")
            print(desc_num.to_string())

        desc_cat = df.select_dtypes(exclude=[np.number]).describe(include="all").T
        if not desc_cat.empty:
            print("\n▶ Variables categóricas / texto:")
            print(desc_cat.to_string())


# ==========================================================
# 3) DISTRIBUCIONES + HISTOGRAMAS (GUARDADOS)
# ==========================================================
def distribuciones_y_histogramas():
    print("\n--- 3️⃣ DISTRIBUCIONES DE VARIABLES + HISTOGRAMAS ---")
    for nombre, df in DATAFRAMES.items():
        print(
            f"\n{'='*60}\n📈 DISTRIBUCIONES — {nombre.upper()}\n{'='*60}"
        )
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            s = df[col].dropna()
            if s.empty:
                continue
            tipo, skew, kurt = clasificar_distribucion(s)
            print(
                f"- {col}: {tipo} | skew={skew:.2f}, kurtosis={kurt:.2f}"
            )

            plt.figure()
            sns.histplot(s, kde=True, bins=30)
            plt.title(f"Distribución de {col} — {nombre}")
            plt.xlabel(col)
            plt.ylabel("Frecuencia")

            nombre_fig = f"estadisticas_{nombre}_hist_{col}.png"
            ruta = CARPETA_FIGURAS / nombre_fig
            plt.tight_layout()
            plt.savefig(ruta, bbox_inches="tight")
            plt.close()
            print(f"   📷 Histograma guardado: {ruta}")


# ==========================================================
# 4) CORRELACIONES + HEATMAPS (GUARDADOS)
# ==========================================================
def correlaciones():
    print("\n--- 4️⃣ ANÁLISIS DE CORRELACIONES ---")
    for nombre, df in DATAFRAMES.items():
        num = df.select_dtypes(include=[np.number])
        if num.shape[1] < 2:
            print(
                f"⚠️ {nombre}: No hay suficientes columnas numéricas para correlación."
            )
            continue

        corr = num.corr()
        print(f"\nMatriz de correlación — {nombre.upper()}:")
        print(corr.to_string())

        plt.figure(figsize=(6, 4))
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="Blues",
            cbar=True,
            square=True,
        )
        plt.title(f"Mapa de calor de correlaciones — {nombre}")
        plt.tight_layout()
        nombre_fig = f"estadisticas_{nombre}_corr.png"
        ruta = CARPETA_FIGURAS / nombre_fig
        plt.savefig(ruta, bbox_inches="tight")
        plt.close()
        print(f"   📷 Heatmap guardado: {ruta}")


# ==========================================================
# 5) DASHBOARD (dejamos solo HTML como antes)
# ==========================================================
def dashboard_simple():
    """
    Dejo un placeholder por si querés seguir usando Plotly.
    Acá podrías reconstruir tu dashboard interactivo si lo necesitás.
    """
    print("\n--- 5️⃣ DASHBOARD (opcional) ---")
    print(
        "Si querés, podemos volver a armar el dashboard de Plotly acá, "
        "pero para la demo principal ya tenés histos y correlaciones."
    )


# ==========================================================
# MAIN
# ==========================================================
def run_all():
    cargar_datasets()
    estadisticas_basicas()
    distribuciones_y_histogramas()
    correlaciones()
    dashboard_simple()
    print("\n🎉 Proceso de estadísticas completado correctamente.")


if __name__ == "__main__":
    run_all()
