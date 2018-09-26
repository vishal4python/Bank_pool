import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import numpy as np
import re
import datetime
from maks_lib import output_path
import time

print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()
Exceldata = []

#CSV File Location.
path = output_path+"Consolidate_WellsF_Data_Deposits_"+today.strftime("%m_%d_%Y")+'.csv'

#Required Fields for scraping the data
tableHeaders = ['Bank_Product_Type', 'Bank_Product_Name', 'Minimu_Balance','Balance', 'Product_Term', 'Product_Interest','Product_Apy']
Exceldata.append(tableHeaders)


post_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

# Getting pageSource by Sending post data and url through requests module in python
resp = requests.post('https://www.wellsfargo.com/savings-cds/rates',headers = post_headers, data={'zipCodeSelector':'10004'}).content

# Getting required fields data by using python BeautifulSoup Module.
jsoup = str(BeautifulSoup(resp, 'html.parser').find('div', attrs={'id':'mainColumns'}).find('div', attrs={'id':'contentBody'})).split('<h3>')



def TermInMOnths(T):
    if T is None:
        return  None
    check_year = re.search('\d.* ?Year', T.replace('to', '-'), re.IGNORECASE)
    check_month = re.search('\d.* ?Month', T.replace('to', '-'), re.IGNORECASE)
    splitChar = ['-', '|']
    if check_year:
        year = re.sub('[^0-9-]', '', check_year.group(0))
        for splitC in splitChar:
            if splitC in year:
                year = year.split(splitC)[0]
                break
        return int(year) * 12
    elif check_month:
        check_month = re.sub('[^0-9-]', '', check_month.group(0))

        for splitC in splitChar:
            if splitC in check_month:
                check_month = check_month.split(splitC)[0]
                break
        return int(check_month)
    else:
        return None


h3Table = jsoup[1:]
for k in h3Table:
    try:
        data = BeautifulSoup('<h3>'+k)
        bank_product_name = data.find('h3')
        if bank_product_name is not None:
            p = data.find('p')
            Balance = None
            if p is not None:
                Balance = p.find('em').text.replace('\n','').strip() if p.find('em') is not None else None
            table = data.find('table')
            if table is not None:
                thead = table.find('thead')
                dataHeaders = dict()
                headers = ['Term', 'Interest Rate', 'APY','Balance']
                if thead is not None:
                    for id,th in enumerate(thead.find_all('th')):
                        if th.text.strip() in headers:
                            dataHeaders[id] = th.text.strip()

                tbody = table.find('tbody')
                if tbody is not None:
                    trs = tbody.find_all('tr')
                    trigger = None
                    for tr in trs:
                        tds = tr.find_all('td')
                        if tr.find('th') is not None:
                            tds.insert(0, tr.find('th'))
                            trigger = tr.find('th')
                        elif trigger is not None:
                            tds.insert(0, trigger)
                        dataDict = dict()
                        for k in dataHeaders.keys():
                            dataDict[dataHeaders[k]] = re.sub('\s','',tds[k].text.replace('\n','').strip())
                        for d in headers:
                            if d not in dataDict:
                                dataDict[d] = None
                        dataDict['bank_product_name'] = bank_product_name.text.replace('\n','').strip()
                        dataDict['Minimu_Balance'] =   Balance.replace('\r','').strip()
                        Term = TermInMOnths(dataDict['Term'])
                        if 'cd' in dataDict['bank_product_name'].lower():
                            if Term in [6,12]:
                                aa = ['CD',re.sub(r'[^\x00-\x7F]+','', dataDict['bank_product_name']), dataDict['Minimu_Balance'], dataDict['Balance'], Term, dataDict['Interest Rate'], dataDict['APY']]
                                Exceldata.append(aa)
                        else:
                            if 'special' not in dataDict['bank_product_name'].lower():
                                aa = ['Savings', re.sub(r'[^\x00-\x7F]+','', dataDict['bank_product_name']), dataDict['Minimu_Balance'], dataDict['Balance'], Term,dataDict['Interest Rate'], dataDict['APY']]
                                Exceldata.append(aa)
                print('-'.center(100, '-'))
    except Exception as e:
        print(e)

#----------------------------------Checkings----------------------------------------
resp = requests.post('https://www.wellsfargo.com/checking/everyday/',headers = post_headers, data={'zipCodeSelector':'10004'}).content
h1 = BeautifulSoup(resp,'html.parser').find('h1')
if h1 is not None:
    g = ['Checking', h1.text, '', None, None, None,None]
    Exceldata.append(g)

print(tabulate(Exceldata))

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
#Arrange all fileds based on required format
order = ["Date", "Bank_Name", "Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name", "Product_Term", "Balance", "Product_Interest", "Product_Apy", "Mortgage_Down_Payment", "Mortgage_Loan", "Min_Credit_Score_Mortagage", "Mortgage_Apr"]
df = pd.DataFrame(Exceldata[1:],columns=tableHeaders)
df['Minimu_Balance'] = df['Minimu_Balance'].apply(lambda x: re.findall('\$\d.*\d ',x)[0] if len(re.findall('\$\d.*\d ',x))!=0 else None)
df['Balance'] = df['Balance'].apply(lambda x: re.sub('[^0-9-,]','',str(x)).strip('-') if x is not None else None)
df["Date"] = today.strftime("%m-%d-%Y")
df["Bank_Name"] = "WELLS FARGO"
df["Bank_Product"] = "Deposits"
df["Bank_Offer_Feature"] = "Offline"
df["Mortgage_Down_Payment"] = np.NAN
df["Mortgage_Loan"] = np.NAN
df["Min_Credit_Score_Mortagage"] = np.NAN
df["Mortgage_Apr"] = np.NAN
df = df[order]
df.to_csv(path, index=False) #Moving Data to Csv File

print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')

