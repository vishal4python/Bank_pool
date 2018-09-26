from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import warnings
import numpy as np
from maks_lib import output_path
warnings.simplefilter(action='ignore')

now = datetime.datetime.now()

class App:

    def __init__(self, url = 'https://www.synchronybank.com/banking/high-yield-savings/ '):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        sleep(5)
        self.data_page()



    def data_page(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML")
        soup = bs(html, 'html.parser')
        li = soup.find_all('li')
        min_open = li[29].getText()
        Pd = soup.find_all('h2', attrs={'class':'heading-level-1'})
        Pd = Pd[1].getText()
        li = soup.find_all('span',attrs={'id':['mmaLowApy','mmaMidApy','mmaHighApy']})
        Apy_li=[]
        for apy in li:
            if apy.getText() is not None:
                Apy_li.append(apy.getText().rstrip("APY*"))

        bal = soup.find_all('div', attrs={'class':'deposit-range'})
        bal_li = []
        for brange in bal:
            if brange.getText() is not None:
                bal_li.append(brange.getText())
        # print(li[32].getText())
        # print(li[33].getText())
        return  Apy_li, Pd, bal_li, min_open

    def browser_close(self):
        self.driver.close()


if __name__ == '__main__':
    app = App()
    Apy_li, Pd, bal_li, min_open = app.data_page()
    app.browser_close()
    df = pd.DataFrame({'Date':now.strftime("%m/%d/%Y"),"Bank Name":'Synchrony','Product Name':Pd,
                       "Minimum Open Balance":min_open,"Deposite":bal_li,"APY":Apy_li})
    df = df.reindex(
        columns=["Date", "Bank Name", "Product Name", "Minimum Open Balance","Deposite", "APY"])
    df.to_csv(output_path +"Sync_Data_Deposit_High_Yield.csv".format(now.strftime("%m_%d_%Y")), index=False)

    df1 = pd.read_csv(output_path+"Sync_Data_Deposit.csv")
    df2 = pd.read_csv(output_path+"Sync_Data_Make_Money.csv")
    df3 = pd.read_csv(output_path+"Sync_Data_Deposit_High_Yield.csv")
    df3 = pd.concat([df1, df2, df3])
#####################################################################################################################
    df3["Date"] = now.strftime("%m-%d-%Y")
    df3["Bank_Name"]="SYNCHRONY"
    df3["Bank_Product"]= "Deposits"
    df3["Bank_Product_Type"] = df3["Product Name"].str.strip("_3 _6 _9 _12 _18 _24 _36 _48 _60 -month Money Market Rates and Terms HYS Rates and Terms")
    df3["Bank_Offer_Feature"] = "Online"
    df3["Bank_Product_Name"] = df3["Product Name"]
    df3["Product_Term"] = df3["Product Name"].str.strip("CD_ -month Money Market Rates and Terms HYS Rates and Terms")
    df3["Balance"] = df3["Deposite"]
    df3["Product_Interest"] = np.NAN
    df3["Product_Apy"] = df3["APY"]
    df3["Mortgage_Down_Payment"] = np.NAN
    df3["Mortgage_Loan"] = np.NAN
    df3["Min_Credit_Score_Mortagage"] = np.NAN
    df3["Mortgage_Apr"] = np.NAN
    df3 = df3.reindex(columns=["Date", "Bank_Name","Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name", "Product_Term", "Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage", "Mortgage_Apr"])
    df3.loc[9:15]['Bank_Product_Type']='Savings'
    df3.to_csv(output_path +"Consolidate_Sync_Data_Deposit{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
