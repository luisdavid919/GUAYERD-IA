# BASE DE DATOS  

### EQUIPO 11

### BASE DE DATOS CLIENTES

**Tenemos una tienda llamada "DÍA" operando como minisúper que comenzó a operar en enero de 2023, en Argentina. Para hacer crecer nuestro negocio, comenzamos a registrar a cada cliente que nos visitaba y su crecimiento**

### Especificaciones:

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

### Datos Técnicos:

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

ESCALA: 
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

