#Iniciamos practica 8import pandas as pd
import pandas as pd
from tabulate import tabulate
import os
import statsmodels.api as sm
import numbers
import matplotlib.pyplot as plt
from io import StringIO

ruta = "img/practica9"

def transform_variable(df: pd.DataFrame, x: str) -> pd.Series:
    if isinstance(df[x][0], numbers.Number):
        return df[x]
    else:
        return pd.Series([i for i in range(0, len(df[x]))])

def linear_regression(df: pd.DataFrame, x: str, y: str) -> None:
    fixed_x = transform_variable(df, x)
    model = sm.OLS(df[y], sm.add_constant(fixed_x)).fit()
    print(f"R2: {model.rsquared_adj}")

    coef = pd.read_html(StringIO(model.summary().tables[1].as_html()), header=0, index_col=0)[0]['coef']
    df.plot(x=x, y=y, kind='scatter')
    plt.plot(df[x], [coef.values[1] * x + coef.values[0] for _, x in fixed_x.items()], color='red')
    plt.xticks(rotation=90)
    plt.savefig(f'img/lr_{y}_{x}.png')
    plt.close()

df = pd.read_csv("csv/registroCrimenes.csv", index_col=False)
#regresamos tiempo a entero
df['Time Occ'] = df['Time Occ'].str.replace(':', '').astype(int)
os.makedirs(ruta, exist_ok=True)

columnas_numericas = [ 'Vict Age', 'LAT', 'LON']
columnas_categoricas = ["Date Occ", "Time Occ", 'Weapon', 'Area Name', 'Crime Desc', 'Vict Sex', 'Vict Descent', 'Premis Desc', 'Crm Status']

print(f'Graficas generadas en: {ruta}')
for cn in columnas_numericas:
    for col in df.columns:
        if col == cn:
            continue
        print(f'{col} y {cn}')
        df_agg = df.groupby([col])[[cn]].agg({cn: ['sum']})
        df_agg.reset_index(inplace=True)

        df_agg.columns = [col,f"{cn} suma"]
        df_agg.reset_index(inplace=True)
        #print(tabulate(df_agg, headers='keys', tablefmt='pretty'))
        linear_regression(df_agg, col, f"{cn} suma")