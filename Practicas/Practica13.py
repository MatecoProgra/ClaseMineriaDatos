import matplotlib.pyplot as plt
import statsmodels.api as sm
import numbers
import pandas as pd
from tabulate import tabulate
from io import StringIO
import numpy as np
import os

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt="orgtbl"))

def transform_variable(df: pd.DataFrame, x: str) -> pd.Series:
    if isinstance(df[x].iloc[0], numbers.Number):
        return df[x]
    else:
        return pd.Series([i for i in range(0, len(df[x]))])

def linear_regression(df: pd.DataFrame, x: str, y: str) -> dict:
    fixed_x = transform_variable(df, x)
    model = sm.OLS(list(df[y]), sm.add_constant(fixed_x)).fit()
    bands = pd.read_html(StringIO(model.summary().tables[1].as_html()), header=0, index_col=0)[0]
    coef = pd.read_html(StringIO(model.summary().tables[1].as_html()), header=0, index_col=0)[0]['coef']
    r_2_t = pd.read_html(StringIO(model.summary().tables[0].as_html()), header=None, index_col=None)[0]
    return {
        'm': coef.values[1],
        'b': coef.values[0],
        'r2': r_2_t.values[0][3],
        'r2_adj': r_2_t.values[1][3],
        'low_band': bands['[0.025'].iloc[0], 
        'hi_band': bands['0.975]'].iloc[0]
    }

def plt_lr(df, x, y, m, b, r2, r2_adj, low_band, hi_band, colors):
    fixed_x = transform_variable(df, x)
    plt.plot(df[x], [m * x + b for _, x in fixed_x.items()], color=colors[0])
    plt.fill_between(df[x],
                     [m * x + low_band for _, x in fixed_x.items()],
                     [m * x + hi_band for _, x in fixed_x.items()],
                     alpha=0.2, color=colors[1])
    
    os.makedirs("img", exist_ok=True)

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

ruta = 'img/Practica13'
os.makedirs(ruta, exist_ok=True)

df['Date_Occ'] = pd.to_datetime(df['Date_Occ'])
df_by_date = df.groupby('Date_Occ').agg(
    total_crimenes=pd.NamedAgg(column='Vict_Age', aggfunc='count')
)
df_by_date.reset_index(inplace=True)

print_tabulate(df_by_date.head(10))


x = "Date_Occ"
y = "total_crimenes"
df_by_date.plot(x=x, y=y, kind='scatter')
plt.xticks(rotation=90)
plt.savefig(f'{ruta}/full_crimenes_fecha.png')
plt.close()


df_50 = df_by_date.tail(50).reset_index(drop=True)
df_50.plot(x=x, y=y, kind='scatter')
a = linear_regression(df_50, x, y)
plt_lr(df=df_50, x=x, y=y, colors=('red', 'orange'), **a)
plt.xticks(rotation=90)
plt.savefig(f'{ruta}/lr_crimenes_50d.png')
plt.close()

# Aplicar reset_index en todos los dfs
dfs = [
    ('50D',   df_by_date.tail(50).reset_index(drop=True)),
    ('10D',   df_by_date.tail(10).reset_index(drop=True)),
    ('5D',    df_by_date.tail(5).reset_index(drop=True)),
    ('lunes', df_by_date[pd.to_datetime(df_by_date[x]).dt.dayofweek == 0].reset_index(drop=True)),
]
lrs = [(title, linear_regression(_df, x=x, y=y), len(_df)) for title, _df in dfs]
lrs_p = [(title, lr['m'] * size + lr['b'], lr) for title, lr, size in lrs]
print(lrs_p)