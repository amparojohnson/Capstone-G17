import pandas as pd
import matplotlib.pyplot as plt 

# Cargar datos
items = pd.read_csv('data_items.csv')
sales = pd.read_csv('data_sales.csv', delimiter=';')

# Eliminar duplicados en datos de productos
items = items.drop_duplicates()

### Demanda por categoría de productos mes a mes ####

# # Convertir la columna de fecha a tipo datetime
sales['date'] = pd.to_datetime(sales['date'])
# Extraer el año y mes de la fecha de venta
sales['year_month'] = sales['date'].dt.to_period('M')
# Unir datos de ventas con datos de productos
sales_items = sales.merge(items[['item_id', 'group_description']], on='item_id')

# Agrupar por categoría y mes, y sumar la cantidad vendida
demand_by_category_month = sales_items.groupby(['group_description', 'year_month'])['quantity'].sum().reset_index()

# Crear una tabla pivot para que cada categoría tenga su propia columna
demand_pivot = demand_by_category_month.pivot(index='year_month', columns='group_description', values='quantity').fillna(0)

### Corrección de nombres de categorías ###
# Fusionar las demandas de las categorías "medicamento" y "medicamentos"
demand_pivot['medicamentos'] = demand_pivot['medicamento'] + demand_pivot['medicamentos']
# Fusionar las demandas de las categorías "accesorio" y "accesorios"
demand_pivot['accesorios'] = demand_pivot['accesorio'] + demand_pivot['accesorios']

# Graficar la demanda por categoría mes a mes (categorías: medicamentos, accesorios, alimento)
# demand_pivot[['medicamentos', 'accesorios', 'alimento']].plot(kind='line', marker='o')
# plt.title('Demanda por categoría de productos')
# plt.xlabel('Mes')
# plt.ylabel('Cantidad vendida')
# plt.grid()
# plt.show()



















