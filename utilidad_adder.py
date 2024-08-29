import pandas as pd

# Cargar los datos
items = pd.read_csv('items_fitrado_costos_y_ventas.csv')
sales = pd.read_csv('data_sales.csv', sep=';')
purchases = pd.read_csv('data_purchases.csv', sep=';')

# Calcular ingresos totales
ingresos = sales['total (CLP)'].sum()

# Calcular el costo de los productos vendidos
ventas_con_costo = pd.merge(sales, items[['item_id', 'cost (CLP)']], on='item_id', how='left')
costo_productos_vendidos = (ventas_con_costo['quantity'] * ventas_con_costo['cost (CLP)']).sum()

# Calcular utilidad bruta
utilidad_bruta = ingresos - costo_productos_vendidos

# Estimar otros costos (esto es una aproximación y puede necesitar ajustes)
costos_almacenamiento = items['storage_cost (CLP)'].sum() * 12  # Asumiendo costo mensual por 12 meses

# Calcular utilidad estimada
utilidad_estimada = utilidad_bruta - costos_almacenamiento

# Crear un DataFrame con los resultados
resultados = pd.DataFrame({
    'Métrica': ['Ingresos Totales', 'Costo de Productos Vendidos', 'Utilidad Bruta', 
                'Costos de Almacenamiento (estimados)', 'Utilidad Estimada'],
    'Valor (CLP)': [ingresos, costo_productos_vendidos, utilidad_bruta, 
                    costos_almacenamiento, utilidad_estimada]
})

# Guardar resultados en un archivo CSV
resultados.to_csv('estimacion_utilidad_tienda.csv', index=False)

print("El archivo 'estimacion_utilidad_tienda.csv' ha sido creado con la estimación de utilidad.")

# Imprimir un resumen en la consola
print("\nResumen de Estimación de Utilidad:")
print(f"Ingresos Totales: {ingresos:,.0f} CLP")
print(f"Costo de Productos Vendidos: {costo_productos_vendidos:,.0f} CLP")
print(f"Utilidad Bruta: {utilidad_bruta:,.0f} CLP")
print(f"Costos de Almacenamiento (estimados): {costos_almacenamiento:,.0f} CLP")
print(f"Utilidad Estimada: {utilidad_estimada:,.0f} CLP")