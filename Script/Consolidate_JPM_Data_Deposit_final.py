import pandas as pd
import numpy as np
import datetime
import warnings

from maks_lib import input_path
from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

df = pd.read_excel(input_path+"JP Morgan Rate Sheet_new.xlsx")
df1 = df[7:13]
df1.drop(df1.columns[[0, 1, 2, 6, 7, 8]], axis=1, inplace=True)
df1["Bank_Product_Name"] = "Chase Premier Plus Checking SM"
df1 = df1[2:]
df1 = df1.rename(columns={'Unnamed: 3': 'Balance', 'Unnamed: 4': 'Product_Interest', 'Unnamed: 5': 'Product_Apy'})
df1['Product_Interest'] = (df1['Product_Interest'] * 100).astype(str) + '%'
df1['Product_Apy'] = (df1['Product_Apy'] * 100).astype(str) + '%'

df2 = df[13:16]
df2.drop(df2.columns[[0, 1, 2, 6, 7, 8]], axis=1, inplace=True)
df2 = df2.rename(columns={'Unnamed: 3': 'Balance', 'Unnamed: 4': 'Product_Interest', 'Unnamed: 5': 'Product_Apy'})
df2['Product_Interest'] = (df2['Product_Interest'] * 100).astype(str) + '%'
df2['Product_Apy'] = (df2['Product_Apy'] * 100).astype(str) + '%'
df2["Bank_Product_Name"] = "Chase Savings SM"
df2 = df2[2:]

df00 = df[42:43]
df00.drop(df00.columns[[0, 1, 2, 3, 4, 5, 6, 8]], axis=1, inplace=True)
df3 = df[47:48]
df3.drop(df3.columns[[1, 2, 3, 4, 5, 6]], axis=1, inplace=True)
df3 = df3.rename(columns={'Unnamed: 0': 'Product_Term', 'Unnamed: 7': 'Product_Interest', 'Unnamed: 8': 'Product_Apy'})
df3['Product_Interest'] = (df3['Product_Interest'] * 100).astype(str) + '%'
df3['Product_Apy'] = (df3['Product_Apy'] * 100).astype(str) + '%'
df3["Bank_Product_Name"] = "CERTIFICATES OF DEPOSIT (CD)"
df3["Balance"] = df00['Unnamed: 7'].values

df4 = df[49:50]
df4.drop(df4.columns[[1, 2, 3, 4, 5, 6]], axis=1, inplace=True)
df4 = df4.rename(columns={'Unnamed: 0': 'Product_Term', 'Unnamed: 7': 'Product_Interest', 'Unnamed: 8': 'Product_Apy'})
df4['Product_Interest'] = (df4['Product_Interest'] * 100).astype(str) + '%'
df4['Product_Apy'] = (df4['Product_Apy'] * 100).astype(str) + '%'
df4["Bank_Product_Name"] = "CERTIFICATES OF DEPOSIT (CD)"
df4["Balance"] = df00['Unnamed: 7'].values

df5 = df[53:54]
df5.drop(df5.columns[[1, 2, 3, 4, 5, 6]], axis=1, inplace=True)
df5 = df5.rename(columns={'Unnamed: 0': 'Product_Term', 'Unnamed: 7': 'Product_Interest', 'Unnamed: 8': 'Product_Apy'})
df5['Product_Interest'] = (df5['Product_Interest'] * 100).astype(str) + '%'
df5['Product_Apy'] = (df5['Product_Apy'] * 100).astype(str) + '%'
df5["Bank_Product_Name"] = "CERTIFICATES OF DEPOSIT (CD)"
df5["Balance"] = df00['Unnamed: 7'].values

frames = [df1, df2, df3, df4, df5]
result = pd.concat(frames)
df_final = pd.DataFrame(
    columns=["Date", "Bank_Name", 'Bank_Product', "Bank_Product_Type", 'Bank_Offer_Feature', 'Bank_Product_Name',
             'Product_Term', 'Balance', 'Product_Interest', 'Product_Apy', 'Mortgage_Down_Payment', 'Mortgage_Loan',
             'Min_Credit_Score_Mortagage', 'Mortgage_Apr'])
df_final['Bank_Product_Name'] = result['Bank_Product_Name'].values
df_final['Product_Term'] = result['Product_Term'].values
df_final['Balance'] = result['Balance'].values
df_final['Product_Interest'] = result['Product_Interest'].values
df_final['Product_Apy'] = result['Product_Apy'].values
df_final['Date'] = now.strftime("%m-%d-%Y")
df_final['Bank_Name'] = "JP MORGAN CHASE & Co."
df_final['Bank_Product'] = 'Deposits'
df_final['Bank_Offer_Feature'] = 'Offline'

for index in range(len(result.index)):
    df_final['Balance'].iloc[index] = df_final['Balance'].iloc[index].replace("$", "").replace("–", " - ")
    if "Checking" in result['Bank_Product_Name'].iloc[index]:
        df_final.ix[index, 'Bank_Product_Type'] = "Checking"
    elif "Savings" in result['Bank_Product_Name'].iloc[index]:
        df_final.ix[index, 'Bank_Product_Type'] = "Savings"
    elif "CERTIFICATES" in result['Bank_Product_Name'].iloc[index]:
        df_final.ix[index, 'Bank_Product_Type'] = "CD"

df_final.to_csv(output_path+"Consolidate_JPM_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
