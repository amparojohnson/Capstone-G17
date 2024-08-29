import pandas as pd

### Productos más vendidos por categoría ###

# Cargar datos
items = pd.read_csv('data_items.csv')
sales = pd.read_csv('data_sales.csv', delimiter=';')

# Eliminar duplicados en datos de productos
items = items.drop_duplicates()

# Unir datos de ventas con datos de productos
sales_items = sales.merge(items[['item_id', 'description', 'description_2', 'group_description']], on='item_id', how='left')

# 1. Demanda total por producto
# Agrupar por producto (manteniendo el item_id y las otras columnas) y calcular la cantidad total vendida
total_sales_by_product = sales_items.groupby('item_id').agg({'quantity': 'sum'}).reset_index()
# Ordenar productos por cantidad total vendida
total_sales_by_product = total_sales_by_product.sort_values(by='quantity', ascending=False)
# Imprimir los productos con mayor cantidad total vendida
print(total_sales_by_product)

# 2. Demanda total por categoría 'description_2'
# Agrupar por categoría y calcular la cantidad total vendida
total_sales_by_sub_category = sales_items.groupby('description_2').agg({'quantity': 'sum'}).reset_index()
# Ordenar categorías por cantidad total vendida
total_sales_by_sub_category = total_sales_by_sub_category.sort_values(by='quantity', ascending=False)
# Imprimir las categorías con mayor cantidad total vendida
print(total_sales_by_sub_category)

# 3. Demanda total por categoría 'group_description'
# Agrupar por categoría y calcular la cantidad total vendida
total_sales_by_category = sales_items.groupby('group_description').agg({'quantity': 'sum'}).reset_index()
# Ordenar categorías por cantidad total vendida
total_sales_by_category = total_sales_by_category.sort_values(by='quantity', ascending=False)
# Imprimir las categorías con mayor cantidad total vendida
print(total_sales_by_category)