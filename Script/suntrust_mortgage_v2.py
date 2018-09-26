import requests
import re
from tabulate import tabulate
import pandas as pd
from bs4 import BeautifulSoup
from maks_lib import output_path
import datetime
today = datetime.datetime.now()
path = output_path+'Consolidate_SunTrust_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'
Excel_Data = []
table_headers = ['Bank_Product_Name', 'Product_Term', 'Product_Interest', 'Mortgage_Apr', 'Mortgage_Loan', 'Mortgage_Down_Payment', 'Min_Credit_Score_Mortagage']
# Excel_Data.append(table_headers)
resp = requests.get('https://www.suntrust.com/home-mortgages/current-rates')
jsoup = BeautifulSoup(resp.content)#.find('div', attrs={'class':'suntrust-rowContainer'})
for div in jsoup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['suntrust-mortgagetable']):
    try:
        Bank_Product_Name = div.find('a').text.strip()
        p = div.find_all('p', attrs={'class': 'suntrust-percentageLink'})
        interest = p[0].text
        apr = p[1].text
        Bal = div.find('div', attrs={'class': 'suntrust-textrightRates'})
        Balance = re.search('\$[0-9.,]*',Bal.find('p').text if Bal.find('p') is not None else '') if Bal is not None else None
        if Balance is not  None:
            Balance = Balance.group(0).strip(',')

        credits = re.search('score of [0-9.]*',Bal.text)
        if credits is not None:
            credits = credits.group(0)
        downPayment = re.search('[0-9]*% down',Bal.text)
        if downPayment is not None:
            downPayment = downPayment.group(0)

        Month = re.search('[0-9 ]*year', Bank_Product_Name, re.IGNORECASE)
        Month = int(re.sub('[^0-9]','',Month.group(0))) if Month is not None else None
        a = [Bank_Product_Name, Month, interest, apr, Balance.strip('$').replace(',',''), re.sub('[^0-9%]', '', downPayment)if downPayment is not None else '0%', re.sub('[^0-9]','',credits)if credits is not None else None]
        Excel_Data.append(a)

    except Exception as e:
        print(e)

order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage","Mortgage_Apr"]
df = pd.DataFrame(Excel_Data,columns=table_headers)
df['Date'] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'SUNTRUST BANKS INC'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Offline'
df['Product_Apy'] = None
df['Balance'] = None
df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_Data))