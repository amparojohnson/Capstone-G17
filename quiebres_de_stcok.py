import pandas as pd

# Leer los archivos CSV
data_purchases = pd.read_csv('data_purchases.csv', sep=';')
data_sales = pd.read_csv('data_sales.csv', sep=';')
data_items = pd.read_csv('items_filtrados_stock.csv', sep=',')

# Convertir las columnas de fecha a tipo datetime
data_purchases['date'] = pd.to_datetime(data_purchases['date'])
data_purchases['delivery_date'] = pd.to_datetime(data_purchases['delivery_date'])
data_sales['date'] = pd.to_datetime(data_sales['date'])

# Unir los dataframes de compras y ventas por item_id y date
merged_data = pd.merge(data_purchases, data_sales, on=['item_id', 'date'], how='outer')


# Calcular el stock actual para cada item y fecha
merged_data['stock'] = merged_data.groupby('item_id')['quantity_x'].cumsum() - merged_data.groupby('item_id')['quantity_y'].cumsum()

# Unir con el dataframe de items para obtener el stock inicial
merged_data = pd.merge(merged_data, data_items[['item_id', 'stock']], on='item_id', how='left')
merged_data.rename(columns={'stock_x': 'current_stock', 'stock_y': 'initial_stock'}, inplace=True)

# Calcular el stock total para cada fila
merged_data['total_stock'] = merged_data['initial_stock'] + merged_data['current_stock']

# Identificar las filas donde el stock total es menor o igual a 0
stockouts = merged_data[merged_data['total_stock'] <= 0]

# Mostrar las fechas y los items donde ocurrieron quiebres de stock
print("Quiebres de stock:")
for _, row in stockouts.iterrows():
    print(f"Item: {row['item_id']}, Fecha: {row['date']}")
    
