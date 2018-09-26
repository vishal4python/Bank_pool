import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()
df0=pd.read_excel('C:\\Users\\Rupa\\.spyder-py3\\Book4.xlsx')
df=pd.DataFrame(columns=['Date','Bank_Name','Bank_Product','Bank_Product_Type','Bank_Offer_Feature', 'Bank_Product_Name', 'Product_Term', 'Balance','Product_Interest',
                         'Product_Apy','Mortgage_Down_Payment','Mortgage_Loan','Min_Credit_Score_Mortagage','Mortgage_Apr'])

df['Date']=now.strftime("%m-%d-%Y")
df['Bank_Name']="JP MORGAN CHASE & Co."
df['Bank_Product']='Deposits'
df['Bank_Offer_Feature']='Offline'
df['Bank_Product_Name']=df0['Product'].values
df['Product_Term']=df0['Terms(months)'].values
df['Balance']=df0['Balance'].values
df['Product_Interest']=(df0['Interest']*100).astype(str)+'%'
df['Product_Apy'] = (df0['APY']*100).astype(str)+'%'
for index, row in df0.iterrows():
    if "Checking" in row['Product']:
        df.iloc[index,3] = "Checking"
    elif "Savings" in row['Product']:
        df.iloc[index,3] = "Savings"
    elif "CERTIFICATES" in row['Product']:
        df.iloc[index,3] = "CDs"
df.to_csv( output_path+"Consolidate_JPM_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )
