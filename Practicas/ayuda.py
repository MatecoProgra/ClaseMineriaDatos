import pandas as pd
from tabulate import tabulate

def imp_tab(df:pd.DataFrame)-> pd.DataFrame:
    print(tabulate(df, headers= df.columns, tablefmt='orgtbl'))