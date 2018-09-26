
# coding: utf-8

# In[71]:


import glob
import os
import pandas as pd
import numpy as np
import datetime
import re
import warnings
from maks_lib import output_path
from maks_lib import input_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

extension = 'csv'


# In[72]:


all_files = glob.glob(output_path+'*.{}'.format(extension))
all_mortage_files  = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and "Mortgage" in file.split("\\")[-1]]
all_deposite_files = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and file not in all_mortage_files]


# In[73]:


COLUMN_NAMES = list(pd.read_csv(all_mortage_files[0]).columns)
df_mortgage = pd.DataFrame(columns=COLUMN_NAMES) 
df_deposit = pd.DataFrame(columns=COLUMN_NAMES)


# In[74]:


for idx, file in enumerate(all_deposite_files):
    print(file)
    print(pd.read_csv(all_deposite_files[idx]).shape[1])


# In[75]:


for file in all_deposite_files:
    df_temp =pd.read_csv(file)
    df_temp.columns = ['Date', 'Bank_Name', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Offer_Feature', 'Bank_Product_Name', 'Product_Term', 'Balance',
       'Product_Interest', 'Product_Apy', 'Mortgage_Down_Payment',
       'Mortgage_Loan', 'Min_Credit_Score_Mortagage', 'Mortgage_Apr']
    df_deposit = pd.concat([df_deposit, df_temp])


# In[76]:


df_deposit.shape


# In[77]:


df_deposit


# In[78]:


df_deposit.dropna(axis=0, how='all', inplace=True)


# In[79]:


df_deposit.drop(columns=['Mortgage_Down_Payment','Mortgage_Loan', 'Min_Credit_Score_Mortagage', 'Mortgage_Apr'], inplace=True)


# In[80]:


df_deposit.rename(columns={"Product_Term": "Term_in_Months","Product_Interest": "Interest","Product_Apy":"APY"}, inplace = True,index=str)


# In[81]:


df_deposit['Date'] = " {}".format(now.strftime("%Y-%m-%d"))
df_deposit['Bank_Native_Country'] = "US"
df_deposit['State'] = "New York"
df_deposit['Bank_Local_Currency'] = "USD"
df_deposit['Bank_Type'] = "Bank"
df_deposit['Bank_Product'] = "Deposits"
df_deposit['Bank_Product_Code'] = np.NAN
df_deposit['Interest_Type'] = "Variable"
df_deposit['Minm_Balance'] = np.NAN
df_deposit['Maxm_Balance'] = np.NAN
df_deposit['Source'] = "Bank Website"

# In[82]:


arranged_cols = ['Date', 'Bank_Native_Country','State','Bank_Name','Bank_Local_Currency', 'Bank_Type','Bank_Product','Bank_Product_Type','Bank_Product_Code','Bank_Product_Name','Balance','Minm_Balance','Maxm_Balance','Bank_Offer_Feature','Term_in_Months', 'Interest_Type','Interest', 'APY','Source']


# In[83]:


df_deposit = df_deposit.reindex(columns= arranged_cols)


# In[84]:


for idx in range(len(df_deposit.index)):
    if "Savings" in df_deposit['Bank_Product_Type'].iloc[idx]:
        df_deposit['Interest_Type'].iloc[idx] = "Fixed"

for idx in range(len(df_deposit.index)):
    if "CD" in df_deposit['Bank_Product_Type'].iloc[idx]:
        df_deposit['Interest_Type'].iloc[idx] = "Fixed"

for idx in range(len(df_deposit.index)):
    if "Checking" in df_deposit['Bank_Product_Type'].iloc[idx]:
        df_deposit['Interest_Type'].iloc[idx] = "Fixed"
# In[85]:


for idx in range(len(df_deposit.index)):
    #print(df_mortgage['Bank_Product_Name'].iloc[idx])
    #print(type(df_mortgage['Bank_Product_Name'].iloc[idx]))
    #  CD  
    
    if "Savings" in df_deposit['Bank_Product_Type'].iloc[idx]:
        s = "SB"
    elif "Checking" in df_deposit['Bank_Product_Type'].iloc[idx]:
        s = "CC"
    else:
        s = "CD"
    try:
        t = int(df_deposit['Term_in_Months'].iloc[idx])
    except ValueError:
        t = "_"        
    df_deposit['Bank_Product_Code'].iloc[idx] = "{0}{1}{2}{3}".format(t,"M", s, df_deposit['Interest_Type'].iloc[idx][0])
    #print(df_mortgage['Interest_Type'].iloc[idx])


