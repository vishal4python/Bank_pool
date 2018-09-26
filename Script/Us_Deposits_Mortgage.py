import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import pandas as pd
from maks_lib import output_path
import datetime
import time

print('Program Execution Started...')
start_time = time.time()
Excel_Table =[]
today = datetime.datetime.now()

#CSV File Location
path = output_path + "Aggregator_US_Deposit_Data_Mortgage_"+today.strftime("%m_%d_%Y")+".csv"

#Filter Banks names based on needeBanks
neededUsBanks = {
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

#Required Fields for scraping the data
table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest', 'APR', 'Mortgage_Loan_Amt']
Excel_Table.append(table_headers)


headers = {"Accept": "text/html, */*; q=0.01",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9",
"Connection": "keep-alive",
"Host": "us.deposits.org",
"Referer": "https://us.deposits.org/loans/",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"}
urlList =["https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=10%20year%20fixed",
          "https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=15%20year%20fixed",
          "https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=20%20year%20fixed",
          "https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=30%20year%20fixed",
          "https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=va",
          "https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=5%2F1%20arm",
          "https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=7%2F1%20arm",
          "https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=fha,"
          "https://us.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=jumbo"]
for url in urlList:
    # Getting pageSource by Sending url through requests module in python
    resp = requests.get(url, headers=headers).content

    # Getting required fields data by using python BeautifulSoup Module.
    trs = BeautifulSoup(resp).find('div', attrs={'class':'reload_tabs'}).find('table').find('tbody').find_all('tr')
    for tr in trs:
        td = tr.find_all('td')
        Bank_Name = td[0].find('a', attrs={'class':'title'}).text
        Bank_Product_Name = td[1].find('a', attrs={'class': 'title'}).text
        Interest = td[2].find('span', attrs={'class':'details'}).text
        td[2].find('span').extract()
        APR = td[2].text
        Term = td[3].text
        check = Term
        Interest_Type = 'Fixed' if 'fixed' in Term.lower() else 'Variable'

        check_year = re.search('(\d.* Year|\d\d.*-Year)', Bank_Product_Name.replace('to', '-'), re.IGNORECASE)

        if check_year:
            splitChar = ['-', '|']
            year = re.sub('[^0-9-]', '', check_year.group(0))
            for splitC in splitChar:
                if splitC in year:
                    Term = year.split(splitC)[0]
                    break
                else:
                    Term = year
        else:
            Term = 30

        for bank in neededUsBanks.keys():
            if bank.lower() in Bank_Name.lower():
                a = [neededUsBanks[bank], Bank_Product_Name, None, 'Offline', Term, Interest_Type, Interest, APR, None]
                Excel_Table.append(a)
                break
print(tabulate(Excel_Table))

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
df = pd.DataFrame(Excel_Table[1:], columns=table_headers)
df["Date"] = ' '+today.strftime('%Y-%m-%d')
df["Bank_Native_Country"] = "US"
df["State"] = "New York"
df["Bank_Local_Currency"] = "USD"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = None
df['Source'] = 'us.deposits.org'

df['Mortgage_Down_Payment'] = '20%'
df['APR'] = df['APR'].apply(lambda x:re.sub('[^0-9%-.]','',str(x)))
#Arrange all fileds based on required format
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APR", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Source"]
df = df[order]
df.to_csv(path, index=False) #Moving Data to CSV File.


print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')
