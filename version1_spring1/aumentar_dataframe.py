import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------
# 1) CARGAR DATASET ORIGINAL
# -----------------------------
script_dir = Path(__file__).resolve().parent
ruta = script_dir / "df_modelo_ticket_alto.csv"

df = pd.read_csv(ruta)
print("Shape original:", df.shape)

# -----------------------------
# 2) GENERAR 1000 FILAS EXTRA
# -----------------------------
N_EXTRA = 1000
target_col = "ticket_alto"

# muestramos filas reales con reemplazo (bootstrap)
df_extra = df.sample(N_EXTRA, replace=True, random_state=42).reset_index(drop=True)

# columnas numéricas (sacamos id_venta e id_cliente si están)
num_cols = df_extra.select_dtypes(include=["int64", "float64"]).columns.tolist()
for col_drop in ["id_venta", "id_cliente"]:
    if col_drop in num_cols:
        num_cols.remove(col_drop)
# no tocamos la columna target
if target_col in num_cols:
    num_cols.remove(target_col)

print("Columnas numéricas a las que les agregamos ruido:", num_cols)

# calculamos desvío estándar original
stds = df[num_cols].std()

# generamos ruido gaussiano (0.05 = 5% del desvío aprox)
ruido = np.random.normal(loc=0.0, scale=0.05, size=df_extra[num_cols].shape)
df_extra[num_cols] = df_extra[num_cols] + ruido * stds.values

# algunas columnas numéricas deberían seguir siendo enteros ≥ 0
cols_enteras = ["num_items", "num_lineas", "num_unique_products", "mes", "dia_semana"]
for col in cols_enteras:
    if col in df_extra.columns:
        df_extra[col] = df_extra[col].round().clip(lower=0).astype(int)

# antigüedad en días también entero pero puede ser grande
if "antiguedad_cliente_dias" in df_extra.columns:
    df_extra["antiguedad_cliente_dias"] = (
        df_extra["antiguedad_cliente_dias"].round().clip(lower=0).astype(int)
    )

print("Shape extra:", df_extra.shape)

# -----------------------------
# 3) CONCATENAR Y GUARDAR
# -----------------------------
df_aumentado = pd.concat([df, df_extra], ignore_index=True)
print("Shape final aumentado:", df_aumentado.shape)

salida = script_dir / "df_modelo_ticket_alto_aumentado.csv"
df_aumentado.to_csv(salida, index=False)
print(f"✅ Guardado en: {salida}")
