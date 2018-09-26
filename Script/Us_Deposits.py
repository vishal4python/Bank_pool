import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import datetime
import time
from maks_lib import output_path

today = datetime.datetime.now()

#Csv file Location
path = output_path + "Aggregator_Us_Deposit_Data_Deposit_"+today.strftime("%m_%d_%Y")+".csv"
# path = 'mybanktracker_Data_US_Deposit_'+today.strftime('%m-%d-%Y')+'.csv'
import re


print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()
Excel_Table = []

#Required Fields for scraping the data
table_headers = ['Bank_Name', 'Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term_in_Months', 'Interest', 'APY']
# Excel_Table.append(table_headers)


#Filternig Required Bank Names by using neededUsBanks
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

#Making Bank_Offer_Feature Online or Offline based on online_banks
online_bank = [k.lower() for k in ['Synchrony Bank', 'Ally Bank', 'Capital One 360']]

# resp = requests.get('https://uk.deposits.org/savings-accounts/').content
urlList = [['Savings','https://us.deposits.org/savings-accounts/'], ['CD','https://us.deposits.org/deposits/']]
for url in urlList:
    resp = requests.get(url[1]).content
    # print(resp)
    trs = BeautifulSoup(resp).find('div', attrs={'class':'reload_tabs'}).find('table').find('tbody').find_all('tr')

    for tr in trs:
        # print(tr)
        td = tr.find_all('td')
        Bank_Name = td[0].find('a', attrs={'class':'title'}).text
        Bank_Product_Name = td[1].find('a', attrs={'class':'title'}).text
        Balance = td[1].find('span')
        if Balance is not  None:
            Balance = Balance.text
            if re.search('minimum.*\d', Balance, re.IGNORECASE) is not  None:
                ab = re.search('minimum.*\d', Balance, re.IGNORECASE)
                # print(re.split('\s',ab.group(0)))
                for k in re.split('\s',ab.group(0)):
                    if re.search('\$\d.*\d',k) is not None:
                        Balance = k
                        break
                    else:
                        Balance = None
            else:
                Balance = None
        else:
            Balance = None
        Interest = td[2].find('span', attrs={'class':'details'}).text

        check_year = re.search('\d.* Year', Bank_Product_Name.replace('to', '-'), re.IGNORECASE)
        check_month = re.search('\d.* Month', Bank_Product_Name.replace('to', '-'), re.IGNORECASE)
        splitChar = ['-', '|']
        if check_year:
            year = re.sub('[^0-9-]', '', check_year.group(0))
            for splitC in splitChar:
                if splitC in year:
                    year = year.split(splitC)[0]
                    break
            Term_in_Months = int(year) * 12
        elif check_month:
            check_month = re.sub('[^0-9-]', '', check_month.group(0))

            for splitC in splitChar:
                if splitC in check_month:
                    check_month = check_month.split(splitC)[0]
                    break
            Term_in_Months = int(check_month)
        else:
            Term_in_Months = None
        Bank_Name = Bank_Name.replace(url[0], '').strip()
        if Bank_Name in neededUsBanks:

            a = [neededUsBanks[Bank_Name], url[0], Bank_Product_Name, Balance, "Online" if Bank_Name.lower() in online_bank else 'Offline', Term_in_Months,Interest, None]
            Excel_Table.append(a)


#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Product_Code'] = None
df['Interest_Type'] = 'Fixed'
df['Source'] = 'us.deposits.org'
df['Balance'] = df['Balance'].apply(lambda x:re.sub('[^0-9,]','',str(x)) if len(re.sub('[^0-9,]','',str(x)))!=0 else None)


#Arrange all fileds based on required format
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term_in_Months", "Interest_Type", "Interest", "APY", "Source"]
df = df[order]
df.to_csv(path, index=False)         #Moving data to CSV File.
print(tabulate(Excel_Table))


print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')