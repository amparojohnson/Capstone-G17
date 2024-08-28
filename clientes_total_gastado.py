import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Constantes
LOOPS = 20
MAX_ITERATIONS = 300
INITIALIZE_CLUSTERS = 'k-means++'
CONVERGENCE_TOLERANCE = 0.0001

def load_and_prepare_data(file_path):
    """
    Carga los datos desde un archivo CSV y prepara los datos para el clustering
    """
    df = pd.read_csv(file_path, sep=';')
    total_spent = df.groupby('client_id')['total (CLP)'].sum().reset_index()
    total_spent.columns = ['Cliente ID', 'Total Gastado (CLP)']
    
    # Normalizar los datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(total_spent[['Total Gastado (CLP)']])
    
    return X_scaled, total_spent

def plot_results(inertias):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(inertias) + 1), inertias, 'bo-', markersize=8, lw=2)
    plt.grid(True)
    plt.xlabel('Número de Clusters')
    plt.ylabel('Inercia')
    plt.title('Método del Codo para Determinar el Número Óptimo de Clusters')
    plt.savefig('metodo_del_codo.png')
    plt.close()

def select_clusters(data, loops, max_iterations, init_cluster, tolerance):
    inertias = []

    for i in range(1, loops + 1):
        kmeans = KMeans(n_clusters=i, max_iter=max_iterations,
                        init=init_cluster, tol=tolerance)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    plot_results(inertias)
    return inertias

def apply_optimal_clustering(data, n_clusters, total_spent):
    kmeans = KMeans(n_clusters=n_clusters, init=INITIALIZE_CLUSTERS)
    cluster_labels = kmeans.fit_predict(data)
    
    total_spent['Cluster'] = cluster_labels
    
    # Visualizar los resultados
    plt.figure(figsize=(12, 6))
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # Añade más colores si necesitas más clusters
    for i in range(n_clusters):
        cluster_data = total_spent[total_spent['Cluster'] == i]
        plt.scatter(cluster_data.index, cluster_data['Total Gastado (CLP)'], 
                    c=colors[i % len(colors)], label=f'Cluster {i}', alpha=0.6)

    plt.title('Gráfico de Dispersión de Clusters por Total Gastado')
    plt.xlabel('Índice de Cliente')
    plt.ylabel('Total Gastado (CLP)')
    plt.legend()
    plt.savefig('dispersion_clusters_total_gastado.png')
    plt.close()

    return total_spent

if __name__ == '__main__':
    # Cargar y preparar los datos
    X_scaled, total_spent = load_and_prepare_data('data_sales.csv')

    # Aplicar el método del codo
    inertias = select_clusters(X_scaled, LOOPS, MAX_ITERATIONS, INITIALIZE_CLUSTERS,
                               CONVERGENCE_TOLERANCE)

    # Determinar el número óptimo de clusters (esto requiere interpretación manual)
    # Por ejemplo, podrías elegir 3 clusters después de ver el gráfico
    optimal_clusters = 3  # Ajusta este número según lo que observes en el gráfico del método del codo

    # Aplicar el clustering con el número óptimo de clusters
    clustered_data = apply_optimal_clustering(X_scaled, optimal_clusters, total_spent)

    # Guardar los resultados
    clustered_data.to_csv('total_gastado_por_cliente_con_clusters.csv', index=False)
    print("Los resultados se han guardado en 'total_gastado_por_cliente_con_clusters.csv'")
    print("Se han generado dos gráficos: 'metodo_del_codo.png' y 'dispersion_clusters_total_gastado.png'")

    # Mostrar estadísticas por cluster
    print("\nEstadísticas por cluster:")
    for i in range(optimal_clusters):
        cluster_data = clustered_data[clustered_data['Cluster'] == i]
        print(f"\nCluster {i}:")
        print(f"Número de clientes: {len(cluster_data)}")
        print(f"Promedio de gasto: {cluster_data['Total Gastado (CLP)'].mean():.2f}")
        print(f"Mínimo de gasto: {cluster_data['Total Gastado (CLP)'].min():.2f}")
        print(f"Máximo de gasto: {cluster_data['Total Gastado (CLP)'].max():.2f}")