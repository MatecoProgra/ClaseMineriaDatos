import pandas as pd
import ayuda
import matplotlib.pyplot as plt
import os

os.makedirs("img", exist_ok=True)
df = pd.read_csv("csv/registroCrimenes.csv", index_col=False)
#Obtenemos los datos estadisticos
ayuda.imp_tab(df)

#Agrupamos por area y sexo de la victima
df_by_sexArea = df.groupby(["Area Name", "Vict Sex"]).agg({"Vict Age": ['sum','count', 'mean', "min", 'max']})
df_by_sexArea = df_by_sexArea.reset_index()
ayuda.imp_tab(df_by_sexArea)

#Agrupamos por 
df_by_sexArea = df.groupby(["Vict Descent", "Vict Sex"]).agg({"Vict Age": ['sum','count', 'mean', "min", 'max']})
df_by_sexArea = df_by_sexArea.reset_index()
ayuda.imp_tab(df_by_sexArea)

#Graficamos por area y cada columna
df.boxplot(by= "Area Name", column=["Time Occ"])
plt.xticks(rotation=90)
plt.savefig("img/byAN-Time")
plt.close()

df.boxplot(by= "Area Name", column=["Vict Age"])
plt.xticks(rotation=90)
plt.savefig("img/byAN-VA")
plt.close()

df.boxplot(by= "Area Name", column=["LAT"])
plt.xticks(rotation=90)
plt.savefig("img/byAN-Lat")
plt.close()

df.boxplot(by= "Area Name", column=["LON"])
plt.xticks(rotation=90)
plt.savefig("img/byAN-Lon")
plt.close()

#Graficamos por sexo y cada columna
df.boxplot(by= "Vict Sex", column=["Time Occ"])
plt.xticks(rotation=90)
plt.savefig("img/byVS-Time")
plt.close()

df.boxplot(by= "Vict Sex", column=["Vict Age"])
plt.xticks(rotation=90)
plt.savefig("img/byVS-VA")
plt.close()

df.boxplot(by= "Vict Sex", column=["LAT"])
plt.xticks(rotation=90)
plt.savefig("img/byVS-Lat")
plt.close()

df.boxplot(by= "Vict Sex", column=["LON"])
plt.xticks(rotation=90)
plt.savefig("img/byVS-Lon")
plt.close()

#Graficamos por Descendencia y cada columna
df.boxplot(by= "Vict Descent", column=["Time Occ"])
plt.xticks(rotation=90)
plt.savefig("img/byVD-Time")
plt.close()

df.boxplot(by= "Vict Descent", column=["Vict Age"])
plt.xticks(rotation=90)
plt.savefig("img/byVD-VA")
plt.close()

df.boxplot(by= "Vict Descent", column=["LAT"])
plt.xticks(rotation=90)
plt.savefig("img/byVD-Lat")
plt.close()

df.boxplot(by= "Vict Descent", column=["LON"])
plt.xticks(rotation=90)
plt.savefig("img/byVD-Lon")
plt.close()