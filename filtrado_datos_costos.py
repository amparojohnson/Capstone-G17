import pandas as pd

# Cargar los datos de items
items = pd.read_csv('data_items.csv')

# Filtrar los productos que tienen información en todas las columnas requeridas
productos_completos = items.dropna(subset=['unit_sale_price (CLP)', 'cost (CLP)', 'cost_per_purchase'])

# Guardar el resultado en un nuevo archivo CSV
productos_completos.to_csv('items_fitrado_costos_y_ventas.csv', index=False)

# Imprimir un resumen
print(f"Se han procesado {len(items)} productos en total.")
print(f"Se han guardado {len(productos_completos)} productos con información completa en 'productos_con_info_completa.csv'.")
print(f"Se omitieron {len(items) - len(productos_completos)} productos por falta de información.")

# Opcional: Mostrar los primeros registros del nuevo DataFrame
print("\nPrimeros registros del nuevo archivo:")
print(productos_completos.head().to_string())