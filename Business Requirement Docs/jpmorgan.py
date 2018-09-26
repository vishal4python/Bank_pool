# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

df=pd.read_excel("JP Morgan Rate Sheet.xlsx")
df1=df[8:14]
df1.drop(df1.columns[[6]], axis=1, inplace=True)
df2=df1[df1.columns[3:6]]
df1.drop(df1.columns[[3,4,5]], axis=1, inplace=True)
df1=df1[:-1]
df2=df2[1:]
df2["Product"]="Chase Premier Plus Checking SM"
df2["Terms(months)"]=np.NAN
df2= df2.rename(columns={'Unnamed: 3': 'Consumer Deposit Rates','Unnamed: 4': 'Interest', 'Unnamed: 5': 'APY'})
df2=df2[1:]
df1["Product"]="Chase Premier Platinum Checking SM"
df1["Terms(months)"]=np.NAN
df1=df1[1:]
df1= df1.rename(columns={'Unnamed: 1': 'Interest', 'Unnamed: 2': 'APY'})
df1=df1[1:]
df3=df[16:17]
df3.drop(df3.columns[[4,5,6]], axis=1, inplace=True)
df3["Product"]="Chase Savings SM"
df3["Terms(months)"]=np.NAN
df3.drop(df3.columns[[0]], axis=1, inplace=True)
df3= df3.rename(columns={'Unnamed: 1': 'Consumer Deposit Rates','Unnamed: 2': 'Interest', 'Unnamed: 3': 'APY'})
df4=df[19:30]
df4.drop(df4.columns[[1,2,5,6]], axis=1, inplace=True)
df4["Product"]="Chase Premier Savings"
df4["Terms(months)"]=np.NAN
df4= df4.rename(columns={'Unnamed: 3': 'Interest', 'Unnamed: 4': 'APY'})
df4=df4[1:]
df5=df[38:42]
df5.drop(df5.columns[[1,2,3,4,5]], axis=1, inplace=True)
df5["Product"]="CERTIFICATES OF DEPOSIT (CD) "
df5["Terms(months)"]=df5["Consumer Deposit Rates"]
df5["Consumer Deposit Rates"]=np.NAN
df6=pd.DataFrame(df5["Unnamed: 6"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df5["Interest"] = df6["Interest"].values
df5["APY"]= df6["APY"].values
df5.drop(df5.columns[[1]], axis=1, inplace=True)
df5=df5.reindex(columns=["Consumer Deposit Rates","Interest","APY","Product","Terms(months)"])
df5=df5[1:]
df7=df[44:59]
df7.drop(df7.columns[[1,2,3,4,5]], axis=1, inplace=True)
df7["Product"]="CERTIFICATES OF DEPOSIT (CD) "
df7["Terms(months)"]=df7["Consumer Deposit Rates"]
df7["Consumer Deposit Rates"]=np.NAN
df6=pd.DataFrame(df7["Unnamed: 6"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df7["Interest"] = df6["Interest"].values
df7["APY"]= df6["APY"].values
df7.drop(df7.columns[[1]], axis=1, inplace=True)
df7=df7.reindex(columns=["Consumer Deposit Rates","Interest","APY","Product","Terms(months)"])
df7=df7[1:]
frames = [df1,df2,df3,df4,df5,df7]
result = pd.concat(frames)
result["Bank Name"]="JP MORGAN"
result.to_csv('Final JP MORGAN.csv')
