import csv
import psycopg2

# Parámetros de conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="tienda_de_mascotas",
    user="martingodoytorres",
    password="martinbacan!",
    host="localhost",
    port="5432"
)

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Ruta del archivo CSV
ruta = 'data_items.csv'

# Leer el archivo CSV e insertar los datos en la tabla
with open(ruta, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        # Convertir campos vacíos en valores NULL o valores por defecto
        item_id = int(row['item_id']) if row['item_id'] else None
        descripcion = row['description'] if row['description'] else None
        sub_categoria = row['description_2'] if row['description_2'] else None
        categoria = row['group_description'] if row['group_description'] else None
        precio_venta_unitario = float(row['unit_sale_price (CLP)']) if row['unit_sale_price (CLP)'] else None
        costo = int(row['cost (CLP)']) if row['cost (CLP)'] else None
        costo_almacenamiento = int(row['storage_cost (CLP)']) if row['storage_cost (CLP)'] else None
        stock = int(row['stock']) if row['stock'] else None
        volumen_m3 = float(row['size_m3']) if row['size_m3'] else None
        costo_por_compra = int(row['cost_per_purchase']) if row['cost_per_purchase'] else None

        # Insertar los datos en la tabla
        cursor.execute('''
        INSERT INTO productos (item_id, descripcion, sub_categoria, categoria, 
                               precio_venta_unitario, costo, costo_almacenamiento, 
                               stock, volumen_m3, costo_por_compra)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (item_id) DO NOTHING
        ''', (
            item_id,
            descripcion,
            sub_categoria,
            categoria,
            precio_venta_unitario,
            costo,
            costo_almacenamiento,
            stock,
            volumen_m3,
            costo_por_compra
        ))

# Guardar (commit) los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()

print("Datos importados correctamente a la base de datos 'tienda_de_mascotas'.")

# import pandas as pd
# from sqlalchemy import create_engine

# # Parámetros de conexión a la base de datos PostgreSQL
# DATABASE_URL = 'postgresql+psycopg2://amparojohnson:Ratonfil1!@localhost:5432/tienda_de_mascotas'

# # Crear una conexión a la base de datos
# engine = create_engine(DATABASE_URL)

# # Ruta del archivo CSV
# ruta = 'data_items.csv'

# # Leer el archivo CSV en un DataFrame de pandas
# df = pd.read_csv(ruta)

# # Convertir campos vacíos en valores NULL
# df.replace('', pd.NA, inplace=True)

# # Insertar datos en la tabla 'productos'
# df.to_sql('productos', engine, if_exists='append', index=False, method='multi')

# print("Datos importados correctamente a la base de datos 'tienda_de_mascotas'.")
