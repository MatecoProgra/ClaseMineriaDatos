import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

df = pd.read_csv("csv/registroCrimenes.csv", index_col=False)
df = df.rename(columns={
    "Date Occ": "Date_Occ",
    "Vict Age": "Vict_Age",
    "Time Occ": "Time_Occ",
    "Vict Sex": "Vict_Sex",
    "Crime Desc": "Crime_Desc",
    'Vict Descent': 'Vict_Descent',
    'Area Name': 'Area_Name',
    'Premis Desc':'Premis_Desc',
    'Crm Status': 'Crm_Status'})

ruta = 'img/Practica12'

os.makedirs(ruta, exist_ok=True)

df_sample = df.sample(n=500, random_state=42)

def get_cmap(n, name="hsv"):
    return plt.colormaps.get_cmap(name)

def euclidean_distance(p_1, p_2):
    return np.sqrt(np.sum((p_2 - p_1) ** 2))

def scatter_group_by(file_path, df, x_column, y_column, label_column):
    fig, ax = plt.subplots()
    labels = pd.unique(df[label_column])
    cmap = get_cmap(len(labels) + 1)
    for i, label in enumerate(labels):
        filter_df = df.query(f"{label_column} == '{label}'")
        ax.scatter(filter_df[x_column], filter_df[y_column], label=label)
    ax.legend()
    plt.set_cmap(cmap)
    plt.savefig(file_path)
    plt.close()

def calculate_means(points, labels, clusters):
    mean = []
    for k in range(clusters):
        m = np.mean(points[labels == k], axis=0)
        mean.append(m)
    return mean

def calculate_nearest_k(point, actual_means):
    distance = [euclidean_distance(mean, point) for mean in actual_means]
    return (point, np.argmin(distance))

def k_means(points, k):
    N = len(points)
    x = np.array(points)
    y = np.random.randint(0, k, N)
    dimensions = len(points[0])
    mean = np.zeros((k, dimensions)) 

    for t in range(15):
        actual_mean = calculate_means(points=x, labels=y, clusters=k)
        y = np.array([calculate_nearest_k(point=point, actual_means=actual_mean)[1] for point in x])

        df_points = pd.DataFrame(x, columns=['x', 'y'])
        df_points['label'] = np.char.mod('%d', y)
        df_mean = pd.DataFrame(actual_mean, columns=['x', 'y'])
        df_mean['label'] = ['centroid' for _ in range(len(actual_mean))]
        df_plot = pd.concat([df_points, df_mean])
        scatter_group_by(f"{ruta}/kmeans_{t}.png", df_plot, "x", "y", "label")

        if np.array_equal(np.array(actual_mean), mean):
            break
        mean = np.array(actual_mean).copy()
    return mean

list_t = [
    (np.array([row['LAT'], row['LON']]), row['Area_Name'])
    for _, row in df_sample.iterrows()
]
points = [point for point, _ in list_t]

kn = k_means(points, 5)
print(f"Centroides finales: {kn}")