# In[86]:


df_deposit.head()


# In[87]:


for idx in range(len(df_deposit.index)):
    if "Below" in str(df_deposit['Balance'].iloc[idx]) or "or less" in str(df_deposit['Balance'].iloc[idx]) or "Less than" in str(df_deposit['Balance'].iloc[idx]) or "less than" in str(df_deposit['Balance'].iloc[idx]) or "Up to" in str(df_deposit['Balance'].iloc[idx]):
        df_deposit['Maxm_Balance'].iloc[idx] = df_deposit['Balance'].iloc[idx]
    elif "-" in str(df_deposit['Balance'].iloc[idx]):
        df_deposit['Minm_Balance'].iloc[idx], df_deposit['Maxm_Balance'].iloc[idx] = str(df_deposit['Balance'].iloc[idx]).split("-")
    elif " to " in str(df_deposit['Balance'].iloc[idx]):
        df_deposit['Minm_Balance'].iloc[idx], df_deposit['Maxm_Balance'].iloc[idx] = str(df_deposit['Balance'].iloc[idx]).split("to")
    else:
        df_deposit['Minm_Balance'].iloc[idx] = df_deposit['Balance'].iloc[idx]


# In[88]:


df_deposit.drop(columns=['Balance'], inplace=True)


# In[89]:


for idx in range(len(df_deposit.index)):
    text1 = str(df_deposit['Maxm_Balance'].iloc[idx])    
    result = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", text1)
    try:
        df_deposit['Maxm_Balance'].iloc[idx] = result[0]
    except IndexError:
        df_deposit['Maxm_Balance'].iloc[idx] = np.NAN
        
    text2 = str(df_deposit['Minm_Balance'].iloc[idx])    
    result = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", text2)
    try:
        df_deposit['Minm_Balance'].iloc[idx] = result[0]
    except IndexError:
        df_deposit['Minm_Balance'].iloc[idx] = np.NAN


# In[90]:


df_deposit["Minm_Balance"] = df_deposit["Minm_Balance"].str.replace(",","")
df_deposit["Maxm_Balance"] = df_deposit["Maxm_Balance"].str.replace(",","")


# In[93]:


for idx in range(len(df_deposit.index)):
    df_deposit['Minm_Balance'].iloc[idx] = str(df_deposit['Minm_Balance'].iloc[idx]).split(".")[0]
    df_deposit['Maxm_Balance'].iloc[idx] = str(df_deposit['Maxm_Balance'].iloc[idx]).split(".")[0]
df_deposit['Minm_Balance'] = df_deposit['Minm_Balance'].str.replace("nan", "")
df_deposit['Maxm_Balance'] = df_deposit['Maxm_Balance'].str.replace("nan", "")

df_ticker = pd.read_csv(input_path+"Bank_Ticker_US.csv")
result = pd.merge(df_deposit, df_ticker, how='left', on='Bank_Name')

arranged_cols = ['Date', 'Bank_Native_Country','State','Bank_Name','Ticker','Bank_Local_Currency', 'Bank_Type','Bank_Product','Bank_Product_Type','Bank_Product_Code','Bank_Product_Name','Minm_Balance','Maxm_Balance','Bank_Offer_Feature','Term_in_Months', 'Interest_Type','Interest', 'APY','Source']
df_deposit = result.reindex(columns= arranged_cols)

# In[94]:

df_deposit = df_deposit[((df_deposit.Bank_Product_Type == "CD") & (df_deposit.Term_in_Months.isin([6.0,12.0,36.0]))) |(df_deposit.Bank_Product_Type != "CD") ]
df_deposit.drop_duplicates(subset=None, keep='first', inplace=False)
df_deposit.to_csv(output_path+"US\\" + "US_Deposits_Data_{}.csv".format(now.strftime("%Y_%m_%d")), index=False )

