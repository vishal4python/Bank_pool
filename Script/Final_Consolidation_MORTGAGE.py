
# coding: utf-8

# In[1]:


import glob
import os
import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import output_path
from maks_lib import input_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

extension = 'csv'


# In[2]:


all_files = glob.glob(output_path+'*.{}'.format(extension))
all_mortage_files  = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and "Mortgage" in file.split("\\")[-1]]
all_deposite_files = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and file not in all_mortage_files]


# In[3]:


COLUMN_NAMES = list(pd.read_csv(all_mortage_files[0]).columns)
df_mortgage = pd.DataFrame(columns=COLUMN_NAMES) 
df_deposit = pd.DataFrame(columns=COLUMN_NAMES)


# In[4]:


df_mortgage


# In[5]:


for idx, file in enumerate(all_mortage_files):
    print(file)
    print(pd.read_csv(all_mortage_files[idx]).shape[1])


# In[6]:


for file in all_mortage_files:
    df_temp =pd.read_csv(file)
    df_temp.columns = ['Date', 'Bank_Name', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Offer_Feature', 'Bank_Product_Name', 'Product_Term', 'Balance',
       'Product_Interest', 'Product_Apy', 'Mortgage_Down_Payment',
       'Mortgage_Loan', 'Min_Credit_Score_Mortagage', 'Mortgage_Apr']
    df_mortgage = pd.concat([df_mortgage, df_temp])


# In[7]:


df_mortgage.shape


# In[8]:


df_mortgage


# In[9]:


df_mortgage.dropna(axis=0, how='all', inplace=True)


# In[10]:


df_mortgage.drop(columns=["Product_Apy"], inplace=True)


# In[11]:


df_mortgage.rename(columns={"Balance": "Min_Loan_Amount", "Product_Term": "Term_in_Year","Product_Interest": "Interest","Mortgage_Loan": "Mortgage_Loan_Amt","Min_Credit_Score_Mortagage":"Credit_Score", "Mortgage_Apr":"APR"}, inplace = True,index=str)


# In[12]:


df_mortgage['Date'] = " {}".format(now.strftime("%Y-%m-%d"))
df_mortgage['Bank_Native_Country'] = "US"
df_mortgage['State'] = "New York"
df_mortgage['Bank_Local_Currency'] = "USD"
df_mortgage['Bank_Type'] = "Bank"
df_mortgage['Bank_Product'] = "Mortgages"
df_mortgage['Bank_Product_Type'] = "Mortgages"
df_mortgage['Bank_Product_Code'] = np.NAN
df_mortgage['Min_Loan_Amount'] = np.NAN
df_mortgage['Interest_Type'] = "Fixed"
df_mortgage['Mortgage_Category'] = "New Purchase"
df_mortgage['Mortgage_Reason'] = "Primary Residence"
df_mortgage['Mortgage_Pymt_Mode'] = "Principal + Interest"
df_mortgage['Source'] = "Bank Website"

# In[13]:


df_mortgage.columns


# In[14]:


arranged_cols = ['Date', 'Bank_Native_Country','State','Bank_Name', 'Bank_Local_Currency','Bank_Type','Bank_Product', 'Bank_Product_Type','Bank_Product_Code','Bank_Product_Name','Min_Loan_Amount','Bank_Offer_Feature','Term_in_Year','Interest_Type','Interest','APR','Mortgage_Loan_Amt','Mortgage_Down_Payment', 'Credit_Score','Mortgage_Category', 'Mortgage_Reason','Mortgage_Pymt_Mode','Source']


# In[15]:


df_mortgage = df_mortgage.reindex(columns= arranged_cols)


# In[16]:


for idx in range(len(df_mortgage.index)):
    if "ARM" in df_mortgage['Bank_Product_Name'].iloc[idx] or "Adjustable Rate" in df_mortgage['Bank_Product_Name'].iloc[idx] or "/" in str(df_mortgage['Bank_Product_Name'].iloc[idx]):
        df_mortgage['Interest_Type'].iloc[idx] = "Variable"


# In[17]:


for idx in range(len(df_mortgage.index)):
    #print(df_mortgage['Bank_Product_Name'].iloc[idx])
    #print(type(df_mortgage['Bank_Product_Name'].iloc[idx]))
    df_mortgage['Bank_Product_Code'].iloc[idx] = "{0}{1}{2}{3}".format(int(df_mortgage['Term_in_Year'].iloc[idx]),"Y", "M", df_mortgage['Interest_Type'].iloc[idx][0])
    #print(df_mortgage['Interest_Type'].iloc[idx])


# In[18]:

df_mortgage = df_mortgage[df_mortgage.Term_in_Year != 25.0]

df_ticker = pd.read_csv(input_path+"Bank_Ticker_US.csv")
result = pd.merge(df_mortgage, df_ticker, how='left', on='Bank_Name')
arranged_cols = ['Date', 'Bank_Native_Country','State','Bank_Name','Ticker','Bank_Local_Currency','Bank_Type','Bank_Product', 'Bank_Product_Type','Bank_Product_Code','Bank_Product_Name','Min_Loan_Amount','Bank_Offer_Feature','Term_in_Year','Interest_Type','Interest','APR','Mortgage_Loan_Amt','Mortgage_Down_Payment', 'Credit_Score','Mortgage_Category', 'Mortgage_Reason','Mortgage_Pymt_Mode','Source']
df_mortgage = result.reindex(columns= arranged_cols)


for idx in range(len(df_mortgage.index)):
    df_mortgage["Mortgage_Loan_Amt"].iloc[idx] = str(df_mortgage["Mortgage_Loan_Amt"].iloc[idx]).replace(",","")
    df_mortgage['Mortgage_Loan_Amt'].iloc[idx] = str(df_mortgage['Mortgage_Loan_Amt'].iloc[idx]).lstrip("$")
df_mortgage['Mortgage_Loan_Amt'] = df_mortgage['Mortgage_Loan_Amt'].str.replace("nan", "")
df_mortgage.drop_duplicates(subset=None, keep='first', inplace=False)

df_mortgage.to_csv(output_path+"US\\" + "US_Mortgage_Data_{}.csv".format(now.strftime("%Y_%m_%d")), index=False )
