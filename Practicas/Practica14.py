#Practica 14
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import os

ruta = 'img/Practica14'
os.makedirs(ruta, exist_ok=True)

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

def generate_word_cloud(df, columna, filename):
    all_words = ""
    palabras = df[columna].dropna().astype(str).tolist()
    for arg in palabras:
        tokens = arg.split()
        all_words += " ".join(tokens) + " "

    print(f"\nTop 10 palabras en '{columna}':")
    print(Counter(all_words.split()).most_common(10))

    wordcloud = WordCloud(
        background_color="white", min_font_size=5
    ).generate(all_words)

    plt.close()
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f"{ruta}/{filename}.png")
    plt.close()

columnas_texto = ["Crime_Desc", "Premis_Desc", "Weapon"]
for col in columnas_texto:
    generate_word_cloud(df, col, f"wordcloud_{col.replace(' ', '_')}")