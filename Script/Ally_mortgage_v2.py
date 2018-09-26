import requests
import re
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import datetime
today = datetime.datetime.now()
Excel_Table = []
import time
from maks_lib import output_path
print('Program Exection Started...')
start_time = time.time()

# Csv file path, to store the scraped data.
path = output_path+'Consolidate_ALLY_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'

Excel_Data = []
#Required fields to scrape the data
table_headers = ['Bank_Product_Name', 'Product_Term', 'Balance','Product_Interest', 'Product_Apy', 'Mortgage_Down_Payment', 'Mortgage_Loan', 'Min_Credit_Score_Mortagage', 'Mortgage_Apr']

#Getting page content by using requests module
g = requests.get('https://www.ally.com/home-loans/mortgage/').content #Pass the required scraping url

#Getting data by using BeautifulSoup module
jsoup = BeautifulSoup(g)
Balance = jsoup.find('output', attrs={'class':'loan-amount'})
downPayment = jsoup.find('figure',attrs={'class':'products'})
s = re.search('\d\d% down', downPayment.text, re.IGNORECASE)
downPayment = re.sub('[^0-9.%]', '', s.group(0)) if s is not None else None
Balance = Balance.text if Balance is not None else None
h3 = jsoup.find_all('h4', attrs={'class':'underline clear'})
heading1 = h3[0].text
heading2 = h3[1].text

#Post data to send with the url
data = {"type":"conventional","data":{"loanPurpose":1,"occupancyType":1,"propertyType":1,"subjectPropertyValue":375000,"programTypeIDString":"1,2,3,4,5,9,10,11","loanAmount":300000,"fico":740,"stateAbbreviation":"CA","lockTerm":9}}

#Headers to handle the requests issues
headers = {"Accept":"application/json",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.9",
            "Connection":"keep-alive",
            "Content-Length":"212",
            "Content-Type":"application/json",
            "Host": "www.ally.com",
            "Origin": "https://www.ally.com",
            "Referer": "https://www.ally.com/home-loans/mortgage/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

#Using post method to send the post data to server
resp = requests.post('https://www.ally.com/services/rates/defaultMortgageRates', json = data, headers=headers)

print(resp.json())
#Id's for finding the required data in json Data
codes = [13431, 13432, 13423,13434,13425, 13452,13451,13450]
for program in resp.json()['mortgageRates']['programs']:
    for rate in program['rates']:
        interest = rate['rate']
        APR = rate['apr']
        Year = rate['actualTerm']
        Payment = rate['piPayment']

        if rate['point']<=0:
            print(program['programID'])
            if int(program['programID']) in codes:
                if 'arm' in program['description'].lower():
                    name = heading2+' '+program['description']
                else:
                    name = heading1+' '+program['description']
                if 'arm' in name.lower():
                    name = name[:name.rindex('ARM')+3]
                elif 'fixed' in name.lower():
                    name = name[:name.rindex('Fixed')+5]
                a = [name, Year/12, Payment,str(interest*100)+'%', None, downPayment, Balance, '720+', str(APR*100)+'%']
                Excel_Data.append(a)
                break

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
print(tabulate(Excel_Data))
df = pd.DataFrame(Excel_Data, columns=table_headers)
df['Date'] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'ALLY'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Online'
df['Balance'] = None
#Arrange all fields in required format
order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage","Mortgage_Apr"]
df = df[order]
df.to_csv(path, index=False) #moving data to csv file

print('Total Execution Time is ',time.time()-start_time,'Seconds') #Displaying total execution time.