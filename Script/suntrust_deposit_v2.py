import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import  tabulate
from maks_lib import output_path
import datetime
import time

print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()

#CSV File Location
path = output_path+'Consolidate_SunTrust_Data_Deposit_'+today.strftime('%m_%d_%Y')+'.csv'

#Required Fields for scraping the data
table_headers = ['Bank_Product_Type', 'Bank_Product_Name', 'Product_Term', 'Balance', 'Product_Interest', 'Product_Apy']
Excel_Data = []
Excel_Data.append(table_headers)

#=============================select-savings====================================
resp = requests.get('https://www.suntrust.com/personal-banking/savings-accounts/select-savings')
jsoup = BeautifulSoup(resp.content).find('div', attrs={'class':'dcm-top-border'}).text
sa = re.search('The interest rate.*[0-9.]*%',jsoup,re.IGNORECASE)
if sa is not None:
    sa = re.search('[0-9.]*%',sa.group(0),re.IGNORECASE)
    interest = sa.group(0)
else:
    balance = None
balance = re.search('daily collected balance of \$[0-9,.]* ',jsoup,re.IGNORECASE)

if balance is not None:
    balance = re.search('\$[0-9,.]*', balance.group(0), re.IGNORECASE)
    balance = balance.group(0)
else:
    balance = None
if interest is not None:
    a = ['Savings', 'Select Savings', None, balance, interest, interest]
    Excel_Data.append(a)
#===================================MM select savings=============================================

mm_sc = requests.get('https://www.suntrust.com/personal-banking/savings-accounts/signature-money-market-savings')
mm_sc_jsoup = BeautifulSoup(mm_sc.content).find('div', attrs={'class':'dcm-top-border'}).text
lis = re.search('Tier \d.*more.',mm_sc_jsoup, re.IGNORECASE)
if lis is not  None:
    for k in lis.group(0).split(';'):
        k = re.search('(\$\d.*\d or less|\$\d.*\d or more|\$\d.*\d|\$\d.* or more)', k)
        if k is not None:
            a = ['Savings', 'Select Savings', None, k.group(0), None, None]
            Excel_Data.append(a)
#=========================================Balanced Banking Essential Checking=====================

BE = requests.get('https://www.suntrust.com/personal-banking/checking')
try:
    BEjsoup = BeautifulSoup(BE.content).find('strong', text='How to avoid Monthly Maintenance Fees').parent.parent
    betds = BEjsoup.find_all('td')
    balanced_banking = betds[0].text
    balanced_banking = re.search('\$[0-9,\.]* minimum daily',balanced_banking)
    if balanced_banking is not None:
        balanced_banking = re.search('\$[0-9,\.]*',balanced_banking.group(0))
        Excel_Data.append(['Savings', 'Balanced Banking', None, balanced_banking.group(0), None, None])
    essentialChecking = betds[1].text
    essentialChecking = re.search('\$[0-9,\.]* minimum daily', essentialChecking)
    if essentialChecking is not None:
        essentialChecking = re.search('\$[0-9,\.]*', essentialChecking.group(0))
        Excel_Data.append(['Checking', 'Essential Checking', None, essentialChecking.group(0), None, None])

except Exception as e:
    print(e)
#==================================Select Checking=================================================
sc = requests.get('https://www.suntrust.com/personal-banking/checking/select-checking')
jsoup = BeautifulSoup(sc.content).find('div', attrs={'class':'dcm-top-border'})
if jsoup is not None:
    jsoup = jsoup.text
    APY = re.search('APY.*[0-9\.]*%', jsoup, re.IGNORECASE)
    if APY is not None:
        APY = re.search('[0-9\.]*%', jsoup, re.IGNORECASE)
    else:
        APY = None
    if APY is not None:
        lis = re.search('Tier \d.*more.',jsoup, re.IGNORECASE)
        if lis is not None:
            for k in lis.group(0).split(';'):
                k = re.search('(\$\d.*\d or less|\$\d.*\d or more|\$\d.*\d)',k)
                if k is not None:
                    a = ['Checking', 'Select Checking', None, k.group(0), None, APY.group(0)]
                    Excel_Data.append(a)

print(tabulate(Excel_Data))

#====================================signature-advantage-checking============================
sac = requests.get('https://www.suntrust.com/personal-banking/checking/signature-advantage-checking')
jsoup = BeautifulSoup(sac.content).find('div', attrs={'class':'dcm-top-border'})
if jsoup is not None:
    sac_text = jsoup.text.split('Signature Advantage Brokerage:')
    for t_text in sac_text:
        dummyDict = dict()
        sac_lis = re.search('Tier \d.*;', t_text+';', re.IGNORECASE)
        if sac_lis is not None:
            for id , k in enumerate(sac_lis.group(0).split(';')):
                k = re.search('(\$\d.*\d or less|\$\d.*\d or more|\$\d.*\d)', k)
                if k is not None:
                    dummyDict[id+1] = [k.group(0)]
        if 'follows:' in t_text:
            t_text = t_text[t_text.index('follows:'):]
            for t in  t_text.split(';'):
                t =re.sub('[^0-9a-z\.%–-]','',t.lower())
                sac_apy = re.search('(Tier\d.*%|Tiers\d.*%)', t, re.IGNORECASE)

                if sac_apy is not None:
                    res = sac_apy.group(0)
                    if 'tiers' in res:
                        ress = re.search('\d-\d',res).group(0).split('-')
                        for i in range(int(ress[0]),int(ress[1])+1):
                            dummyDict[i] = dummyDict[i]+[re.search('\d\.[0-9]*%',res).group(0)]
                            Excel_Data.append(['Savings', 'Signature Advantage Brokerage', None, dummyDict[i][0], None, dummyDict[i][1]])
                    else:
                        it = int(re.sub('[^0-9]','',re.search('(Tier\d\d?)', t, re.IGNORECASE).group(0)))
                        dummyDict[it] = dummyDict[it]+[re.search('\d\..*%', t, re.IGNORECASE).group(0)]
                        Excel_Data.append(['Savings', 'Signature Advantage Brokerage', None, dummyDict[it][0], None, dummyDict[it][1]])

                else:
                    print('None')
        else:
            sac_apy = re.search('APY.*\d\.[0-9]*%', t_text, re.IGNORECASE)
            if sac_apy is not  None:
                apy = re.search('\d\.[0-9]*%', t_text, re.IGNORECASE).group(0)
                for i in dummyDict.keys():
                    dummyDict[i] = dummyDict[i]+[apy]
                    Excel_Data.append(['Checking', 'Signature Advantage Checking', None, dummyDict[i][0], None, dummyDict[i][1]])
            else:
                for i in dummyDict.keys():
                    dummyDict[i] = dummyDict[i]+[None]
                    Excel_Data.append(['Checking', 'Signature Advantage Checking', None, dummyDict[i][0], None, dummyDict[i][1]])

print(tabulate(Excel_Data))

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
df = pd.DataFrame(Excel_Data[1:], columns=table_headers)
#Arrange all fileds based on required format
order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage","Mortgage_Apr"]
df['Date'] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'SUNTRUST BANKS INC'
df['Bank_Product'] = 'Deposits'
df['Bank_Offer_Feature'] = 'Offline'
df['Mortgage_Down_Payment'] = None
df['Mortgage_Loan'] = None
df['Min_Credit_Score_Mortagage'] = None
df['Mortgage_Apr'] = None
df = df[order]
df.to_csv(path, index=False) #Moving Data to Csv File.


print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')