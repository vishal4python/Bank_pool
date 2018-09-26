
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from tabulate import tabulate
from selenium.webdriver.firefox.options import Options
import pandas as pd
import datetime
import time
from maks_lib import output_path

print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()
Excel_Table = []

#Csv file location
path = output_path+'Consolidate_CapitalOne_Data_Deposit_'+today.strftime('%m_%d_%Y')+'.csv'

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
driver.maximize_window()
print('Browser Loaded')

#Required Fields for scraping the data
table_headers = ['Bank_Product_Type', 'Bank_Product_Name', 'Product_Term', 'Balance', 'Product_Interest', 'Product_Apy']

Excel_Table.append(table_headers)

#Getting pageSource by using selenium Module.
driver.get('https://www.capitalone.com/online-money-market-account/disclosures/')

#Getting Required data from oageSource using BeautifulSoup Module.
mma = BeautifulSoup(driver.page_source).find('rates', attrs={'product':'mma'})
if mma is not None:
    ul = mma.find('ul')
    if ul is not  None:
        for p in ul.find_all('p'):
            tag = ''
            p = p.text
            if 'less' in p.lower():
                tag = 'less than '
            elif 'more' in p.lower():
                tag = 'more than '

            Balance = re.search('\$[0-9,\.]*',p).group(0)
            p = re.findall('[0-9\.]*%',p)
            if len(p)!=0 and len(p)==2:
                rate = p[0]
                APY = p[1]
                Excel_Table.append(['Savings','360 Money Market', None, str(tag+Balance).strip('.').strip(','), rate, APY])


urls = [['360 Savings','savings','https://www.capitalone.com/savings-accounts/online-savings-account/disclosures/'],
        ['360 IRA Savings Traditional','ira','https://www.capitalone.com/terms-ira/']]
        # ['Money Checking','money','https://www.capitalone.com/teen-checking-account-money/disclosures/']]

for url in urls:
    driver.get(url[2])
    jsoup = BeautifulSoup(driver.page_source)
    Balance = jsoup.find('strong', text=re.compile('Initial Deposit Requirement',re.IGNORECASE))
    Balance = Balance.parent.text
    Balance = re.search('\$[0-9,\.]*',Balance)
    Balance = Balance.group(0) if Balance is not None else 0
    for p in jsoup.find('rates', attrs={'product':url[1]}).find_all('p'):
        p = p.text
        if Balance!=0:
            Balance = re.search('\$[0-9,\.]*', p)
            if Balance is not  None:
                Balance = Balance.group(0)
        p = re.findall('[0-9\.]*%', p)
        if len(p) != 0 and len(p) == 2:
            rate = p[0]
            APY = p[1]
            Excel_Table.append(['Savings', url[0], None, str(Balance).strip('.').strip(','), rate, APY])

driver.get('https://www.capitalone.com/cds/online-cds/disclosures/')
jsoup = BeautifulSoup(driver.page_source)
Balance = jsoup.find('strong', text='Initial Deposit Requirement')
Balance = Balance.parent.text
Balance = re.search('\$[0-9,\.]*',Balance)
Balance = Balance.group(0) if Balance is not None else 0
months = [6,12,36]
for tr in jsoup.find('rates', attrs={'product':'cds'}).find('table').find('tbody').find_all('tr'):
    try:
        tds = tr.find_all('td')
        month = int(re.sub('[^0-9]','',tds[0].text))
        if month in months:
            Excel_Table.append(['CD', '360 CDs '+str(month)+' months', month, str(Balance).strip('.').strip(','), tds[1].text.strip(), tds[2].text.strip()])

    except Exception as e:
        print(e)
try:
    driver.close()
except Exception as e:
    print(e)

print(tabulate(Excel_Table))

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
#Arrange all fileds based on required format
order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortgage","Mortgage_APR"]
df = pd.DataFrame(Excel_Table[1:], columns=table_headers)
df["Date"] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'CAPITAL ONE'
df['Bank_Product'] = 'Deposits'
df['Bank_Offer_Feature'] = 'Online'
df['Mortgage_Down_Payment'] = None
df['Mortgage_Loan'] = None
df['Min_Credit_Score_Mortgage'] = None
df['Mortgage_APR'] = None
df = df[order]
df.to_csv(path, index=False) #Moving Data to csv.

print('Total Execution Time:',time.time()-start_time,' Seconds') #Display total time taken to Execute the program
print('Execution Completed.')