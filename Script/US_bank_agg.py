
# coding: utf-8

# In[43]:


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


all_files = glob.glob(output_path+"US\\"+'*.{}'.format(extension))


# In[44]:


output_path+"US\\"
#C:\Users\vishal\PycharmProjects\pool-master\data\output\US


# In[45]:


all_files


# In[46]:


bank_mortage_file  = [file for file in all_files if file.split("\\")[-1].startswith("US_Mortgage_Data") ]
bank_deposite_file = [file for file in all_files if file.split("\\")[-1].startswith("US_Deposits_Data") ]

agg_mortage_file  = [file for file in all_files if file.split("\\")[-1].startswith("Aggregator_US_Mortgage") ]
agg_deposite_file = [file for file in all_files if file.split("\\")[-1].startswith("Aggregate_US_Deposits") ]


# In[47]:


bank_mortage_file  = pd.read_csv(bank_mortage_file[0])
bank_deposite_file = pd.read_csv(bank_deposite_file[0])

agg_mortage_file  = pd.read_csv(agg_mortage_file[0])
agg_deposite_file = pd.read_csv(agg_deposite_file[0])


# In[48]:


df_deposit = pd.concat([bank_deposite_file, agg_deposite_file])
df_mortage = pd.concat([bank_mortage_file, agg_mortage_file])


# In[49]:


df_deposit.to_csv(output_path+"US\\" + "US_FINAL_Deposits_Data_{}.csv".format(now.strftime("%Y_%m_%d")), index=False )


# In[50]:


df_mortage.to_csv(output_path+"US\\" + "US_FINAL_Mortgage_Data_{}.csv".format(now.strftime("%Y_%m_%d")), index=False )

