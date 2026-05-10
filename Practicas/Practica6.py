import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("csv/registroCrimenes.csv", index_col=False)
os.makedirs("img/practica6", exist_ok=True)

columnas_numericas = [ 'Vict Age', 'LAT', 'LON']
columnas_categoricas = ["Date Occ", "Time Occ", 'Weapon', 'Area Name', 'Crime Desc', 'Vict Sex', 'Vict Descent', 'Premis Desc', 'Crm Status']

#Mostramos el histograma de cada numerica
for col in columnas_numericas:
    df[col].hist(figsize=(10, 6))
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.savefig(f"img/practica6/hist_{col}.png")
    plt.close()


for col in columnas_categoricas:
    counts = df[col].value_counts()
    counts.plot(kind="pie", figsize=(10, 10), autopct="%1.1f%%")
    plt.title(f"Pie chart of {col}")
    plt.savefig(f"img/practica6/pie_{col}.png")
    plt.close()

for i in range(len(columnas_numericas)):
    for j in range(i + 1, len(columnas_numericas)):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(df[columnas_numericas[i]], df[columnas_numericas[j]])
        ax.set_xlabel(columnas_numericas[i])
        ax.set_ylabel(columnas_numericas[j])
        plt.title(f"Scatter {columnas_numericas[i]} vs {columnas_numericas[j]}")
        plt.savefig(f"img/practica6/scatter_{columnas_numericas[i]}_vs_{columnas_numericas[j]}.png")
        plt.close()
        
for cat in columnas_categoricas:
    for col in columnas_numericas:
        df_grouped = df.groupby(cat)[col].mean().reset_index()
        fig, ax = plt.subplots(figsize=(18, 10))
        ax.plot(df_grouped[cat], df_grouped[col])
        plt.xticks(rotation=90)
        plt.title(f"Mean {col} by {cat}")
        plt.savefig(f"img/practica6/line_{col}-{cat}.png")
        plt.close()

hmap = sns.heatmap(df[columnas_numericas].corr(), annot=True)
plt.xticks(rotation=90)
plt.title(f"HeatMap of Crime")
plt.savefig(f"img/practica6/heatmap.png")
plt.close()