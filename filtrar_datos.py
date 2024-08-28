import csv
from datetime import datetime

# Crear listas para almacenar los datos de las tablas
cajas = []
personal = []
productos = []
living = []
dormitorio = []
iluminacion = []
stock = []
tiendas = []
clientes = []
compras = []
comuna_region = []
despachos = []
jefes = []
licencias = []
repartidores = []
vehiculos = []

# Iterar sobre los archivos CSV
archivos_csv = ["cajas.csv", "personal.csv", "productos.csv", "stock.csv", "tiendas.csv", 
                "clientes.csv", "compras.csv", "comuna_region.csv", "despachos.csv", 
                "jefes.csv", "licencias.csv", "repartidores.csv", "vehiculos.csv"]

for archivo in archivos_csv:
    with open(archivo, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Omitir la primera fila
        for fila in reader:
            # Eliminar filas repetidas:
            if archivo == archivos_csv[0]:
                if fila not in cajas:
                    cajas.append(fila)
            elif archivo == archivos_csv[1]:
                if fila not in personal:
                    personal.append(fila)
            elif archivo == archivos_csv[2]:
                if fila not in productos:
                    productos.append(fila)
            elif archivo == archivos_csv[3]:
                if fila not in stock:
                    stock.append(fila)
            elif archivo == archivos_csv[4]:
                if fila not in tiendas:
                    tiendas.append(fila)
            elif archivo == archivos_csv[5]:
                if fila not in clientes:
                    clientes.append(fila)
            elif archivo == archivos_csv[6]:
                if fila not in compras:
                    compras.append(fila)
            elif archivo == archivos_csv[7]:
                if fila not in comuna_region:
                    comuna_region.append(fila)
            elif archivo == archivos_csv[8]:
                if fila not in despachos:
                    despachos.append(fila)
            elif archivo == archivos_csv[9]:
                if fila not in jefes:
                    jefes.append(fila)
            elif archivo == archivos_csv[10]:
                if fila not in licencias:
                    licencias.append(fila)
            elif archivo == archivos_csv[11]:
                if fila not in repartidores:
                    repartidores.append(fila)
            elif archivo == archivos_csv[12]:
                if fila not in vehiculos:
                    vehiculos.append(fila)
            

# --- PROCESAR CAJAS --- header: id_caja, tipo_caja, id_producto, peso, descripcion
i = 0
cajas = sorted(cajas, key=lambda fila : fila[1]) # Ordenar por id_producto
for fila in cajas:
    if fila[3] == "Fragil":
        fila[3] = 1 # Si es "Fragil" se le asigna un 1
    else:
        fila[3] = 0 # Si es "Sin descripcion" se le asigna un 0
    fila.insert(0, i) # Agregar id_caja
    i = i + 1
header_cajas = ["id_caja", "tipo_caja", "id_producto", "peso", "descripcion"]

# --- PROCESAR JEFES --- header: id_tienda, id_personal
jefes = sorted(jefes, key=lambda fila : fila[1]) # Ordenar por id_personal
for fila in jefes: # Cambiar el orden de las columnas
    id_tienda = fila[0]
    id_personal = fila[1]
    fila[0] = id_personal
    fila[1] = id_tienda
header_jefes = ["id_personal", "id_tienda"]

# --- PROCESAR PERSONAL --- header: id_personal, nombre, rut, edad, genero, fecha_inicio, cargo, id_tienda
personal = sorted(personal, key=lambda fila : fila[0]) # Ordenar por id_personal
for fila in personal:
    if fila[4] == "Female":
        fila[4] = 1 # Si es "Female" se le asigna un 1
    else:
        fila[4] = 0 # Si es "Male" se le asigna un 0
    
    fila.append("Empleado") # Agregar columna cargo
    fila.append("NULL") # Agregar columna id_tienda

    # Convertir fecha_inicio a formato datetime
    fecha = fila[5]
    fecha_mal = datetime.strptime(fecha,"%d/%m/%Y")
    fecha_bien  = fecha_mal.strftime("%Y%m%d")
    fila[5] = fecha_bien
    for jefe in jefes:
        if fila[0] == jefe[0]:
            fila[6] = "Jefe"
            fila[7] = jefe[1]
    for repartidor in repartidores:
        if fila[6] == "Empleado":
            if fila[0] == repartidor[0] and repartidor[6] == "YES":
                fila[6] = "Chofer"
            if fila[0] == repartidor[0] and repartidor[6] == "NO":
                fila[6] = "Repartidor"

i = 0
for fila in personal:
    if fila[7] == "NULL":
        fila[7] = i
        if i < len(tiendas):
            i = i + 1
        else:
            i = 0    
header_personal = ["id_personal", "nombre", "rut", "edad", "genero", "fecha_inicio", "cargo", "id_tienda"]


# --- PROCESAR PRODUCTOS --- header: id_producto, nombre, precio, numero_cajas (preguntar si agregar tipo)
for i in range (len(productos)):
    fila = productos[i]
    fila = list(filter(bool, fila))
    if fila[4] == "living":
        liv = [fila[0], fila[5], fila[6], fila[7]] # id_producto, dimensiones, material, carga
        living.append(liv)
    elif fila[4] == "dormitorio":
        if fila[7] == "Uno de los productos mas vendidos":
            fila[7] = 1
        else:
            fila[7] = 0
        dor = [fila[0], fila[5], fila[6], fila[7]] # id_producto, tamaño, color, descripcion 
        # (Si es uno de los productos mas vendidos = 1, Si es Sin descripcion = 0)
        dormitorio.append(dor)
    elif fila[4] == "iluminacion":
        ilu = [fila[0], fila[5], fila[7], fila[8], fila[9]] # id_producto, color, frecuencia de trabajo, potencia y tension.
        iluminacion.append(ilu)
    prod = fila[0:4] # Eliminar columnas innecesarias
    productos[i] = prod
    i = i + 1

header_productos = ["id_producto", "nombre", "precio", "numero_cajas", "categoria"]
header_living = ["id_producto", "dimensiones", "material", "carga"]
header_dormitorio = ["id_producto", "tamaño", "color", "descripcion"]
header_iluminacion = ["id_producto", "color", "frecuencia de trabajo", "potencia", "tension"]
    
# Ordenar por id_producto  
productos = sorted(productos, key=lambda fila : fila[0])
living = sorted(living, key=lambda fila : fila[0])
dormitorio = sorted(dormitorio, key=lambda fila : fila[0])
iluminacion = sorted(iluminacion, key=lambda fila : fila[0])


# --- PROCESAR STOCK --- header: id_stock, id_tienda, id_producto, cantidad, descuento
i = 0
stock = sorted(stock, key=lambda fila : fila[0]) # Ordenar por id_tienda
for fila in stock:
    fila.insert(0, i) # Agregar id_stock
    i = i + 1
header_stock = ["id_stock", "id_tienda", "id_producto", "cantidad", "descuento"]

# --- PROCESAR TIENDAS --- header: id_tienda, telefono, calle, numero, comuna, region, capacidad_estacionamiento
tiendas = sorted(tiendas, key=lambda fila : fila[0]) # Ordenar por id_tienda
header_tiendas = ["id_tienda", "telefono", "calle", "numero", "comuna", "region", "capacidad_estacionamiento"]

# --- PROCESAR REPARTIDORES --- header: id_personal, id_chofer_vehiculo
repartidores = sorted(repartidores, key=lambda fila : fila[5]) # Ordenar por id_chofer_vehiculo
for i in range(len(repartidores)): # sacar info repetida
    fila = repartidores[i]
    repartidores[i] = [fila[5], fila[0]]
header_repartidores = ["id_personal", "id_chofer_vehiculo"]


# SOBREESCRIBIR ARCHIVOS

#--- SOBREESCRIBIR PERSONAL ---
with open("personal.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_personal)
    writer.writerows(personal)

# --- SOBREESCRIBIR PRODUCTOS ---
with open("productos.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_productos)
    writer.writerows(productos)

# --- SOBREESCRIBIR LIVING ---
with open("living.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_living)
    writer.writerows(living)

# --- SOBREESCRIBIR DORMITORIO ---
with open("dormitorio.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_dormitorio)
    writer.writerows(dormitorio)

# --- SOBREESCRIBIR ILUMINACION ---
with open("iluminacion.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_iluminacion)
    writer.writerows(iluminacion)

# --- SOBREESCRIBIR STOCK ---
with open("stock.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_stock)
    writer.writerows(stock)

# --- SOBREESCRIBIR TIENDAS ---
with open("tiendas.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_tiendas)
    writer.writerows(tiendas)

# --- SOBREESCRIBIR REPARTIDORES ---
with open("repartidores.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_repartidores)
    writer.writerows(repartidores)

# --- SOBREESCRIBIR CAJAS ---
with open("cajas.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_cajas)
    writer.writerows(cajas)

# --- SOBREESCRIBIR JEFES ---
with open("jefes.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(header_jefes)
    writer.writerows(jefes)

# testing
#for i in range(1000):
    #print(cajas[i])
    #print(personal[i])
    #print(productos[i])
    #print(living[i])
    #print(dormitorio[i])
    #print(iluminacion[i])
    #print(tiendas[i])