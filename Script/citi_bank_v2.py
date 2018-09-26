import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import numpy as np
from maks_lib import output_path

headers = ['Bank_Product_Type', 'Bank_Product_Name', 'Balance',   'Product_Interest', 'Product_Apy', 'Product_Term']
tableData = []
today = datetime.datetime.now()

# Colmn names  and mapped vaiables
Date = today.strftime("%m-%d-%Y")
Bank_Name = 'CITIGROUP INC'
Bank_Product = 'Deposits'
Bank_Offer_Feature = 'Offline'
Mortgage_Down_Payment = None
Mortgage_Loan = None
Min_Credit_Score_Mortagage = None
Mortgage_Apr = None
columnsOrder = ["Date", "Bank_Name", "Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name",
                "Product_Term", "Balance", "Product_Interest", "Product_Apy", "Mortgage_Down_Payment", "Mortgage_Loan",
                "Min_Credit_Score_Mortagage", "Mortgage_Apr"]
#Csv File Location
path = output_path + "Consolidate_CITI_Data_Deposit_{}.csv".format(today.strftime("%m_%d_%Y"))

#Load Browser
driver = webdriver.Firefox()
driver.maximize_window()

def getPageSource(url):
    driver.get(url)
    try:
        time.sleep(5)
        driver.find_element_by_class_name("ui-selectmenu-item-header").click()
        driver.find_element_by_id("RegionalPricingLocation-snapshot-menu-option-41").click()
        driver.find_element_by_id("cmlink_GoBtnLocForm").click()
    except:
        pass
    time.sleep(5)
    jsoup = BeautifulSoup(driver.page_source, 'html.parser')
    pageSource = jsoup.find('div', attrs={'id':'main-details'})
    return pageSource

def checkingData(url):
    checking = getPageSource(url)
    df = pd.read_html(str(checking))
    for d in df:
        test = d.values.tolist()[:1][0][0]
        Banktype = ['Checking', test] if 'checking' in test.lower() else ['Savings', test]
        for k in d.values.tolist()[1:]:
            k.insert(0,Banktype[0])
            k.insert(1, Banktype[1])
            tableData.append(k)

def CDRates(url):
    pageSource = getPageSource(url)
    period = ''
    for tboby in pageSource.find('table').find_all('tbody'):
        trs = tboby.find_all('tr')
        if len(trs)==1:
            tds = trs[0].find_all('td')
            if any([True for x in ['year','month'] if x in tds[0].text.lower()]):
                period = tds[0].text
                continue
        for tr in tboby.find_all('tr'):
            temp = [td.text for td in tr.find_all('td')]
            del temp[-1]
            temp.append(period)
            temp.insert(0, 'CD')
            temp.insert(1, period)
            tableData.append(temp)

if __name__ == '__main__':
    checkingData('https://online.citi.com/US/JRS/pands/detail.do?ID=CurrentRates&JFP_TOKEN=7JAPCVIC')
    CDRates('https://online.citi.com/US/JRS/pands/detail.do?ID=CDRates&JFP_TOKEN=0UYWWGSQ')
    print(tableData)
    df = pd.DataFrame(tableData, columns=headers)
    df = df[df['Product_Term'].apply(lambda x: True if x  in [np.nan, '6-Month', '1-Year', '3-Year'] else False)]
    def conMonth(x):
        if isinstance(x,str):
            if 'year' in x.lower():
                try:
                    return int(re.sub('[^0-9]', '',x))*12
                except:
                    return None
            elif 'month' in x.lower():
                return  re.sub('[^0-9]', '', x)
        else:
            return None
    df['Product_Term'] = df['Product_Term'].apply(conMonth)
    df['Date'] = Date
    df['Bank_Name'] = Bank_Name
    df['Bank_Product'] = Bank_Product
    df['Bank_Offer_Feature'] = Bank_Offer_Feature
    df['Mortgage_Down_Payment'] = Mortgage_Down_Payment
    df['Mortgage_Loan'] = Mortgage_Loan
    df['Min_Credit_Score_Mortagage'] = Min_Credit_Score_Mortagage
    df['Mortgage_Apr'] = Mortgage_Apr
    df = df[columnsOrder]
    df.to_csv(path, index=False)
    print(df)

    driver.close()