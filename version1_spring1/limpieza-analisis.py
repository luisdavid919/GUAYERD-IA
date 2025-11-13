#!/usr/bin/env python
# coding: utf-8

# ###. 1 Importamos Dataset

# In[82]:


import pandas as pd
from pathlib import Path

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

# Función para cargar un archivo desde la carpeta 'datos'
def get_dataset(filename: str, base_dir: str | Path | None = None) -> pd.DataFrame:
    if base_dir is None:
        base_dir = find_data_dir()
        if base_dir is None:
            raise FileNotFoundError("No se pudo localizar la carpeta 'datos'.")
    filepath = Path(base_dir) / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
    return pd.read_excel(filepath)

# Cargar el dataset 'clientes.xlsx'
dataset1 = get_dataset('clientes.xlsx')

dataset1.info()


# ### 2. Verificamos la limpieza de los datos

# In[83]:


dataset1.head()


# In[84]:


dataset1.duplicated(keep=False)


# In[85]:


conteo_duplicados = dataset1.duplicated().sum()
print(f'Número de filas duplicadas: {conteo_duplicados}')


# In[86]:


dataset1.describe(include='all').transpose()


# In[87]:


dataset1['id_cliente'].nunique()


# ### 3. Estadisticas del Dataset

# In[88]:


dataset1.describe()


# ### 4. Importamos y analizamos `detalle_ventas.xlsx`

# In[89]:


# Lectura del archivo detalle_ventas.xlsx
dataset2 = get_dataset('detalle_ventas.xlsx')

dataset2.info()


# In[90]:


# Vista rápida
dataset2.head()


# In[91]:


# Detección de filas duplicadas (booleano)
dataset2.duplicated(keep=False)


# In[92]:


conteo_duplicados = dataset2.duplicated().sum()
print(f'Número de filas duplicadas (detalle_ventas): {conteo_duplicados}')


# In[93]:


dataset2.describe(include='all').transpose()


# In[94]:


# Intentamos obtener el conteo de IDs comunes de detalle_ventas (si existen)
candidate_ids = ['id_detalle', 'id_detalle_venta', 'id_venta', 'id_producto', 'id']
for c in candidate_ids:
    if c in dataset2.columns:
        print(f'Columna encontrada: {c} -> Unicos: {dataset2[c].nunique()}')
        break
else:
    print('No se encontró una columna ID conocida en detalle_ventas. Columnas disponibles:', dataset2.columns.tolist())


# ### 5. Importamos y analizamos `productos.xlsx`

# In[95]:


# Lectura del archivo productos.xlsx
dataset3 = get_dataset('productos.xlsx')

dataset3.info()


# In[96]:


dataset3.head()


# In[97]:


dataset3.duplicated(keep=False)


# In[98]:


conteo_duplicados_prod = dataset3.duplicated().sum()
print(f'Número de filas duplicadas (productos): {conteo_duplicados_prod}')


# In[99]:


dataset3.describe(include='all').transpose()


# In[100]:


# Intentamos obtener el conteo de IDs comunes de productos (si existen)
candidate_ids_prod = ['id_producto', 'producto_id', 'id']
for c in candidate_ids_prod:
    if c in dataset3.columns:
        print(f'Columna encontrada: {c} -> Unicos: {dataset3[c].nunique()}')
        break
else:
    print('No se encontró una columna ID conocida en productos. Columnas disponibles:', dataset3.columns.tolist())


# ### 6. Importamos y analizamos `ventas.xlsx`

# In[101]:


# Lectura del archivo ventas.xlsx
dataset4 = get_dataset('ventas.xlsx')

dataset4.info()


# In[102]:


dataset4.head()


# In[103]:


dataset4.duplicated(keep=False)


# In[104]:


conteo_duplicados_ventas = dataset4.duplicated().sum()
print(f'Número de filas duplicadas (ventas): {conteo_duplicados_ventas}')


# In[105]:


dataset4.describe(include='all').transpose()


# In[106]:


# Intentamos obtener el conteo de IDs comunes de ventas (si existen)
candidate_ids_ventas = ['id_venta', 'venta_id', 'id']
for c in candidate_ids_ventas:
    if c in dataset4.columns:
        print(f'Columna encontrada: {c} -> Unicos: {dataset4[c].nunique()}')
        break
else:
    print('No se encontró una columna ID conocida en ventas. Columnas disponibles:', dataset4.columns.tolist())


# In[109]:


from pathlib import Path
import pandas as pd

# --- PASO 1: CONFIGURACIÓN DE RUTAS Y NOMBRES ---
# Define tus 4 archivos con sus nombres específicos
archivos_info = {
    'clientes': 'clientes.xlsx',
    'productos': 'productos.xlsx',
    'ventas': 'ventas.xlsx',
    'detalle_ventas': 'detalle_ventas.xlsx'
}

dataframes = {}

print("--- 1. CARGANDO DATASETS INDIVIDUALMENTE ---")

for nombre, archivo in archivos_info.items():
    try:
        # Usamos get_dataset para leer cada archivo desde la carpeta 'datos'
        df_temp = get_dataset(archivo)
        dataframes[nombre] = df_temp  # Almacena cada DataFrame con su nombre clave
        print(f"✅ Cargado: {nombre} ({df_temp.shape[0]} filas)")
    except FileNotFoundError:
        print(f"❌ ERROR: Archivo '{archivo}' no encontrado.")
    except Exception as e:
        print(f"❌ ERROR al procesar '{archivo}': {e}")

# Accede a tus DataFrames así:
# df_clientes = dataframes['clientes']
# df_productos = dataframes['productos']


# In[ ]:


from pathlib import Path

# Carpeta donde guardar los CSV
SALIDA = find_data_dir() / 'limpios'
SALIDA.mkdir(parents=True, exist_ok=True)

# Exportar cada DataFrame limpio a CSV
for nombre, df in dataframes_limpios.items():
    archivo = SALIDA / f"{nombre}.csv"
    df.to_csv(archivo, index=False, encoding='utf-8-sig')
    print(f"✅ Exportado: {archivo}")

