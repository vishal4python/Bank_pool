
import requests
import numpy as np
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import time
import re
import datetime
from maks_lib import output_path

print('Program Execution Started Please wait....')
startTime = time.time()
Excel_Table = []

today = datetime.datetime.now()

#Required Fields for scraping the data
table_headers = ['Bank_Name', 'Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term_in_Months', 'Interest', 'APY']

#Csv file Location
path = output_path+"Aggregator_Nerdwallet_Data_Deposit"+today.strftime('%Y_%m_%d')+".csv"

#Making Bank_Offer_Feature Online or Offline based on online_banks
online_bank = [k.lower() for k in ['Synchrony Bank', 'Ally Bank', 'Capital One 360']]

#Filternig Required Bank Names by using neededUsBanks
neededBanks = {
    "Ally Bank":'ALLY',
    "Bank of America":"BANK OF AMERICA CORP",
    "Capital One":"CAPITAL ONE",
    "Capital One 360":"CAPITAL ONE",
    "Chase":"JP MORGAN CHASE & Co.",
    "Citibank":"CITIGROUP INC",
    "PNC":"PNC FINANCIAL SERVICES GROUP INC",
    "Synchrony Bank":"SYNCHRONY",
    "Wells Fargo":"WELLS FARGO",
    "SunTrust":"SUNTRUST BANKS INC"

}


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
           'X-Caller-Client-ID':'banking-client'}
urlDict = [('Savings Accounts','https://www.nerdwallet.com/rates/savings-account?active_offers=true&bank_type=bank&bank_type=internet_bank&deposit_minimum=10000&min_ratings=All+ratings&sort_key=apy&sort_order=desc&sub_product_type=SAVINGS&zip_code=10004'),
           ('Checking Account','https://www.nerdwallet.com/checking-accounts?active_offers=true&bank_type=bank&bank_type=internet_bank&checking_daily_balance=0&customer_type=everyone&direct_deposit=0&sort_key=monthly_cost&sort_order=desc&sub_product_type=CHECKING&zip_code=10004'),
            ('CD','https://www.nerdwallet.com/rates/cds/best-cd-rates?active_offers=true&bank_type=bank&bank_type=credit_union&bank_type=internet_bank&deposit_minimum=25000&length_of_term=1800&min_ratings=4&sort_key=apy&sort_order=desc&sub_product_type=CD&zip_code=10004')
]

#CD

#Getting API data by using requests module
resp = requests.get(urlDict[2][1]+'&page=1').content
pages = BeautifulSoup(resp, 'html.parser').find('div', attrs={'class': 'pagination'}).find_all('a')
for i in range(1,len(pages)+1):
    print('https://api.nerdwallet.com/banking-products/v1/rates?sort_key=apy&sort_order=desc&page='+str(i)+'&zip_code=10004&deposit_minimum=25000&length_of_term=1800&min_ratings=4&bank_type=bank%2Cinternet_bank%2Ccredit_union&sub_product_type=CD&active_offers=true')
    resp = requests.get('https://api.nerdwallet.com/banking-products/v1/rates?sort_key=apy&sort_order=desc&page='+str(i)+'&zip_code=10004&deposit_minimum=25000&length_of_term=1800&min_ratings=4&bank_type=bank%2Cinternet_bank%2Ccredit_union&sub_product_type=CD&active_offers=true',headers=headers).json()
    for offer in  resp['data']['offers']:
        product_name = offer['product']['details']['display_name']['value']
        apy = offer['details']['apy']['value']
        Bank_name = offer['product']['institution']['details']['banking_display_name']['value']
        minimum_balance = offer['details']['minimum_balance']['value']
        days = offer['product']['details']['ratewatch_comment']['value']
        if Bank_name in neededBanks:

            a = [neededBanks[Bank_name], 'CD', product_name, minimum_balance, 'Online' if Bank_name.lower() in online_bank else 'Offline', days,'Interest', str(float(apy))+'%']
            Excel_Table.append(a)

