import pandas as pd
import matplotlib.pyplot as plt 

# Cargar datos
items = pd.read_csv('data_items.csv')
sales = pd.read_csv('data_sales.csv', delimiter=';')

# Eliminar duplicados en datos de productos
items = items.drop_duplicates()

### Separación de productos por demanda anual ###

# Convertir la columna de fecha a tipo datetime
sales['date'] = pd.to_datetime(sales['date'])
# Unir datos de ventas con datos de productos
sales_items = sales.merge(items[['item_id', 'description', 'description_2', 'group_description']], on='item_id', how='left')

# Separar ventas por año 
sales_items['year'] = sales_items['date'].dt.year


# Crear un archivo csv por cada año con las ventas de ese año sólo con las columnas item_id, description, description_2, group_description, quantity
# for year in sales_items['year'].unique():
#     sales_year = sales_items[sales_items['year'] == year]
#     sales_year = sales_year[['item_id', 'description', 'description_2', 'group_description', 'date', 'quantity', 'unit_sale_price (CLP)', 'total (CLP)', 'client_id']]
#     sales_year.to_csv(f'sales_{year}.csv', index=False)


### Identificar productos con demanda más variable entre semanas ###

# Año 2020:
sales_2020 = pd.read_csv('Amparo/sales_2020.csv')
# Año 2021:
sales_2021 = pd.read_csv('Amparo/sales_2021.csv')
# Año 2022:
sales_2022 = pd.read_csv('Amparo/sales_2022.csv')
# Año 2023:
sales_2023 = pd.read_csv('Amparo/sales_2023.csv')
# Año 2024:
sales_2024 = pd.read_csv('Amparo/sales_2024.csv')

# Convertir la columna de fecha a tipo datetime para cada archivo
sales_2020['date'] = pd.to_datetime(sales_2020['date'])
sales_2021['date'] = pd.to_datetime(sales_2021['date'])
sales_2022['date'] = pd.to_datetime(sales_2022['date'])
sales_2023['date'] = pd.to_datetime(sales_2023['date'])
sales_2024['date'] = pd.to_datetime(sales_2024['date'])

# Crear una columna para la semana del año para cada archivo
sales_2020['year_week'] = sales_2020['date'].dt.strftime('%G-%V')
sales_2021['year_week'] = sales_2021['date'].dt.strftime('%G-%V')
sales_2022['year_week'] = sales_2022['date'].dt.strftime('%G-%V')
sales_2023['year_week'] = sales_2023['date'].dt.strftime('%G-%V')
sales_2024['year_week'] = sales_2024['date'].dt.strftime('%G-%V')

### Identificar meses de mayor y menor demanda de cada producto para cada archivo ###

# Crear una columna para el mes del año para cada archivo
sales_2020['month'] = sales_2020['date'].dt.month
sales_2021['month'] = sales_2021['date'].dt.month
sales_2022['month'] = sales_2022['date'].dt.month
sales_2023['month'] = sales_2023['date'].dt.month
sales_2024['month'] = sales_2024['date'].dt.month

### DEMANDA MENSUAL ### (ordenada de mayor a menor)
monthly_sales_2020 = sales_2020.groupby(['item_id', 'description', 'description_2', 'group_description', 'month'])['quantity'].sum().reset_index().sorted_by('quantity', ascending=False)
monthly_sales_2021 = sales_2021.groupby(['item_id', 'description', 'description_2', 'group_description', 'month'])['quantity'].sum().reset_index().sorted_by('quantity', ascending=False)
monthly_sales_2022 = sales_2022.groupby(['item_id', 'description', 'description_2', 'group_description', 'month'])['quantity'].sum().reset_index().sorted_by('quantity', ascending=False)
monthly_sales_2023 = sales_2023.groupby(['item_id', 'description', 'description_2', 'group_description', 'month'])['quantity'].sum().reset_index().sorted_by('quantity', ascending=False)
monthly_sales_2024 = sales_2024.groupby(['item_id', 'description', 'description_2', 'group_description', 'month'])['quantity'].sum().reset_index().sorted_by('quantity', ascending=False)

# Calcular meses de mayor y menor demanda total (todos los productos) para cada archivo
max_demand_month_2020 = monthly_sales_2020.groupby('month')['quantity'].sum().idxmax()
min_demand_month_2020 = monthly_sales_2020.groupby('month')['quantity'].sum().idxmin()
max_demand_month_2021 = monthly_sales_2021.groupby('month')['quantity'].sum().idxmax()
min_demand_month_2021 = monthly_sales_2021.groupby('month')['quantity'].sum().idxmin()
max_demand_month_2022 = monthly_sales_2022.groupby('month')['quantity'].sum().idxmax()
min_demand_month_2022 = monthly_sales_2022.groupby('month')['quantity'].sum().idxmin()
max_demand_month_2023 = monthly_sales_2023.groupby('month')['quantity'].sum().idxmax()
min_demand_month_2023 = monthly_sales_2023.groupby('month')['quantity'].sum().idxmin()
max_demand_month_2024 = monthly_sales_2024.groupby('month')['quantity'].sum().idxmax()
min_demand_month_2024 = monthly_sales_2024.groupby('month')['quantity'].sum().idxmin()

# Escribir resultados en un csv con las columnas: year, max_demand_month, min_demand_month
# demand_months = pd.DataFrame({
#     'year': [2020, 2021, 2022, 2023, 2024],
#     'max_demand_month': [max_demand_month_2020, max_demand_month_2021, max_demand_month_2022, max_demand_month_2023, max_demand_month_2024],
#     'min_demand_month': [min_demand_month_2020, min_demand_month_2021, min_demand_month_2022, min_demand_month_2023, min_demand_month_2024]
# })
# demand_months.to_csv('demand_months.csv', index=False)


# ### Identificar meses de mayor demanda de un producto específico ###

# # Definir el producto, categoría o subcategoría de interés
# item_id = 0  # Ejemplo: ID del producto
# description = ''  # Ejemplo: Categoría
# description_2 = ''  # Ejemplo: Subcategoría
# group_description = ''  # Ejemplo: Categoría
# year = 0  # Ejemplo: sales_2020

# # Filtrar datos por producto, categoría y/o subcategoría
# filtered_sales = year[
#     (year['item_id'] == item_id) | 
#     (year['description'] == description) | 
#     (year['description_2'] == description_2) |
#     (year['group_description'] == group_description)
# ]

# # Agrupar por año y mes y sumar la cantidad vendida
# monthly_demand = filtered_sales.groupby('month')['quantity'].sum().reset_index()

# # Ordenar por cantidad vendida en orden descendente para encontrar los meses con mayor demanda
# monthly_demand_sorted = monthly_demand.sort_values(by='quantity', ascending=False)

# # Mostrar los meses con mayor demanda
# print("Meses con mayor demanda:")
# print(monthly_demand_sorted)


















