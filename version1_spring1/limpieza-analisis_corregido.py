#!/usr/bin/env python
# coding: utf-8

"""
Script de limpieza y análisis inicial de datasets de ventas.
Versión corregida: incluye exportación funcional y detección automática de formato.
"""

import pandas as pd
from pathlib import Path

# =============================================================
# FUNCIONES AUXILIARES
# =============================================================

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


def get_dataset(filename: str, base_dir: str | Path | None = None) -> pd.DataFrame:
    """Carga automáticamente un archivo Excel o CSV desde la carpeta 'datos'."""
    if base_dir is None:
        base_dir = find_data_dir()
        if base_dir is None:
            raise FileNotFoundError("No se pudo localizar la carpeta 'datos'.")
    filepath = Path(base_dir) / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
    if filepath.suffix.lower() == '.csv':
        return pd.read_csv(filepath)
    else:
        return pd.read_excel(filepath)


# =============================================================
# 1️⃣ IMPORTAR DATASETS
# =============================================================

archivos_info = {
    'clientes': 'clientes.xlsx',
    'productos': 'productos.xlsx',
    'ventas': 'ventas.xlsx',
    'detalle_ventas': 'detalle_ventas.xlsx'
}

dataframes = {}

print("--- 1️⃣ CARGANDO DATASETS ---")
for nombre, archivo in archivos_info.items():
    try:
        df_temp = get_dataset(archivo)
        dataframes[nombre] = df_temp
        print(f"✅ Cargado: {nombre} ({df_temp.shape[0]} filas, {df_temp.shape[1]} columnas)")
    except Exception as e:
        print(f"❌ ERROR al cargar {archivo}: {e}")


# =============================================================
# 2️⃣ ANÁLISIS BÁSICO DE CADA DATASET
# =============================================================

for nombre, df in dataframes.items():
    print(f"\n{'='*60}\n📊 ANALISIS — {nombre.upper()}\n{'='*60}")
    print(df.info())
    print(df.describe(include='all').transpose())
    duplicados = df.duplicated().sum()
    print(f"🔁 Filas duplicadas: {duplicados}")
    id_cols = [c for c in df.columns if 'id' in c.lower()]
    for c in id_cols:
        print(f"🧩 {c}: {df[c].nunique()} únicos")


# =============================================================
# 3️⃣ EXPORTACIÓN DE DATASETS LIMPIOS
# =============================================================

print("\n--- 3️⃣ EXPORTANDO ARCHIVOS LIMPIOS ---")
salida_base = find_data_dir()
if salida_base is None:
    raise FileNotFoundError("No se pudo localizar la carpeta 'datos' para exportar los archivos limpios.")
SALIDA = salida_base / 'limpios'
SALIDA.mkdir(parents=True, exist_ok=True)

for nombre, df in dataframes.items():
    archivo = SALIDA / f"{nombre}_limpio.csv"
    df.to_csv(archivo, index=False, encoding='utf-8-sig')
    print(f"✅ Exportado: {archivo}")

print("\n🎉 Proceso completado correctamente.")
