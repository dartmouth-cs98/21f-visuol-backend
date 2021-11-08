import pandas as pd

def state_tax(state, income, married):
    df = pd.read_csv('state_taxes')
    df2 = df[df['State'] == state]
    remaining_income = 0
    if(len(df2) == 0):
        return income
    if(married):
        for i in reversed(range(len(df2))):
            if(income > df2.iloc[i]['Married Bracket'] / 2):
                        if(i == len(df2) - 1):
                            remaining_income += (income - df2.iloc[i]['Married Bracket'] / 2) * (1 - df2.iloc[i]['Married Rate'])
                        else:
                            remaining_income += ((min(income, df2.iloc[i + 1]['Married Bracket'] / 2) - df2.iloc[i]['Married Bracket'] / 2)  * (1 - df2.iloc[i]['Married Rate']))
    else:
        for i in reversed(range(len(df2))):
            if(income > df2.iloc[i]['Single Bracket']):
                        if(i == len(df2) - 1):
                            remaining_income += (income - df2.iloc[i]['Single Bracket']) * (1 - df2.iloc[i]['Single Rate'])
                        else:
                            remaining_income += ((min(income, df2.iloc[i + 1]['Single Bracket']) - df2.iloc[i]['Single Bracket'])  * (1 - df2.iloc[i]['Single Rate']))
    return remaining_income

print(state_tax('Washington D.C.', 100000, False))