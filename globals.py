import pandas as pd
import os

if ("df_despesa.csv" in os.listdir()) and ("df_receita.csv" in os.listdir()):
    df_despesa = pd.read_csv("df_despesa.csv", index_col=0, parse_dates=True)
    df_receita = pd.read_csv("df_receita.csv", index_col=0, parse_dates=True)
    df_despesa["Data"] = pd.to_datetime(df_despesa["Data"])
    df_receita["Data"] = pd.to_datetime(df_receita["Data"])
    df_despesa["Data"] = df_despesa["Data"].apply(lambda x: x.date())
    df_receita["Data"] = df_receita["Data"].apply(lambda x: x.date())
else:
    data_structure = {'Valor':[],
        'Efetuado':[],
        'Fixo':[],
        'Data':[],
        'Categoria':[],
        'Descrição':[],}
    df_receita = pd.DataFrame(data_structure)
    df_despesa = pd.DataFrame(data_structure)
    df_despesa.to_csv("df_despesa.csv")
    df_receita.to_csv("df_receita.csv")

if ("df_cat_despesa.csv" in os.listdir()) and ("df_cat_receita.csv" in os.listdir()):
    df_cat_despesa = pd.read_csv("df_cat_despesa.csv", index_col=0)
    df_cat_receita = pd.read_csv("df_cat_receita.csv", index_col=0)
    cat_despesa = df_cat_despesa.values.tolist()
    cat_receita = df_cat_receita.values.tolist()

else:
    cat_receita = {'Categoria': ["Salário", "Investimentos","Comissão"]}
    cat_despesa = {'Categoria': ["Alimentação", "Aluguel","Gasolina", "Saúde", "lazer"]}

    df_cat_receita = pd.DataFrame(cat_receita)
    df_cat_despesa = pd.DataFrame(cat_despesa)
    df_cat_receita.to_csv("df_cat_receita.csv")
    df_cat_despesa.to_csv("df_cat_despesa.csv")