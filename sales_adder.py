import pandas as pd

# Cargar los datos
items = pd.read_csv('data_items.csv')
sales = pd.read_csv('data_sales.csv', sep=';')

# Calcular el total de ventas y número de ventas por item_id
ventas_por_item = sales.groupby('item_id').agg({
    'total (CLP)': 'sum',
    'quantity': 'sum'
}).reset_index()

# Combinar con la información de los items
resultado = pd.merge(items[['item_id', 'description']], ventas_por_item, on='item_id', how='left')

# Rellenar con 0 las ventas y cantidades de items que no tienen ventas
resultado['total (CLP)'] = resultado['total (CLP)'].fillna(0)
resultado['quantity'] = resultado['quantity'].fillna(0)

# Renombrar columnas para mayor claridad
resultado = resultado.rename(columns={
    'item_id': 'ID del item',
    'description': 'Nombre del item',
    'total (CLP)': 'Total de ventas (CLP)',
    'quantity': 'Cantidad vendida'
})

# Ordenar por total de ventas de mayor a menor
resultado = resultado.sort_values('Total de ventas (CLP)', ascending=False)

# Guardar el resultado en un archivo CSV
resultado.to_csv('ventas_totales_por_item.csv', index=False)

print("El archivo 'ventas_totales_por_item.csv' ha sido creado exitosamente.")