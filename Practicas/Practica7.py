import pandas as pd

from statsmodels.formula.api import ols
import statsmodels.api as sm
df = pd.read_csv("../csv/registroCrimenes.csv", index_col=False)

columnas_numericas = [ 'Vict_Age', 'LAT', 'LON']
columnas_categoricas = ["Date_Occ", "Time_Occ", 'Weapon', 'Area_Name', 'Crime_Desc', 'Vict_Sex', 'Vict_Descent', 'Premis_Desc', 'Crm_Status']
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

#Calculamos la anova de todas las columnas
for cn in columnas_numericas:
    for cc in columnas_categoricas:
        modl = ols(f"{cn} ~ {cc}", data=df).fit()
        anova_df = sm.stats.anova_lm(modl, typ=2)
        print(f"Entre {cc} y {cn}")
        if anova_df["PR(>F)"][cc]< 0.005:
            print("Hay diferencias")
            print(anova_df)
        else:
            print("No hay diferencias")


#Ahora obtenemos el ttest entre Area y vict sex
from statsmodels.stats.weightstats import ttest_ind
top_Areas= df.groupby('Area_Name')["Vict_Age"].mean().sort_values(ascending=False).head(2).index;
grupo_1=df[df['Area_Name']== top_Areas[0]]['Vict_Age']
grupo_2=df[df['Area_Name']== top_Areas[1]]['Vict_Age']
t_stat, p_value, df_freedom = ttest_ind(grupo_1, grupo_2)

if p_value < 0.005:
    print(f"Hay diferencias entre los grupos {top_Areas[0]} y {top_Areas[1]}")
else:
    print(f"NO Hay diferencias entre los grupos {top_Areas[0]} y {top_Areas[1]}")