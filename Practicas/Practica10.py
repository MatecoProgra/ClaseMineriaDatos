#Inicia practica 10
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mode
import matplotlib

def get_cmap(n, name="hsv"):
    return matplotlib.colormaps.get_cmap(name)

def scatter_group_by(file_path, df, x_column, y_column, label_column):
    fig, ax = plt.subplots()
    labels = pd.unique(df[label_column])
    cmap = get_cmap(len(labels) + 1)
    for i, label in enumerate(labels):
        filter_df = df.query(f"{label_column} == '{label}'")
        ax.scatter(filter_df[x_column], filter_df[y_column], label=label, color=cmap(i))
    ax.legend()
    plt.savefig(file_path)
    plt.close()

def euclidean_distance(p_1: np.array, p_2: np.array) -> float:
    return np.sqrt(np.sum((p_2 - p_1) ** 2))

def k_nearest_neightbors(points, labels, input_data, k):
    label_indices = {label: index for index, label in enumerate(pd.unique(labels))}
    indices_labels = {index: label for label, index in label_indices.items()}
    input_distances = [
        [euclidean_distance(input_point, point) for point in points]
        for input_point in input_data
    ]
    points_k_nearest = [
        np.argsort(input_point_dist)[:k] for input_point_dist in input_distances
    ]
    return [
        indices_labels[mode([label_indices[labels[index]] for index in point_nearest]).mode]
        for point_nearest in points_k_nearest
    ]

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
scatter_group_by("img/groups.png", df, "LAT", "LON", "Area_Name")


list_t = [
    (np.array([row['LAT'], row['LON']]), row['Area_Name'])
    for _, row in df.iterrows()
]
input_data = [point for point, _ in list_t]
labels = np.array([label for _, label in list_t])

# Punto nuevo a clasificar
new_points = [np.array([35.05, -118.24])]
kn = k_nearest_neightbors(input_data, labels, new_points, 5)
print(kn)