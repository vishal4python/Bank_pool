import requests
import pandas as pd
import datetime
import re
import time
from tabulate import tabulate
from maks_lib import output_path

print('Program Execution Started...')
today = datetime.datetime.now()
start_time = time.time()

#CSV File Location.
path = output_path+'Consolidate_Synchrony_new_Data_Deposits_'+today.strftime('%m_%d_%Y')+'.csv'

#Required Fields for scraping the data
table_headers = ['Bank_Product_Name', 'Product_Term', 'Balance', 'Product_Apy', 'Bank_Product_Type']

Excel_table = []


url =[["https://www.synchronybank.com/sites/Satellite?d=&pagename=GetRates&type=retail&product=CD",'CD','CD',None],
      ["https://www.synchronybank.com/sites/Satellite?d=&pagename=GetRates&type=retail&product=MMA",'MMA','Savings','Money Market Rates and Terms'],
      ['https://www.synchronybank.com/sites/Satellite?d=&pagename=GetRates&type=retail&product=HYS','HYS','Savings','HYS Rates and Terms']]
for urls in url:
    # Getting API by Sending url through requests module in python
    response = requests.get(urls[0]).json()
    for data in response[urls[1]]:
        if urls[3] is not None:
            product_name = urls[3]

            for k in data['Rates']:
                s = str(k['Low_BAL'])+'-'+str(k['High_BAL'])
                APY_RATE = k['APY_RATE']
                a = [product_name,None,s, str(APY_RATE)+'%',urls[2]]
                Excel_table.append(a)
        else:
            term = re.findall(r'\d+', data['TERM'])[0]
            product_name = data['TERM']

            for k in data['Rates']:
                APY_RATE = k['APY_RATE']
                a = [str('CD_')+product_name,term, str(k['Low_BAL'])+'+',str(APY_RATE)+'%',urls[2]]
                Excel_table.append(a)

                break

print(tabulate(Excel_table))
#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
#Arrange all fileds based on required format
order= ['Date', 'Bank_Name', 'Bank_Product', 'Bank_Product_Type', 'Bank_Offer_Feature','Bank_Product_Name', 'Product_Term', 'Balance', 'Product_Interest','Product_Apy','Mortgage_Down_Payment','Mortgage_Loan','Min_Credit_Score_Mortagage','Mortgage_Apr']
df = pd.DataFrame(Excel_table, columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Name'] = 'SYNCHRONY'
df['Bank_Product'] = 'Deposits'
df['Bank_Offer_Feature'] = 'Online'
df['Product_Interest'] = None
df['Mortgage_Down_Payment'] = None
df['Mortgage_Loan'] = None
df['Min_Credit_Score_Mortagage'] = None
df['Mortgage_Apr'] =None
df = df[order]
df.to_csv(path, index=False) #Moving Data to Csv.


print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')




