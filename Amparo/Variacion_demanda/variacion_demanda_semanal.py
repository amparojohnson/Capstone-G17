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

# Agrupar por producto y semana para calcular la cantidad total vendida por semana para cada archivo
weekly_sales_2020 = sales_2020.groupby(['item_id', 'year_week'])['quantity'].sum().reset_index()
weekly_sales_2021 = sales_2021.groupby(['item_id', 'year_week'])['quantity'].sum().reset_index()
weekly_sales_2022 = sales_2022.groupby(['item_id', 'year_week'])['quantity'].sum().reset_index()
weekly_sales_2023 = sales_2023.groupby(['item_id', 'year_week'])['quantity'].sum().reset_index()
weekly_sales_2024 = sales_2024.groupby(['item_id', 'year_week'])['quantity'].sum().reset_index()

# Calcular la variación porcentual semana a semana por producto para cada archivo (en valor absoluto)
weekly_sales_2020['pct_change'] = weekly_sales_2020.groupby('item_id')['quantity'].pct_change().abs()
weekly_sales_2021['pct_change'] = weekly_sales_2021.groupby('item_id')['quantity'].pct_change().abs()
weekly_sales_2022['pct_change'] = weekly_sales_2022.groupby('item_id')['quantity'].pct_change().abs()
weekly_sales_2023['pct_change'] = weekly_sales_2023.groupby('item_id')['quantity'].pct_change().abs()
weekly_sales_2024['pct_change'] = weekly_sales_2024.groupby('item_id')['quantity'].pct_change().abs()

# Calcular la variación porcentual promedio por producto (ignorando NaN), para cada archivo por separado
average_pct_change_2020 = weekly_sales_2020.groupby('item_id')['pct_change'].mean().reset_index()
average_pct_change_2021 = weekly_sales_2021.groupby('item_id')['pct_change'].mean().reset_index()
average_pct_change_2022 = weekly_sales_2022.groupby('item_id')['pct_change'].mean().reset_index()
average_pct_change_2023 = weekly_sales_2023.groupby('item_id')['pct_change'].mean().reset_index()
average_pct_change_2024 = weekly_sales_2024.groupby('item_id')['pct_change'].mean().reset_index()

# Renombrar columnas para mayor claridad
average_pct_change_2020.columns = ['item_id', 'average_pct_change_2020']
average_pct_change_2021.columns = ['item_id', 'average_pct_change_2021']
average_pct_change_2022.columns = ['item_id', 'average_pct_change_2022']
average_pct_change_2023.columns = ['item_id', 'average_pct_change_2023']
average_pct_change_2024.columns = ['item_id', 'average_pct_change_2024']

# Identificar los 10 productos con mayor variación porcentual promedio entre semanas para cada archivo
most_variable_products_2020 = average_pct_change_2020.sort_values(by='average_pct_change_2020', ascending=False).head(10)
most_variable_products_2021 = average_pct_change_2021.sort_values(by='average_pct_change_2021', ascending=False).head(10)
most_variable_products_2022 = average_pct_change_2022.sort_values(by='average_pct_change_2022', ascending=False).head(10)
most_variable_products_2023 = average_pct_change_2023.sort_values(by='average_pct_change_2023', ascending=False).head(10)
most_variable_products_2024 = average_pct_change_2024.sort_values(by='average_pct_change_2024', ascending=False).head(10)

# # Escribir resultados en un csv
# most_variable_products_2020.to_csv('most_variable_products_2020.csv', index=False)
# most_variable_products_2021.to_csv('most_variable_products_2021.csv', index=False)
# most_variable_products_2022.to_csv('most_variable_products_2022.csv', index=False)
# most_variable_products_2023.to_csv('most_variable_products_2023.csv', index=False)
# most_variable_products_2024.to_csv('most_variable_products_2024.csv', index=False)

# Identificar productos con variación de demanda =0 entre semanas para cada archivo
least_variable_products_2020 = average_pct_change_2020[average_pct_change_2020['average_pct_change_2020'] == 0]
least_variable_products_2021 = average_pct_change_2021[average_pct_change_2021['average_pct_change_2021'] == 0]
least_variable_products_2022 = average_pct_change_2022[average_pct_change_2022['average_pct_change_2022'] == 0]
least_variable_products_2023 = average_pct_change_2023[average_pct_change_2023['average_pct_change_2023'] == 0]
least_variable_products_2024 = average_pct_change_2024[average_pct_change_2024['average_pct_change_2024'] == 0]

# Escribir resultados en un csv
# least_variable_products_2020.to_csv('least_variable_products_2020.csv', index=False)
# least_variable_products_2021.to_csv('least_variable_products_2021.csv', index=False)
# least_variable_products_2022.to_csv('least_variable_products_2022.csv', index=False)
# least_variable_products_2023.to_csv('least_variable_products_2023.csv', index=False)
# least_variable_products_2024.to_csv('least_variable_products_2024.csv', index=False)
