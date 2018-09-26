
# coding: utf-8

# In[41]:


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


# In[42]:


all_files = glob.glob(output_path+'*.{}'.format(extension))
all_mortage_files  = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and "Mortgage" in file.split("\\")[-1]]
all_deposite_files = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and file not in all_mortage_files]


# In[43]:


COLUMN_NAMES = list(pd.read_csv(all_mortage_files[0]).columns)
df_mortgage = pd.DataFrame(columns=COLUMN_NAMES) 
df_deposit = pd.DataFrame(columns=COLUMN_NAMES)


# In[44]:


for idx, file in enumerate(all_deposite_files):
    print(file)
    print(pd.read_csv(all_deposite_files[idx]).shape[1])


# In[45]:


for file in all_deposite_files:
    df_temp =pd.read_csv(file)
    df_temp.columns = ['Date', 'Bank_Name', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Offer_Feature', 'Bank_Product_Name', 'Term_in_Year', 'Balance',
       'Interest', 'APY', 'Mortgage_Down_Payment',
       'Mortgage_Loan', 'Credit_Score', 'Mortgage_Apr']
    df_deposit = pd.concat([df_deposit, df_temp])


# In[46]:


df_deposit.shape


# In[47]:


df_deposit


# In[48]:


df_deposit.dropna(axis=0, how='all', inplace=True)


# In[49]:


df_deposit.drop(columns=['Mortgage_Down_Payment','Mortgage_Loan', 'Credit_Score', 'Mortgage_Apr'], inplace=True)


# In[50]:


df_deposit.rename(columns={"Term_in_Year": "Term_in_Year","Interest": "Interest","APY":"APY"}, inplace = True,index=str)


# In[51]:


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


# In[52]:


arranged_cols = ['Date', 'Bank_Native_Country','State','Bank_Name','Bank_Local_Currency', 'Bank_Type','Bank_Product','Bank_Product_Type','Bank_Product_Code','Bank_Product_Name','Balance','Minm_Balance','Maxm_Balance','Bank_Offer_Feature','Term_in_Year', 'Interest_Type','Interest', 'APY']


# In[53]:


df_deposit = df_deposit.reindex(columns= arranged_cols)


# In[54]:


for idx in range(len(df_deposit.index)):
    if "CD" in df_deposit['Bank_Product_Type'].iloc[idx]:
        df_deposit['Interest_Type'].iloc[idx] = "Fixed"


# In[55]:


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
        t = int(df_deposit['Term_in_Year'].iloc[idx])
    except ValueError:
        t = "_"        
    df_deposit['Bank_Product_Code'].iloc[idx] = "{0}{1}{2}{3}".format(t,"M", s, df_deposit['Interest_Type'].iloc[idx][0])
    #print(df_mortgage['Interest_Type'].iloc[idx])


# In[56]:


df_deposit.head()


# In[57]:


for idx in range(len(df_deposit.index)):
    if "Below" in str(df_deposit['Balance'].iloc[idx]) or "or less" in str(df_deposit['Balance'].iloc[idx]) or "Less than" in str(df_deposit['Balance'].iloc[idx]) or "less than" in str(df_deposit['Balance'].iloc[idx]) or "Up to" in str(df_deposit['Balance'].iloc[idx]):
        df_deposit['Maxm_Balance'].iloc[idx] = df_deposit['Balance'].iloc[idx]
    elif "-" in str(df_deposit['Balance'].iloc[idx]):
        df_deposit['Minm_Balance'].iloc[idx], df_deposit['Maxm_Balance'].iloc[idx] = str(df_deposit['Balance'].iloc[idx]).split("-")
    elif " to " in str(df_deposit['Balance'].iloc[idx]):
        df_deposit['Minm_Balance'].iloc[idx], df_deposit['Maxm_Balance'].iloc[idx] = str(df_deposit['Balance'].iloc[idx]).split("to")
    else:
        df_deposit['Minm_Balance'].iloc[idx] = df_deposit['Balance'].iloc[idx]


# In[58]:


df_deposit.drop(columns=['Balance'], inplace=True)


# In[59]:


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


# In[60]:

df_deposit = df_deposit[((df_deposit.Bank_Product_Type == "CD") & (df_deposit.Term_in_Year.isin([6.0,12.0,36.0]))) |(df_deposit.Bank_Product_Type != "CD") ]
df_deposit.to_csv(output_path+"US\\" + "US_Deposits_Data_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )

