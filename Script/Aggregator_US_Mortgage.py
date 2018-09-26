
# coding: utf-8

# In[121]:


import glob
import os
import pandas as pd
import numpy as np
import datetime
import re
import warnings
#output_path = "C:\\Users\\vishal\\PycharmProjects\\pool-master\\data\\output\\US"
output_path = "C:\\Users\\vishal\\PycharmProjects\\pool-master\\data\\output\\"
input_path =  "C:\\Users\\vishal\\PycharmProjects\\pool-master\\data\\input\\"
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

extension = 'csv'


# In[122]:


agg_files = glob.glob(output_path+'*.{}'.format(extension))
agg_mortage_files  = [file for file in agg_files if file.split("\\")[-1].startswith("Aggregator") and "Mortgage" in file.split("\\")[-1]]
agg_deposite_files = [file for file in agg_files if file.split("\\")[-1].startswith("Aggregator") and file not in agg_mortage_files]


# In[123]:


agg_mortage_files


# In[124]:


for val in agg_mortage_files:
    df = pd.read_csv(val)
    print(df.shape[1],df.columns)


# In[125]:


COLUMN_NAMES = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name', 'Ticker',
       'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Product_Code', 'Bank_Product_Name', 'Min_Loan_Amount',
       'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest', 'APR',
       'Mortgage_Loan_Amt', 'Mortgage_Down_Payment', 'Mortgage_Category',
       'Mortgage_Reason', 'Mortgage_Pymt_Mode', 'Source']
df_mortgage = pd.DataFrame(columns=COLUMN_NAMES)


# In[126]:


for file in agg_mortage_files:
    df_temp =pd.read_csv(file)
    df_mortgage = pd.concat([df_mortgage, df_temp])


# In[127]:


df_mortgage.rename(columns={'Term (Y)': 'Term_in_Year'}, inplace=True)


# In[128]:


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
df_mortgage['Credit_Score'] = "720+"


# In[129]:


df_mortgage.drop(columns=['Ticker'], inplace = True)


# In[130]:


for idx in range(len(df_mortgage.index)):
    if "ARM" in df_mortgage['Bank_Product_Name'].iloc[idx] or "Adjustable Rate" in df_mortgage['Bank_Product_Name'].iloc[idx] or "/" in str(df_mortgage['Bank_Product_Name'].iloc[idx]):
        df_mortgage['Interest_Type'].iloc[idx] = "Variable"


# In[131]:


for idx in range(len(df_mortgage.index)):
    try:
        df_mortgage['Bank_Product_Code'].iloc[idx] = "{0}{1}{2}{3}".format(int(df_mortgage['Term_in_Year'].iloc[idx]),"Y", "M", df_mortgage['Interest_Type'].iloc[idx][0])
    except ValueError:
        df_mortgage["Term_in_Year"] = 30
        df_mortgage['Bank_Product_Code'].iloc[idx] = "{0}{1}{2}{3}".format(int(df_mortgage['Term_in_Year'].iloc[idx]),"Y", "M", df_mortgage['Interest_Type'].iloc[idx][0])

df_mortgage = df_mortgage[df_mortgage.Term_in_Year != 25.0]




# In[132]:


df_ticker = pd.read_csv(input_path+"Bank_Ticker_US.csv")


# In[136]:


result = pd.merge(df_mortgage, df_ticker, how='left', on='Bank_Name')


# In[138]:


arranged_cols = ['Date', 'Bank_Native_Country','State','Bank_Name','Ticker','Bank_Local_Currency','Bank_Type','Bank_Product', 'Bank_Product_Type','Bank_Product_Code','Bank_Product_Name','Min_Loan_Amount','Bank_Offer_Feature','Term_in_Year','Interest_Type','Interest','APR','Mortgage_Loan_Amt','Mortgage_Down_Payment', 'Credit_Score','Mortgage_Category', 'Mortgage_Reason','Mortgage_Pymt_Mode', 'Source']
df_mortgage = result.reindex(columns= arranged_cols)


for idx in range(len(df_mortgage.index)):
    df_mortgage["Mortgage_Loan_Amt"].iloc[idx] = str(df_mortgage["Mortgage_Loan_Amt"].iloc[idx]).replace(",","")
    df_mortgage['Mortgage_Loan_Amt'].iloc[idx] = str(df_mortgage['Mortgage_Loan_Amt'].iloc[idx]).lstrip("$")
df_mortgage['Mortgage_Loan_Amt'] = df_mortgage['Mortgage_Loan_Amt'].str.replace("nan", "")
df_mortgage.drop_duplicates(subset=None, keep='first', inplace=False)

df_mortgage.to_csv(output_path+"US\\" + "Aggregator_US_Mortgage_Data_{}.csv".format(now.strftime("%Y_%m_%d")), index=False )

