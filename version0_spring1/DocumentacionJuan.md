# TRABAJO EN EQUIPO 

### EQUIPO 11

# TEMA

**Tenemos una tienda llamada "DÍA" operando como minisúper que comenzó a operar en enero de 2023, en Argentina. Para hacer crecer nuestro negocio, comenzamos a registrar a cada cliente que nos visitaba y su crecimiento**

## Especificaciones:

1.- Cada registro guarda quién es el cliente, cómo contactarlo, de qué ciudad viene y desde cuándo forma parte de nuestra comunidad.

Ejemplos:

El 1 de enero de 2023, se registró Mariana Lopez, de Carlos Paz, quien dejó su correo electrónico para recibir novedades.

Al día siguiente, llegó Nicolás Rojas, también de Carlos Paz, mostrando que en esa ciudad empezó a crecer tu base de clientes.

Unos días después se unió Hernán Martínez, pero esta vez desde Río Cuarto, lo que mostró que tu negocio empezó a expandirse a otras ciudades.

Con el paso del tiempo, la lista se fue llenando y vemos lo siguiente:

Qué tan rápido creció nuestra clientela (gracias a las fechas de alta).

Dónde están ubicados nuestros clientes (ciudades principales como Córdoba, Carlos Paz, Río Cuarto).

Cómo contactarlos (correos electrónicos organizados).

Esto derivo en la creación de los siguientes registros que consideramos oportunos: 

**Productos**

La tienda no solo sumaba clientes, también ampliaba su catálogo. En la base de datos de productos encontramos los artículos que se ofrecen, cada uno con su nombre, descripción, precio y categoría. Esto muestra cómo la tienda fue diversificando su oferta para atraer a distintos tipos de clientes.

**Ventas**

La tercera pieza del rompecabezas son las ventas. Aquí se registran los movimientos reales: qué cliente compró, qué producto eligió, en qué fecha y en qué cantidad.
Al cruzar esta información con los clientes y productos, podemos ver:

Quiénes son los clientes más activos.

Qué productos tienen mayor demanda.

Cómo varían las compras por ciudad o a lo largo del tiempo.

La historia completa
Al unir las tres bases, la historia deja de ser solo una lista de datos y se convierte en un relato de crecimiento empresarial:

Los primeros clientes que llegaron en enero.

Los productos que empezaron a ganar popularidad.

Las ventas que fueron consolidando la confianza y preferencia en diferentes ciudades.

Así, la base de datos cuenta la evolución de un negocio: desde registrar los primeros clientes, pasando por construir un catálogo de productos, hasta generar ventas que muestran qué tan fuerte es la relación entre la tienda y su comunidad.

### ESTRUCTURA:

Estructura: Base de datos de tipo tabular (filas, columnas) en formato Excel donde se compone de los siguientes rubros:

Las tablas principales serán:

* Clientes (id_cliente, nombre_cliente, email, ciudad, fecha_alta)

* Productos (id_producto, nombre_producto, categoria, precio_unitario)

* Ventas (id_venta, fecha, id_cliente, medio_pago)

* Detalle_Ventas (id_venta, id_producto, cantidad, importe)

Tipos de Datos:

* INTEGER para identificadores (IDs) y cantidades.

* TEXT o VARCHAR para nombres, emails, ciudades, categorías, etc.

* DATE o DATETIME para las fechas de venta y alta de clientes.

* REAL o DECIMAL para precios e importes monetarios, para asegurar la precisión.

De nuestro modelo relacional, nuestras llaves primarias (PK) y foráneas (FK) son las siguientes:

1. Clientes

PK: id_cliente

Sin foráneas (tabla independiente, es maestra para Ventas).

2. Productos

PK: id_producto

Sin foráneas (tabla independiente, es maestra para Detalle_Ventas).

3. Ventas

PK: id_venta

FK: id_cliente → referencia a Clientes(id_cliente)

4. Detalle_Ventas

PK compuesta: (id_venta, id_producto)
(cada producto vendido dentro de una venta es único en el detalle).

FK1: id_venta → referencia a Ventas(id_venta)

FK2: id_producto → referencia a Productos(id_producto)

