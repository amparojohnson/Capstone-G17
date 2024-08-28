import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Cargar data_purchases.csv
purchases_file = os.path.join(current_dir, 'data_purchases.csv')
df_purchases = pd.read_csv(purchases_file, sep=';')

# Cargar data_items.csv
items_file = os.path.join(current_dir, 'data_items.csv')
df_items = pd.read_csv(items_file, sep=',')  # Cambiado a separador de coma

# Imprimir las columnas de ambos DataFrames
print("Columnas en df_purchases:")
print(df_purchases.columns)
print("\nColumnas en df_items:")
print(df_items.columns)

# Convertir columnas de fecha a datetime
df_purchases['date'] = pd.to_datetime(df_purchases['date'])
df_purchases['delivery_date'] = pd.to_datetime(df_purchases['delivery_date'])

# Calcular lead time
df_purchases['lead_time'] = (df_purchases['delivery_date'] - df_purchases['date']).dt.days

# Unir df_purchases con df_items
df_merged = pd.merge(df_purchases, df_items, on='item_id', how='left')

# Crear directorio para gráficos
graphs_dir = os.path.join(current_dir, 'graficos_lead_time')
os.makedirs(graphs_dir, exist_ok=True)

# Análisis por categoría de producto
if 'group_description' in df_merged.columns:
    plt.figure(figsize=(15, 8))
    sns.boxplot(x='group_description', y='lead_time', data=df_merged)
    plt.title('Lead Time por Categoría de Producto')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'lead_time_by_category.png'))
    plt.close()

    # Calcular lead time promedio por categoría
    lead_time_by_category = df_merged.groupby('group_description')['lead_time'].agg(['mean', 'median', 'std']).sort_values('mean', ascending=False)
    print("Lead time promedio por categoría:")
    print(lead_time_by_category)
else:
    print("No se encontró la columna 'group_description' en los datos unidos.")

# Análisis de lead time por ID de producto
plt.figure(figsize=(20, 10))
sns.boxplot(x='item_id', y='lead_time', data=df_merged)
plt.title('Lead Time por ID de Producto')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(graphs_dir, 'lead_time_by_product_id.png'))
plt.close()

# Impacto en la satisfacción del cliente
# Como no tenemos datos de satisfacción del cliente, podríamos usar la frecuencia de compra como proxy
df_customer_frequency = df_purchases.groupby('id')['date'].nunique().reset_index()
df_customer_frequency.columns = ['id', 'purchase_frequency']
df_merged_with_frequency = pd.merge(df_merged, df_customer_frequency, on='id', how='left')

# Eliminar valores infinitos o nulos
df_merged_with_frequency = df_merged_with_frequency.replace([np.inf, -np.inf], np.nan).dropna(subset=['lead_time', 'purchase_frequency'])

plt.figure(figsize=(10, 6))
sns.scatterplot(x='lead_time', y='purchase_frequency', data=df_merged_with_frequency)
plt.title('Impacto del Lead Time en la Frecuencia de Compra')
plt.xlabel('Lead Time (días)')
plt.ylabel('Frecuencia de Compra (número de días con compras)')
plt.tight_layout()
plt.savefig(os.path.join(graphs_dir, 'lead_time_vs_purchase_frequency.png'))
plt.close()

# Calcular correlación entre lead time y frecuencia de compra
correlation = df_merged_with_frequency['lead_time'].corr(df_merged_with_frequency['purchase_frequency'])
print(f"Correlación entre lead time y frecuencia de compra: {correlation:.2f}")

# Análisis de outliers
def identify_outliers(group):
    q1 = group['lead_time'].quantile(0.25)
    q3 = group['lead_time'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    return group[(group['lead_time'] < lower_bound) | (group['lead_time'] > upper_bound)]

outliers = df_merged.groupby('group_description', group_keys=False).apply(identify_outliers)
print("\nNúmero de outliers por categoría:")
print(outliers['group_description'].value_counts())

print("\nAlgunos ejemplos de outliers:")
print(outliers.head(10))

# Guardar outliers en un archivo CSV para análisis posterior
outliers.to_csv(os.path.join(graphs_dir, 'lead_time_outliers.csv'), index=False)
print("\nSe ha guardado un archivo CSV con todos los outliers en el directorio de gráficos.")

print("Análisis completado. Se han generado nuevos gráficos en el directorio 'graficos_lead_time'.")