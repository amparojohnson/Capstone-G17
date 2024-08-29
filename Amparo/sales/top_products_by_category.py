import pandas as pd

### Productos más vendidos por categoría ###

# Cargar datos
items = pd.read_csv('data_items.csv')
sales = pd.read_csv('data_sales.csv', delimiter=';')

# Eliminar duplicados en datos de productos
items = items.drop_duplicates()

# Unir datos de ventas con datos de productos
sales_items = sales.merge(items, on='item_id')

# Agrupar por categoría y producto, y calcular el total vendido
sales_summary = sales_items.groupby(['description_2','group_description', 'description'])['total (CLP)'].sum().reset_index()

# Encontrar el producto con mayor venta en cada categoría
top_products_by_category = sales_summary.loc[sales_summary.groupby('description_2')['total (CLP)'].idxmax()]

# Ordenar resultados por total de ventas
top_products_by_category = top_products_by_category.sort_values(by='total (CLP)', ascending=False)

# Escribir resultados en un csv
top_products_by_category.to_csv('top_products_by_sub_category.csv', index=False)



