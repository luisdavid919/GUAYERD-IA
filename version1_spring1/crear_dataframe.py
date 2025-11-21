import pandas as pd
from pathlib import Path

# =========================================
# FUNCIONES AUXILIARES
# =========================================

def cargar_csv_con_busqueda(nombre_archivo: str) -> pd.DataFrame:
    """
    Intenta cargar un CSV probando varias rutas relativas a la ubicación de ML.py.
    Imprime qué archivo termina usando o qué errores encuentra.
    """
    script_dir = Path(__file__).resolve().parent
    print(f"\n🔎 Buscando {nombre_archivo}...")

    # Rutas candidatas (ajusta si usás otra estructura)
    candidatos = [
        script_dir / nombre_archivo,
        script_dir / "limpios" / nombre_archivo,
        script_dir / "datos" / "limpios" / nombre_archivo,
        script_dir / "data" / "limpios" / nombre_archivo,
        script_dir / "datos" / nombre_archivo,
        script_dir / "data" / nombre_archivo,
    ]

    for ruta in candidatos:
        print(f"  - Probando: {ruta}")
        if ruta.is_file():
            print(f"✅ Encontrado: {ruta}")
            return pd.read_csv(ruta)

    raise FileNotFoundError(
        f"No se encontró {nombre_archivo} en ninguna de las rutas probadas.\n"
        f"Ubicación de ML.py: {script_dir}"
    )


# =========================================
# 1) CARGA DE DATASETS
# =========================================

def cargar_datasets_ml():
    print("=========================================")
    print("   INICIO ML.py")
    print("=========================================")
    script_dir = Path(__file__).resolve().parent
    print(f"📂 Carpeta donde está ML.py: {script_dir}")

    df_clientes = cargar_csv_con_busqueda("df_clientes_limpio.csv")
    df_ventas = cargar_csv_con_busqueda("df_ventas_limpio.csv")
    df_detalle = cargar_csv_con_busqueda("df_detalle_ventas_limpio.csv")

    print("\nTamaños de los dataframes cargados:")
    print("  Clientes:", df_clientes.shape)
    print("  Ventas  :", df_ventas.shape)
    print("  Detalle :", df_detalle.shape)

    return df_clientes, df_ventas, df_detalle


# =========================================
# 2) CONSTRUIR DATAFRAME NIVEL VENTA
# =========================================

def construir_df_modelo(df_clientes, df_ventas, df_detalle):
    print("\n=========================================")
    print("   CONSTRUYENDO DATAFRAME df_modelo")
    print("=========================================")

    # Aseguramos tipos numéricos
    df_detalle["importe"] = pd.to_numeric(df_detalle["importe"], errors="coerce").fillna(0)
    df_detalle["cantidad"] = pd.to_numeric(df_detalle["cantidad"], errors="coerce").fillna(0)

    # --- Agregamos por id_venta (ticket) ---
    df_ticket = (
        df_detalle
        .groupby("id_venta")
        .agg(
            ticket_total=("importe", "sum"),            # suma del importe del ticket
            num_items=("cantidad", "sum"),             # total de unidades compradas
            num_lineas=("id_producto", "size"),        # cantidad de líneas del ticket
            num_unique_products=("id_producto", "nunique")  # productos distintos
        )
        .reset_index()
    )

    print("✔ Ticket (nivel venta) generado. Tamaño:", df_ticket.shape)

    # --- Unimos con ventas ---
    columnas_ventas = ["id_venta", "id_cliente", "fecha"]
    if "medio_pago" in df_ventas.columns:
        columnas_ventas.append("medio_pago")

    df_ventas_sel = df_ventas[columnas_ventas].copy()
    df_modelo = df_ticket.merge(df_ventas_sel, on="id_venta", how="left")
    print("✔ Merge con ventas. Tamaño actual:", df_modelo.shape)

    # --- Unimos con clientes ---
    columnas_clientes = ["id_cliente", "ciudad"]
    if "fecha_alta" in df_clientes.columns:
        columnas_clientes.append("fecha_alta")

    df_clientes_sel = df_clientes[columnas_clientes].copy()
    df_modelo = df_modelo.merge(df_clientes_sel, on="id_cliente", how="left")
    print("✔ Merge con clientes. Tamaño actual:", df_modelo.shape)

    # --- Fechas y features de tiempo ---
    df_modelo["fecha"] = pd.to_datetime(df_modelo["fecha"], errors="coerce")

    if "fecha_alta" in df_modelo.columns:
        df_modelo["fecha_alta"] = pd.to_datetime(df_modelo["fecha_alta"], errors="coerce")
        df_modelo["antiguedad_cliente_dias"] = (
            df_modelo["fecha"] - df_modelo["fecha_alta"]
        ).dt.days
    else:
        df_modelo["antiguedad_cliente_dias"] = pd.NA

    df_modelo["mes"] = df_modelo["fecha"].dt.month
    df_modelo["dia_semana"] = df_modelo["fecha"].dt.weekday  # 0=lunes, 6=domingo

    # --- Variable objetivo: ticket_alto (p75) ---
    umbral_75 = df_modelo["ticket_total"].quantile(0.75)
    print(f"\nUmbral para 'ticket_alto' (percentil 75): {umbral_75:.2f}")

    df_modelo["ticket_alto"] = (df_modelo["ticket_total"] >= umbral_75).astype(int)

    print("\nDistribución de 'ticket_alto' (0 = normal, 1 = alto):")
    print(df_modelo["ticket_alto"].value_counts(normalize=True))

    return df_modelo


# =========================================
# 3) MAIN
# =========================================

def main():
    try:
        df_clientes, df_ventas, df_detalle = cargar_datasets_ml()
        df_modelo = construir_df_modelo(df_clientes, df_ventas, df_detalle)

        print("\n=========================================")
        print("   PRIMERAS FILAS DEL DATAFRAME FINAL")
        print("=========================================")
        print(df_modelo.head())

        # Guardamos el dataframe final en la misma carpeta de ML.py
        script_dir = Path(__file__).resolve().parent
        salida = script_dir / "df_modelo_ticket_alto.csv"
        df_modelo.to_csv(salida, index=False)
        print(f"\n✅ Archivo guardado en: {salida}")

    except Exception as e:
        print("\n❌ OCURRIÓ UN ERROR EN ML.py")
        print(type(e).__name__, ":", e)


if __name__ == "__main__":
    main()