#====================================================================================================================
#Checking Account

#Getting API data by using requests module
resp = requests.get(urlDict[1][1] + '&page=1').content
pages = BeautifulSoup(resp,'html.parser').find('div', attrs={'class': 'pagination'}).find_all('a')
for i in range(1,len(pages)+1):
    resp = requests.get('https://api.nerdwallet.com/banking-products/v1/rates?sort_key=monthly_cost&sort_order=desc&page='+str(i)+'&zip_code=10004&checking_daily_balance=0&direct_deposit=0&bank_type=bank%2Cinternet_bank&customer_type=everyone&sub_product_type=CHECKING&active_offers=true', headers=headers).json()
    for offer in  resp['data']['offers']:
        Bank_name = offer['product']['institution']['details']['banking_display_name']['value']
        fee = offer['details']['balance_to_avoid_fees']['value']
        product_name = offer['details']['display_name']['value']
        online = offer['product']['institution']['details']['banking_branch_count']['value']
        if online is None:
            online = 'Online'
        else:
            online = 'Offline'

        if Bank_name in neededBanks:
            if Bank_name.lower() in online_bank:
                online = 'Online'
            a = [neededBanks[Bank_name], 'Checking', product_name, fee, online, 'Term_in_Months', 'Interest', np.nan]
            Excel_Table.append(a)

#=====================================================================================================================
#Savings

#Getting API data by using requests module
resp = requests.get(urlDict[0][1] + '&page=1').content
pages = BeautifulSoup(resp,'html.parser').find('div', attrs={'class': 'pagination'}).find_all('a')
for i in range(1,len(pages)+1):
    resp = requests.get('https://api.nerdwallet.com/banking-products/v1/rates?sort_key=apy&sort_order=desc&page='+str(i)+'&zip_code=10004&deposit_minimum=10000&min_ratings=All%20ratings&bank_type=bank%2Cinternet_bank&sub_product_type=SAVINGS&active_offers=true', headers=headers)
    data = resp.json()
    for offer in  data['data']['offers']:
        bank_name = offer['product']['institution']['name']
        if bank_name in neededBanks:

            a = [neededBanks[bank_name], 'Savings', offer['product']['details']['display_name']['value'], offer['details']['minimum_balance']['value'], "Online" if bank_name.lower() in online_bank else 'Offline', 'Term_in_Months', 'Interest', str(float(offer['details']['apy']['value']))+'%']
            Excel_Table.append(a)
print(tabulate(Excel_Table))

#Arrange all fileds based on required format
order = ["Date","Bank_Native_Country", "State","Bank_Name",'Bank_Local_Currency', "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term_in_Months", "Interest_Type", "Interest", "APY"]

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
df = pd.DataFrame(Excel_Table[1:], columns=table_headers)
def termClear(x):
    if x is None:
        return None
    if 'year' in x.lower():
        return int(re.findall('\d.* ',x)[0])*12
    else:
        return re.sub('[^0-9]','',x) if len(re.sub('[^0-9]','',x))!=0 else np.nan
def product_name_checker(x):
    if 'SAV' in x:
        return 'Savings Account'
    elif 'MCD' in x:
        return 'Certificate of Deposit'
    else:
        return x

Excel_Table.append(table_headers)
df['Interest'] = np.nan
df['Date'] = today.strftime('%m-%d-%Y')
df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Interest_Type'] = 'Fixed'
df['Bank_Product_Code'] = np.nan
df['Term_in_Months'] = df['Term_in_Months'].apply(termClear)
df['Bank_Offer_Feature'] = df['Bank_Offer_Feature'].apply(lambda x:'Online' if 'online' in x.lower() else 'Offline')
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(product_name_checker)
df = df[order]
df['Source'] = 'nerdwallet.com'
df.to_csv(path, index=False)     #Moving data to CSV File.

print('Exection Completed.')
print('Total Execution Time:',time.time()-startTime,' Seconds')         #Display total execution time.
