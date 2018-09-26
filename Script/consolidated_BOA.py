import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import input_path
from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

df0=pd.read_excel(input_path+"DigitalDeposit_MD.xlsx",sheet_name="page-1")
df1=pd.read_excel(input_path+"DigitalDeposit_MD.xlsx",sheet_name="page-2")
df2=pd.read_excel(input_path+"DigitalDeposit_MD.xlsx",sheet_name="page-3")


df01=df0[4:9]
df01["Bank_Product_Name"]="Rewards Savings"
df01=df01[3:5]
df01.drop(df01.columns[[3]], axis=1, inplace=True)
df01= df01.rename(columns={'Deposit Interest Rates & Annual Percentage Yields (APYs)': 'Balance','Unnamed: 1': 'Product_Interest','Unnamed: 2': 'Product_Apy'})
df01['Product_Interest'] = (df01['Product_Interest']).astype(str)+'%'
df01['Product_Apy'] = (df01['Product_Apy']).astype(str)+'%'
df01["Bank_Product_Name"]="Rewards Savings/Minor Savings"
df01["Bank_Offer_Feature"]="Offline"
df01["Bank_Product_Type"]="Savings"
df01["Bank_Product"]="Deposits"
df01["Bank_Name"]="BANK OF AMERICA CORP"

df11=df1[16:21]
df11["Bank_Product_Name"]="Bank of America Interest Checking"
df11=df11[2:]
df11= df11.rename(columns={'The Interest Rate Booster ("Booster") is included in the "Rate %" and "APY %" shown above for the Preferred Rewards': 'Balance','Unnamed: 1': 'Product_Interest', 'Unnamed: 2': 'Product_Apy'})
df11['Product_Interest'] = (df11['Product_Interest']).astype(str)+'%'
df11['Product_Apy'] = (df11['Product_Apy']).astype(str)+'%'
df11["Bank_Offer_Feature"]="Offline"
df11["Bank_Product_Type"]="Checking"
df11["Bank_Product"]="Deposits"
df11["Bank_Name"]="BANK OF AMERICA CORP"


df21=df2[0:12]
df22 = df21.iloc[:,0:4]
df22.drop(df22.columns[[1]], axis=1, inplace=True)
df22["Bank_Product_Name"]="Fixed Term CD/IRA Products"
df22=df22[1:]
df22["Balance"]="Less than $10,000"
df22=df22[3:]
df22= df22.rename(columns={'Fixed Term CD/IRA Products':'Product_Term','Unnamed: 3': 'Product_Apy','Unnamed: 2': 'Product_Interest'})
df22=df22.reindex(columns=["Balance","Product_Interest","Product_Apy","Bank_Product_Name","Product_Term"])

df23=df2[0:12]
df23.drop(df23.columns[[1,2,3,4,6,7]], axis=1, inplace=True)
df23["Bank_Product_Name"]="Fixed Term CD/IRA Products"
df23=df23[1:]
df23["Balance"]="$10,000 - $99,999"
df23=df23[3:]
df3=pd.DataFrame(df23["Unnamed: 5"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df23["Product_Interest"] = df3["Interest"].values
df23["Product_Apy"]= df3["APY"].values
df23.drop(df23.columns[[1]], axis=1, inplace=True)
df23= df23.rename(columns={'Fixed Term CD/IRA Products':'Product_Term'})
df23=df23.reindex(columns=["Balance","Product_Interest","Product_Apy","Bank_Product_Name","Product_Term"])

df24=df2[0:12]
df24.drop(df24.columns[[1,2,3,5,4,6]], axis=1, inplace=True)
df24["Bank_Product_Name"]="Fixed Term CD/IRA Products"
df24=df24[1:]
df24["Balance"]="$100,000 and over"
df24=df24[3:]
df3=pd.DataFrame(df24["Unnamed: 7"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df24["Product_Interest"] = df3["Interest"].values
df24["Product_Apy"]= df3["APY"].values
df24.drop(df24.columns[[1]], axis=1, inplace=True)
df24= df24.rename(columns={'Fixed Term CD/IRA Products':'Product_Term'})
df24=df24.reindex(columns=["Balance","Product_Interest","Product_Apy","Bank_Product_Name","Product_Term"])
frames_page3 = [df22,df23,df24]
result_page3 = pd.concat(frames_page3)
result_page3['Product_Interest'] = (result_page3['Product_Interest']).astype(str)+'%'
result_page3['Product_Apy'] = (result_page3['Product_Apy']).astype(str)+'%'
result_page3["Bank_Offer_Feature"]="Offline"
result_page3["Bank_Product_Type"]="CD"
result_page3["Bank_Product"]="Deposits"
result_page3["Bank_Name"]="BANK OF AMERICA CORP"
result_page3["Bank_Product_Name"]=result_page3["Product_Term"].values
df3=pd.DataFrame(result_page3["Product_Term"].str.split('-').tolist(),columns=["In","A"])
result_page3["Product_Term"]=df3["In"].values
result_page3=result_page3.iloc[[0,1,4],:]

frames=[df01,df11,result_page3]
result=pd.concat(frames)
df_final = pd.DataFrame(columns=["Date", "Bank_Name", 'Bank_Product', "Bank_Product_Type", 'Bank_Offer_Feature', 'Bank_Product_Name',
             'Product_Term', 'Balance', 'Product_Interest',
             'Product_Apy', 'Mortgage_Down_Payment', 'Mortgage_Loan', 'Min_Credit_Score_Mortagage', 'Mortgage_Apr'])


df_final['Bank_Product_Name'] = result['Bank_Product_Name'].values
df_final['Product_Term'] = result['Product_Term'].values
df_final['Balance'] = result['Balance'].values
df_final['Product_Interest'] = result['Product_Interest'].values
df_final['Product_Apy'] = result['Product_Apy'].values
df_final['Bank_Name'] =result['Bank_Name'].values
df_final['Bank_Product'] = result['Bank_Product'].values
df_final['Bank_Offer_Feature'] = result['Bank_Offer_Feature'].values
df_final['Bank_Product_Type'] = result['Bank_Product_Type'].values
df_final['Date'] = now.strftime("%m-%d-%Y")
df_final.to_csv(output_path+"Consolidate_BOA_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )
    
