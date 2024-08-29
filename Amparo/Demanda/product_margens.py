import pandas as pd
import matplotlib.pyplot as plt 

# Cargar datos
items = pd.read_csv('data_items.csv')
sales = pd.read_csv('data_sales.csv', delimiter=';')

# Eliminar duplicados en datos de productos
items = items.drop_duplicates()

## productos con mayores y menores márgenes de ganancia ##

# Calcular el margen de ganancia por producto (unit_sale_price (CLP) - cost (CLP))
items['profit_margin'] = items['unit_sale_price (CLP)'] - items['cost (CLP)']
# Ordenar productos por margen de ganancia
items_dec = items.sort_values(by='profit_margin', ascending=False).head(15)
items_inc = items.sort_values(by='profit_margin', ascending=True).head(15)

# Imprimir los productos con mayor y menor margen de ganancia
print('Productos con mayor margen de ganancia:')
print(items_dec)
print('\nProductos con menor margen de ganancia:')
print(items_inc)


### Productos con mayores y menores márgenes que realmente se venden ###

# Unir datos de ventas con datos de productos
sales_items = sales.merge(items, on='item_id')

# Agrupar por producto y calcular el margen de ganancia promedio (no se consideran costos de almacenamiento y orden)
profit_margin_by_product = sales_items.groupby('description')['profit_margin'].mean().reset_index()

# Encontrar los productos con mayor margen de ganancia
top_products_by_margin = profit_margin_by_product.sort_values(by='profit_margin', ascending=False).head(10)
# Encontrar los productos con menor margen de ganancia
bottom_products_by_margin = profit_margin_by_product.sort_values(by='profit_margin', ascending=True).head(10)

# Imprimir resultados
print('Productos con mayor margen de ganancia promedio por ventas:')
print(top_products_by_margin)
print('\nProductos con menor margen de ganancia promedio por ventas:')
print(bottom_products_by_margin)

# Crear un solo gráfico de barras comparando los productos con mayor margen de ganancia y mayor margen de ganancia promedio
# plt.figure(figsize=(12, 6))
# plt.barh(items_dec['description'], items_dec['profit_margin'], color='skyblue', label='Margen de ganancia por producto')
# plt.barh(top_products_by_margin['description'], top_products_by_margin['profit_margin'], color='orange', label='Margen de ganancia promedio por ventas')
# plt.xlabel('Margen de ganancia (CLP)')
# plt.ylabel('Producto')
# plt.title('Comparación de productos con mayor margen de ganancia y mayor margen de ganancia promedio')
# plt.legend()
# plt.tight_layout()
# plt.show()

# # Guardar gráfico
# plt.savefig('top_products_by_margin.png')

plt.figure(figsize=(10, 6))
plt.scatter(items_dec['description'], items_dec['profit_margin'], color='blue', label='Productos con mayor margen de ganancia')
plt.scatter(top_products_by_margin['description'], top_products_by_margin['profit_margin'], color='green', label='Productos con mayor margen de ganancia promedio')
plt.scatter(items_inc['description'], items_inc['profit_margin'], color='red', label='Productos con menor margen de ganancia')
plt.scatter(bottom_products_by_margin['description'], bottom_products_by_margin['profit_margin'], color='orange', label='Productos con menor margen de ganancia promedio')
plt.xticks(rotation=90)
plt.xlabel('Producto')
plt.ylabel('Margen de ganancia (CLP)')
plt.title('Comparación margen por producto y margen promedio por ventas')
plt.legend()
plt.tight_layout()
plt.show()

# Guardar gráfico
plt.savefig('top_bottom_products_by_margin.png')





