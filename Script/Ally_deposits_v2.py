
from bs4 import BeautifulSoup
from tabulate import  tabulate
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import datetime
today = datetime.datetime.now()
from maks_lib import output_path

static_banknae = 'Ally'
print('Program Exection Started...')
Excel_Data =[]
path = output_path+'Consolidate_ALLY_Data_Deposit_'+today.strftime('%m_%d_%Y')+'.csv' #Location of a file to store the data
table_headers = ['Bank_Product_Name','Bank_Product_Type','Product_Term', 'Balance', 'Product_Apy'] #Required Fields to scrap the data.

start_time = time.time()
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options) #Create one FireFox driver
driver.maximize_window()
print('Browser Loaded')
print('Please wait scraping is runnning...')

#---------------------------------Checking Account-----------------------------------------------
driver.get('https://www.ally.com/bank/interest-checking-account/') #Pass the required Scraping url
checkings = BeautifulSoup(driver.page_source).find('main', attrs={'id':'content'})
checkName = checkings.find('h1').text
for k in checkings.find_all('div', attrs={'class':'sm-col-12 md-col-4', 'role':'presentation'}):
    try:
        data = k.text
        APY = re.search('\d.*%', data)
        if '%' in data:
            Balance = data[data.index('%') + 1:]
        else:
            Balance = data

        APY = APY.group(0) if APY is not None else None
        a = [checkName.strip(), 'Checking', None, Balance, APY]
        Excel_Data.append(a)
    except Exception as e:
        print(e)


#------------------------------------Savings Account----------------------------------------------
driver.get('https://www.ally.com/bank/savings-account-rates/') #Pass the required Scraping url
half = BeautifulSoup(driver.page_source).find('div', attrs={'class':'compare-box'}).find_all('div', attrs={'class':'half'})
li = ['Savings']
for k in range(len(half)):
    try:
        online = half[k].find('h2').text
        for k in half[k].find('div', attrs={'class':'rate-module'}).find('div', attrs={'role':'tabpanel'}).find_all('div'):
            data = k.text
            APY = re.search('\d.*%', data)
            if '%' in data:
                Balance = data[data.index('%') + 1:]
            else:
                Balance = data
            # Balance = re.search('\$\d.*\d ', data)
            # Balance = Balance.group(0) if Balance is not None else None
            APY = APY.group(0) if APY is not None else None
            a = [online.strip(), 'Savings', None, Balance, APY]
            Excel_Data.append(a)
    except Exception as e:
        print(e)

#----------------------------------------CD-------------------------------------------------------
urls = [['https://www.ally.com/bank/cd-rates/', 'CD'], ['https://www.ally.com/bank/ira/ira-account/','']]
for url in urls[:1]:
    try:
        driver.get(url[0])  #Pass the required Scraping url
        divs = BeautifulSoup(driver.page_source).find('div', attrs={'class':'compare-box'}).find_all('div', attrs={'class':'third'})
        for k in range(len(divs)):
            for tab in divs[k].find_all('div', attrs={'role':'tabpanel'}):
                name1 = divs[k].find('h2').text
                term = tab['data-term']
                for div in tab.find_all('div'):
                    data = div.text
                    print(data)
                    APY = re.search('\d.*%',data)
                    if '%' in data:
                        Balance = data[data.index('%')+1:]
                    else:
                        Balance = data

                    APY =  APY.group(0) if APY is not None else None
                    find = [6, 12, 36]
                    if int(term) in find:
                        a = [name1.strip()+'_'+str(term)+' Months',url[1], term, Balance,  APY]
                        Excel_Data.append(a)
    except Exception as e:
        print(e)
try:
    driver.close()
except Exception as e:
    print(e)
print('Browser Closed Successfully.')
print(tabulate(Excel_Data))

#------------------------------------Moving Data to CSV File using Pandas----------------------------------------------

# Arrange the Order of all fields.
order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term",
         "Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage","Mortgage_Apr"]
df = pd.DataFrame(Excel_Data, columns=table_headers)
df['Date'] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'ALLY'
df['Bank_Product'] = 'Deposits'
df['Bank_Offer_Feature'] = 'Online'
df['Product_Interest'] = None
df['Mortgage_Down_Payment'] = None
df['Mortgage_Loan'] = None
df['Min_Credit_Score_Mortagage'] = None
df['Mortgage_Apr'] = None
df = df[order]
df.to_csv(path, index=False)

print('Total Execution Time is ',time.time()-start_time,'Seconds') #Displaying total execution time.