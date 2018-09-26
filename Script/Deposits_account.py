import requests
import numpy as np
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
import pandas as pd
import time
import datetime
from maks_lib import output_path

print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()
Excel_Table = []

#Csv file Location.
path = output_path+"Aggregator_DepositAccount_Data_Deposit"+today.strftime('%Y_%m_%d')+".csv"

#Required Fields for scraping the data
table_headers=['APY','Balance','Bank_Name','Bank_Product_Name','Bank_Product_Type','Term_in_Months','Bank_Offer_Feature']
Excel_Table.append(table_headers)





#Making Bank_Offer_Feature Online or Offline Based on online_bank
online_bank = ['Synchrony Bank', 'Ally Bank', 'Capital One 360']

#Filter Banks names based on needeBanks
neededBanks = {
    "Ally Bank":'ALLY',
    "Bank of America":"BANK OF AMERICA CORP",
    "Capital One":"CAPITAL ONE",
    "Capital One 360":"CAPITAL ONE",
    "Chase Bank":"JP MORGAN CHASE & Co.",
    "Citibank":"CITIGROUP INC",
    "PNC Bank":"PNC FINANCIAL SERVICES GROUP INC",
    "Synchrony Bank":"SYNCHRONY",
    "Wells Fargo Bank":"WELLS FARGO",
    "SunTrust Bank":"SUNTRUST BANKS INC"

}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
           'X-Caller-Client-ID':'banking-client'}


countList = [0,40]
types = [[9,'Savings'],[13,'Checking'],[2,'CD'],[3,'CD'],[6,'CD']]
check = ["Savings", "Checking"]
for i in countList:
    for j in types:
        #Getting pageSource by Sending post data and url through requests module in python
        resp = requests.post('https://www.depositaccounts.com/ajax/rates.aspx?productId='+str(j[0])+'&amount=25000&start='+str(i)+'&web=1&branches=1&banks=1&state=CT&dma=501&cuIndustries=&legacy=false').content

        #Getting required fields data by using python BeautifulSoup Module.
        divs = BeautifulSoup(resp, 'html.parser').find_all('div', attrs={'id':re.compile('a')})
        for div in divs:
            apy = re.sub('[^0-9.%]', '', div.find('div', attrs={'class': 'apy'}).text)
            Balance = div.find('div', attrs={'class': 'info'}).find_all('span')
            Balance = str(Balance[0].text)+'-'+str(Balance[1].text)
            Bank_Name = div.find('a', attrs={'class': 'name'}).text.strip('\t').strip('-')
            Bank_Product_Name = div.find('div', attrs={'class': 'bank'}).find('span').text.strip('\t').strip('-')
            if j[1] in check:
                Term_in_Months = np.nan
            else:
                x= Bank_Product_Name
                if 'year' in x.lower():
                    Term_in_Months = int(re.sub('[^0-9]', '', re.findall('\d.* y', x, re.IGNORECASE)[0] if len(re.findall('\d.* y', x, re.IGNORECASE)) >= 1 else str(0))) * 12
                elif 'month' in x.lower():
                    if '-' in x:
                        x = x.split('-')[0] + ' month'
                    Term_in_Months = int(re.sub('[^0-9]', '', re.findall('\d.* m', x, re.IGNORECASE)[0] if len(re.findall('\d.* m', x, re.IGNORECASE)) >= 1 else str(0)))
                else:
                    Term_in_Months = np.nan

            if Bank_Name.strip() in neededBanks:
                if Bank_Name.strip() in online_bank:
                    Bank_Offer_Feature = 'Online'
                else:
                    Bank_Offer_Feature = 'Offline'
                #Appending Scrapped data to Excel_Table
                Excel_Table.append([apy, Balance, neededBanks[Bank_Name.strip()], Bank_Product_Name,j[1], Term_in_Months,Bank_Offer_Feature])


print(tabulate(Excel_Table))



#--------------------------------------Moving Data to CSV File using Pandas----------------------------------

#This method is useful for getting term into months.
def termClear(x):
    if x is  None:
        return None
    x = str(x)
    if 'year' in x.lower():
        return int(re.sub('[^0-9]','',re.findall('\d.* y',x,re.IGNORECASE)[0] if len(re.findall('\d.* y',x,re.IGNORECASE))>=1 else str(0)))*12
    elif 'month' in x.lower():
        if '-' in x:
            x = x.split('-')[0]+' month'
        return int(re.sub('[^0-9]', '', re.findall('\d.* m', x, re.IGNORECASE)[0] if len(re.findall('\d.* m', x, re.IGNORECASE)) >= 1 else str(0)))
    else:
        return re.sub('[^0-9]','',x) if len(re.sub('[^0-9]','',x))!=0 else np.nan

#Arrange all fileds based on required format
order = ["Date","Bank_Native_Country", "State","Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term_in_Months", "Interest_Type", "Interest", "APY", "Source"]
df = pd.DataFrame(Excel_Table[1:],columns=table_headers)
df['Interest'] = np.nan
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Interest_Type'] = 'Fixed'
df['Bank_Product_Code'] = np.nan
df['Source'] = 'DepositAccounts.com'
df['Balance'] = df['Balance'].apply(lambda x: re.sub('[^0-9-]','',str(x.replace('k','000').replace('m','000000'))).strip('-'))
df = df[order]
df.to_csv(path, index=False) #Moving Data to CSV File.



print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')