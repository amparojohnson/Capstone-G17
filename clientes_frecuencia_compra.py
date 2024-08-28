import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Cargar los datos desde el archivo CSV
df = pd.read_csv('data_sales.csv', sep=';')

# Contar el número de compras por cliente
purchase_frequency = df['client_id'].value_counts().reset_index()
purchase_frequency.columns = ['Cliente ID', 'Número de Compras']

# Preparar los datos para la clusterización
X = purchase_frequency[['Número de Compras']].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determinar el número óptimo de clusters usando el método del codo
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Graficar el método del codo
plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), wcss)
plt.title('Método del Codo')
plt.xlabel('Número de clusters')
plt.ylabel('WCSS')
plt.savefig('metodo_del_codo.png')
plt.close()

# Basándonos en el gráfico del método del codo, elegimos un número de clusters (por ejemplo, 3)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
cluster_labels = kmeans.fit_predict(X_scaled)

# Añadir las etiquetas de cluster al DataFrame
purchase_frequency['Cluster'] = cluster_labels

# Crear el histograma
plt.figure(figsize=(12, 6))
for i in range(n_clusters):
    cluster_data = purchase_frequency[purchase_frequency['Cluster'] == i]
    plt.hist(cluster_data['Número de Compras'], bins=30, alpha=0.5, label=f'Cluster {i}')

plt.title('Histograma de Frecuencia de Compras por Cluster')
plt.xlabel('Número de Compras')
plt.ylabel('Frecuencia')
plt.legend()
plt.savefig('histograma_clusters.png')
plt.close()

# Crear el gráfico de dispersión
plt.figure(figsize=(12, 6))
colors = ['r', 'g', 'b']  # Colores para cada cluster
for i in range(n_clusters):
    cluster_data = purchase_frequency[purchase_frequency['Cluster'] == i]
    plt.scatter(cluster_data.index, cluster_data['Número de Compras'], 
                c=colors[i], label=f'Cluster {i}', alpha=0.6)

plt.title('Gráfico de Dispersión de Clusters')
plt.xlabel('Índice de Cliente')
plt.ylabel('Número de Compras')
plt.legend()
plt.savefig('dispersion_clusters.png')
plt.close()

# Mostrar estadísticas por cluster
print("Estadísticas por cluster:")
for i in range(n_clusters):
    cluster_data = purchase_frequency[purchase_frequency['Cluster'] == i]
    print(f"\nCluster {i}:")
    print(f"Número de clientes: {len(cluster_data)}")
    print(f"Promedio de compras: {cluster_data['Número de Compras'].mean():.2f}")
    print(f"Mínimo de compras: {cluster_data['Número de Compras'].min()}")
    print(f"Máximo de compras: {cluster_data['Número de Compras'].max()}")

# Guardar los resultados en un archivo CSV
purchase_frequency.to_csv('frecuencia_compras_por_cliente_con_clusters.csv', index=False)
print("\nLos resultados se han guardado en 'frecuencia_compras_por_cliente_con_clusters.csv'")
print("Se han generado tres gráficos: 'metodo_del_codo.png', 'histograma_clusters.png' y 'dispersion_clusters.png'")