import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta
import time
import sys

def print_and_flush(message):
    print(message)
    sys.stdout.flush()

print_and_flush("Script iniciado.")

# Directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
print_and_flush(f"Directorio actual: {current_dir}")

try:
    print_and_flush("Cargando datos...")
    # Cargar datos
    df_items = pd.read_csv(os.path.join(current_dir, 'data_items.csv'))
    print_and_flush(f"data_items.csv cargado. Shape: {df_items.shape}")
    
    df_purchases = pd.read_csv(os.path.join(current_dir, 'data_purchases.csv'), sep=';')
    print_and_flush(f"data_purchases.csv cargado. Shape: {df_purchases.shape}")
    
    df_sales = pd.read_csv(os.path.join(current_dir, 'data_sales.csv'), sep=';')
    print_and_flush(f"data_sales.csv cargado. Shape: {df_sales.shape}")

    print_and_flush("Convirtiendo fechas...")
    # Convertir fechas a datetime
    df_purchases['date'] = pd.to_datetime(df_purchases['date'])
    df_purchases['delivery_date'] = pd.to_datetime(df_purchases['delivery_date'])
    df_sales['date'] = pd.to_datetime(df_sales['date'])

    # Función para calcular el inventario diario
    def calculate_daily_inventory(item_id, start_date, end_date):
        dates = pd.date_range(start=start_date, end=end_date)
        inventory = pd.Series(index=dates, dtype=float)
        
        initial_stock = df_items.loc[df_items['item_id'] == item_id, 'stock'].values[0]
        inventory.iloc[0] = initial_stock
        
        purchases = df_purchases[df_purchases['item_id'] == item_id]
        sales = df_sales[df_sales['item_id'] == item_id]
        
        for date in dates[1:]:
            prev_inventory = inventory.loc[date - timedelta(days=1)]
            day_sales = sales[sales['date'].dt.date == date.date()]['quantity'].sum()
            day_purchases = purchases[purchases['delivery_date'].dt.date == date.date()]['quantity'].sum()
            
            inventory.loc[date] = prev_inventory - day_sales + day_purchases
        
        return inventory

    print_and_flush("Calculando inventario diario para todos los productos...")
    # Calcular inventario diario para todos los productos
    start_date = min(df_sales['date'].min(), df_purchases['date'].min())
    end_date = max(df_sales['date'].max(), df_purchases['delivery_date'].max())

    all_inventory = {}
    total_items = len(df_items['item_id'])
    for i, item_id in enumerate(df_items['item_id'], 1):
        if i % 10 == 0 or i == total_items:
            print_and_flush(f"Procesando item {i} de {total_items}...")
        all_inventory[item_id] = calculate_daily_inventory(item_id, start_date, end_date)

    print_and_flush("Creando DataFrame con inventario diario...")
    # Crear DataFrame con inventario diario
    df_daily_inventory = pd.DataFrame(all_inventory)
    df_daily_inventory.to_csv(os.path.join(current_dir, 'inventario_diario.csv'))

    print_and_flush("Creando DataFrame con inventario mensual...")
    # Crear DataFrame con inventario mensual
    df_monthly_inventory = df_daily_inventory.resample('M').last()
    df_monthly_inventory.to_csv(os.path.join(current_dir, 'inventario_mensual.csv'))

    print_and_flush("Identificando quiebres de stock...")
    # Identificar quiebres de stock
    df_stock_breaks = (df_daily_inventory <= 0).astype(int)

    print_and_flush("Uniendo con información de categoría...")
    # Unir con información de categoría
    df_items_category = df_items[['item_id', 'group_description']]
    df_stock_breaks_with_category = df_stock_breaks.reset_index().melt(id_vars='index', var_name='item_id', value_name='stock_break')
    df_stock_breaks_with_category = pd.merge(df_stock_breaks_with_category, df_items_category, on='item_id', how='left')
    df_stock_breaks_with_category = df_stock_breaks_with_category[df_stock_breaks_with_category['stock_break'] == 1]

    print_and_flush("Analizando categorías de producto...")
    # 1. Categoría de producto que más se queda sin stock
    category_stock_breaks = df_stock_breaks_with_category.groupby('group_description').size().sort_values(ascending=False)
    print_and_flush("Categorías de producto con más quiebres de stock:")
    print_and_flush(str(category_stock_breaks))

    plt.figure(figsize=(12, 6))
    category_stock_breaks.plot(kind='bar')
    plt.title('Número de Quiebres de Stock por Categoría')
    plt.xlabel('Categoría')
    plt.ylabel('Número de Quiebres')
    plt.tight_layout()
    plt.savefig(os.path.join(current_dir, 'quiebres_por_categoria.png'))
    plt.close()

    print_and_flush("Analizando productos...")
    # 2. Producto que se queda más sin stock
    product_stock_breaks = df_stock_breaks_with_category.groupby('item_id').size().sort_values(ascending=False)
    print_and_flush("\nProductos con más quiebres de stock:")
    print_and_flush(str(product_stock_breaks.head(10)))

    plt.figure(figsize=(12, 6))
    product_stock_breaks.head(20).plot(kind='bar')
    plt.title('Top 20 Productos con Más Quiebres de Stock')
    plt.xlabel('ID del Producto')
    plt.ylabel('Número de Quiebres')
    plt.tight_layout()
    plt.savefig(os.path.join(current_dir, 'top_20_productos_quiebres.png'))
    plt.close()

    print_and_flush("Analizando frecuencia de quiebres por mes...")
    # 3. Frecuencia de quiebre de stock por mes
    df_stock_breaks_with_category['date'] = pd.to_datetime(df_stock_breaks_with_category['index'])
    df_stock_breaks_with_category['year_month'] = df_stock_breaks_with_category['date'].dt.to_period('M')
    monthly_stock_breaks = df_stock_breaks_with_category.groupby('year_month').size().sort_index()
    print_and_flush("\nFrecuencia de quiebres de stock por mes:")
    print_and_flush(str(monthly_stock_breaks))

    plt.figure(figsize=(12, 6))
    monthly_stock_breaks.plot(kind='line', marker='o')
    plt.title('Frecuencia de Quiebres de Stock por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Número de Quiebres')
    plt.tight_layout()
    plt.savefig(os.path.join(current_dir, 'quiebres_por_mes.png'))
    plt.close()

    print_and_flush("Guardando resultados en CSV...")
    # Guardar resultados en CSV
    category_stock_breaks.to_csv(os.path.join(current_dir, 'quiebres_por_categoria.csv'))
    product_stock_breaks.head(20).to_csv(os.path.join(current_dir, 'top_20_productos_quiebres.csv'))
    monthly_stock_breaks.to_csv(os.path.join(current_dir, 'quiebres_por_mes.csv'))

    print_and_flush("\nAnálisis completado. Se han generado gráficos y archivos CSV con los resultados.")

except Exception as e:
    print_and_flush(f"Se produjo un error: {str(e)}")
    import traceback
    print_and_flush(traceback.format_exc())

print_and_flush("Script finalizado.")