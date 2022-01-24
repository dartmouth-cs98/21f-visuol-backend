import pandas as pd

from mongo.mongo_client import client
db = client.VisuOL
col = db['state_tax_brackets']

def state_tax(state, income, married):
    cols = col.find({"State": state})
    df2= pd.DataFrame(list(cols))
    remaining_income = 0
    if(len(df2) == 0):
        return 0
    if(married=='married'):
        if(df2.iloc[0]['Married Bracket'] != 0):
            remaining_income = min(income, df2.iloc[0]['Married Bracket'])
        for i in range(len(df2)):
            if(income > df2.iloc[i]['Married Bracket'] / 2):
                        if(i == len(df2) - 1):
                            remaining_income += (income - df2.iloc[i]['Married Bracket'] / 2) * (df2.iloc[i]['Married Rate'])
                        else:
                            remaining_income += ((min(income, df2.iloc[i + 1]['Married Bracket'] / 2) - df2.iloc[i]['Married Bracket'] / 2)  * (df2.iloc[i]['Married Rate']))
    else:
        if(df2.iloc[0]['Married Bracket'] != 0):
            remaining_income = min(income, df2.iloc[0]['Single Bracket'])
        for i in range(len(df2)):
            if(income > df2.iloc[i]['Single Bracket']):
                        if(i == len(df2) - 1):
                            remaining_income += (income - df2.iloc[i]['Single Bracket']) * (df2.iloc[i]['Single Rate'])
                        else:
                            remaining_income += ((min(income, df2.iloc[i + 1]['Single Bracket']) - df2.iloc[i]['Single Bracket'])  * (df2.iloc[i]['Single Rate']))
    return 1 - remaining_income/income