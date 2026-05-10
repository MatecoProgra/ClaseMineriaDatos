#Solo en esta practica mostraré la limpieza de datos, en las demas ya no

import pandas as pd
from tabulate import tabulate

df = pd.read_csv("csv/registroCrimenes.csv")

print(tabulate(df, headers='keys', tablefmt='pretty'))

df_limpio = df.drop(columns=["DR_NO", "Date Rptd", "AREA","Rpt Dist No", 
                             "Part 1-2", "Status","Crm Cd", "Crm Cd 2", 
                             "Crm Cd 3", "Crm Cd 4","LOCATION","Cross Street",
                             "Mocodes", "Premis Cd", "Weapon Used Cd", "Crm Cd 1"])
df_limpio["Vict Sex"] = df_limpio["Vict Sex"].replace("H", "X").fillna("X")
df_limpio["Vict Descent"] = df_limpio["Vict Descent"].fillna("X")
df_limpio["Weapon Desc"] = df_limpio["Weapon Desc"].fillna("UNKNOWN WEAPON/OTHER WEAPON")
df_limpio = df_limpio.loc[df_limpio["Vict Age"]!=0]
df_limpio["Premis Desc"]= df_limpio["Premis Desc"].fillna("UKNOWN")
df_limpio = df_limpio.drop_duplicates()
df_limpio.rename(columns={"TIME OCC": "Time Occ", "DATE OCC": "Date Occ", "Crm Cd Desc": "Crime Desc"
                          ,"Status Desc":"Crm Status", "Weapon Desc":"Weapon"
                          }, inplace=True)

df_limpio['Date Occ'] = pd.to_datetime(df_limpio['Date Occ'], format='%m/%d/%Y %I:%M:%S %p')
# Convertir directamente a formato de tiempo
df_limpio['Time Occ'] = pd.to_datetime(df_limpio['Time Occ'].astype(str).str.zfill(4), format='%H%M').dt.time
df_limpio['Date Occ'] = df['Date Occ'].dt.date
df_limpio.to_csv('../csv/registroCrimenes.csv')
print(tabulate(df_limpio, headers='keys', tablefmt='pretty'))
df_limpio.to_csv("csv/registroCrimenes.csv")