## ESCALA: 
### Clientes
- **id_cliente** → Nominal (identificador)  
- **nombre_cliente** → Nominal  
- **email** → Nominal  
- **ciudad** → Nominal  
- **fecha_alta** → Intervalo (fecha)

### Productos
- **id_producto** → Nominal (identificador)  
- **nombre_producto** → Nominal  
- **categoria** → Nominal *(u ordinal si existe jerarquía)*  
- **precio_unitario** → Razón

### Ventas
- **id_venta** → Nominal (identificador)  
- **fecha** → Intervalo (fecha)  
- **id_cliente** → Nominal (FK)  
- **medio_pago** → Nominal

### Detalle_Ventas
- **id_venta** → Nominal (FK)  
- **id_producto** → Nominal (FK)  
- **cantidad** → Razón (discreta)  
- **importe** → Razón

## Formato Tabla:

**Clientes**

| Tabla | Campo | Tipo de Dato |
|-------|-------|--------------|
| id_cliente | Nominal (identificador) |
| | nombre_cliente | Nominal |
| | email | Nominal |
| | ciudad | Nominal |
| | fecha_alta | Intervalo (fecha) |

**Productos**

| Tabla | Campo | Tipo de Dato |
|-------|-------|--------------|
| | id_producto | Nominal (identificador) |
| | nombre_producto | Nominal |
| | categoria | Nominal *(u ordinal si existe jerarquía)* |
| | precio_unitario | Razón |

**Ventas**

| Tabla | Campo | Tipo de Dato |
|-------|-------|--------------|
| | id_venta | Nominal (identificador) |
| | fecha | Intervalo (fecha) |
| | id_cliente | Nominal (FK) |
| | medio_pago | Nominal |

**Detalle_Ventas**

| Tabla | Campo | Tipo de Dato |
|-------|-------|--------------|
| | id_venta | Nominal (FK) |
| | id_producto | Nominal (FK) |
| | cantidad | Razón (discreta) |
| | importe | Razón |


#

# Para el programa en Python que consultará la documentación:
## Define información, pasos y pseudocódigo


 ## 1. Información a Manejar


- Carpeta del proyecto.
- Carpeta en VS Code.
- Archivo Documentación.md.
- Tema, problema y solución.
- Base de datos





## 2. Pasos del Programa

El script seguirá una secuencia lógica para funcionar:

Listar las Tareas: 


* **Tarea 1: Preparación del Entorno**
    * ✅ Crear una carpeta para el proyecto.
    * ✅ Conectar la carpeta a Visual Studio Code.
    * ✅ Crear el archivo `Documentacion.md`.

***

* **Tarea 2: Documentación del Proyecto**
    * ✅ Definir el tema, problema y solución.
    * ✅ Describir la estructura, tipos y escala de la base de datos.

***

* **Tarea 3: Planificación del Script**
    * ✅ Definir la información, pasos y pseudocódigo para el programa en Python.



3. Pseudocódigo

## Pseudocódigo: Proyecto Aurelion



Algoritmo ProyectoAurelion
	
	// --- Módulo 1: Preparación del Entorno ---
	Escribir "--- Módulo 1: Preparación del Entorno ---"
	
	Escribir "Paso 1: Crear la carpeta Proyecto Aurelion en tu PC."
	Escribir "Paso 2: Abrir Visual Studio Code y conectar a la carpeta del proyecto."
	
	Escribir "Paso 3: Crear un nuevo archivo llamado Documentacion.md."
	Escribir "" // Línea en blanco para separar
	
	// --- Módulo 2: Documentación ---
	Escribir "--- Módulo 2: Documentación (dentro de Documentacion.md) ---"
	Escribir "Paso 4: Escribir la sección Tema, Problema y Solución."
	Escribir "Paso 5: Escribir la sección Descripción de la BD , definiendo su estructura, tipos y escala."
	Escribir "" // Línea en blanco para separar
	
	// --- Módulo 3: Planificación ---
	Escribir "--- Módulo 3: Planificación (dentro de Documentacion.md) ---"
	Escribir "Paso 6: Escribir la sección Plan del Programa, definiendo la información, los pasos y el pseudocódigo."
	Escribir "Paso final: Guardar el archivo Documentacion.md"

FinAlgoritmo


![alt text](<Proyecto Aurelion-2025-10-09-234251.png>)
