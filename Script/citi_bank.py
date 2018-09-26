from selenium import webdriver
from bs4 import  BeautifulSoup as bs
import pandas as pd
import time
import os
import sys
import warnings
import datetime
import time
starttime = time.time()
import logging as log
from maks_lib import logpath,output_path,input_path
from maks_lib import log_config
from maks_lib import output_path
import numpy as np

now = datetime.datetime.now()

warnings.simplefilter(action='ignore')


class Citi_bank:
    def __init__(self, url, tab):
        self.url = url
        self.tab = tab

    def start_driver(self):
        self.driver = webdriver.Firefox()

    def close_driver(self):
        return self.driver.close()

    def get_url(self):
        self.driver.get(self.url)

    def select_state(self):
        self.driver.maximize_window()
        time.sleep(6)
        click1 = self.driver.find_element_by_class_name("ui-selectmenu-item-header")
        click1.click()
        time.sleep(1)
        click2 = self.driver.find_element_by_id("RegionalPricingLocation-snapshot-menu-option-41")
        click2.click()
        time.sleep(1)
        select_btn = self.driver.find_element_by_id("cmlink_GoBtnLocForm")
        select_btn.click()
        time.sleep(2)
        return "AA"

    def get_current_url(self):
        return self.driver.current_url

    def save_page(self):
        # pyautogui.hotkey('ctrl', 's')
        # time.sleep(1)
        # pyautogui.typewrite("citi")
        # time.sleep(1)
        # pyautogui.hotkey('enter')
        page = self.driver.page_source
        with open("citi_"+self.tab+".html", 'w')as file:
            file.write(page)

    def unhide(self):
        pass
        # time.sleep(3)
        # unhind = self.driver.find_element_by_xpath('//*[@class = "open"]')
        # unhind.click()

class ExtractInfo(Citi_bank):
    def __init__(self, page,tab):
        self.page = page
        self.tab = tab

    def findtables_tab1(self):
        soup = bs(self.page, "lxml")
        data = []
        for tr in soup.find_all('tr', {"class": self.tab}):
            tds = tr.find_all('td')
            row = [elem.text.strip() for elem in tds]
            data.append(row)
        df = pd.DataFrame.from_records(data[1:])
        temp = df.iloc[5:12,3:5].copy(deep = True)
        try:

            df.drop(df.columns[[3, 4, 5]], axis=1, inplace=True)
        except Exception as e:
            print(e)

        df_0 = df[1:4]
        df_0["Product Name"] = df.iloc[0, 0].replace("Footnote 1", "")
        df_0["Product Type"] = "Checking"
        df_1 = df.iloc[5:12]
        df_1[df_1.columns[1]] = temp[temp.columns[0]]
        df_1[df_1.columns[2]] = temp[temp.columns[1]]
        df_1["Product Name"] = df.iloc[4, 0]
        df_1["Product Type"] = "Savings"
        df_2 = df.iloc[13:20]
        df_2["Product Name"] = df.iloc[12, 0]
        df_2["Product Type"] = "Savings"
        df_3 = df.iloc[21:28]
        df_3["Product Name"] = df.iloc[20, 0]
        df_3["Product Type"] = "Savings"
        df = pd.concat([df_0, df_1, df_2, df_3])
        df.columns = ['Balance', 'APY', 'Interest Rate','Product Name', "Product Type"]
        df["Date"] = now.strftime("%m-%d-%Y")
        df["Bank Name"] = "CITIGROUP INC"
        df["Bank_Product"] = "Deposits"

        dff = df.reindex(columns= ["Date","Bank Name","Product Type",'Bank_Product','Product Name','Balance', 'Interest Rate', 'APY'])
        return dff
        #dff.to_csv(output_path+"CITI_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index =False)

    def findtables_tab2(self):
        soup = bs(self.page, "lxml")
        data = []
        for tr in soup.find_all('tr', {"class": self.tab}):
            tds = tr.find_all('td')

            row = [elem.text.strip() for elem in tds]
            data.append(row)
        df = pd.DataFrame.from_records(data)
        df.drop(df.columns[3], axis=1, inplace=True)
        df.drop(df.index[8:24], inplace=True)
        df.drop(df.index[16:48], inplace=True)
        df.drop(df.index[24:40], inplace=True)
        df.drop(df.index[32:40], inplace=True)
        df.drop(df.index[40:], inplace=True)
        df0 = df[1:8];df0["Tenor"] = "3";df0['Product Name']="3 months"
        df1 = df[9:16];df1["Tenor"] = "6";df1['Product Name']="6 months"
        df2 = df[17:24];df2["Tenor"] = "12";df2['Product Name']="1 year"
        df3 = df[25:32];df3["Tenor"] = "24";df3['Product Name']="2 years"
        df4 = df[33:40];df4["Tenor"] = "36";df4['Product Name']="3 years"

        # df0 =  pd.DataFrame(df0.str.split('-', 1).tolist(), columns=['Minimum Balance', 'Maximum Balance'])
        dfn = pd.concat([df0, df1, df2, df3, df4])
        dfn.columns = ['Balance', 'APY', 'Interest Rate', 'Tenor',
                       'Product Name']

        dfn["Date"] = now.strftime("%m-%d-%Y")
        dfn["Bank Name"] = "CITIGROUP INC"
        dfn["Bank_Product"] = "Deposits"
        dfn["Product Type"] = "CD"
        df_fin = dfn.reindex(
            columns=["Date", "Bank Name","Product Type",'Bank_Product',
                     'Product Name', 'Balance', 'Interest Rate', "APY",
                     "Tenor"])
        # df_final = pd.concat([self.dff, df_fin])
        # df_final.to_csv(output_path + "CITI_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
        return df_fin

class MergeCsv:
    def __init__(self, csv1, csv2 ):
        self.csv1 = csv1
        self.csv2 = csv2
    def concatenate(self):
        pass


if __name__ == "__main__":

    print("Starting scrapping...")
    tab1_url = "https://online.citi.com/US/JRS/pands/detail.do?ID=CurrentRates&JFP_TOKEN=7JAPCVIC"
    tab2_url = "https://online.citi.com/US/JRS/pands/detail.do?ID=CDRates&JFP_TOKEN=0UYWWGSQ"
    urls = [tab1_url, tab2_url]
    tabs = ["tab1", "tab2"]
    for number in range(len(urls)):
        obj = Citi_bank(urls[number], tabs[number])
        obj.start_driver()
        obj.get_url()
        state = obj.select_state()
        obj.save_page()
        obj.close_driver()
        time.sleep(5)
    for scrab in range(len(tabs)):
        page = open("citi_"+tabs[scrab]+".html",'r')
        if tabs[scrab] == "tab1":
            tab1 = ['header', 'switch', 'CPrates']
            extract = ExtractInfo(page, tab1)
            t1 = extract.findtables_tab1()
        else:
            tab2 = ['header','switch']
            extract = ExtractInfo(page, tab2)
            t2 = extract.findtables_tab2()
        page.close()
    df_final = pd.concat([t1,t2])
    df_final["Bank_Offer_Feature"] = "Offline"
    df_final["Mortgage_Down_Payment"] = np.NaN
    df_final["Mortgage_Loan"] = np.NaN
    df_final["Min_Credit_Score_Mortagage"] = np.NaN
    df_final["Mortgage_Apr"] = np.NaN

    df_final.rename(columns={'Date':'Date','Bank Name':'Bank_Name','Product Type':'Bank_Product_Type','Product Name':'Bank_Product_Name','Balance':'Balance',
                        'Interest Rate':'Product_Interest','APY':'Product_Apy','Tenor':'Product_Term','Bank_Product':"Bank_Product"},inplace=True)

    dff= df_final.reindex(columns=['Date','Bank_Name',"Bank_Product",'Bank_Product_Type','Bank_Offer_Feature','Bank_Product_Name','Product_Term','Balance','Product_Interest',
                        'Product_Apy','Mortgage_Down_Payment','Mortgage_Loan','Min_Credit_Score_Mortagage','Mortgage_Apr'])

    dff.to_csv(output_path + "Consolidate_CITI_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
    os.remove("citi_tab1.html")
    time.sleep(2)
    os.remove("citi_tab2.html")
    print("Finished scrapping!!!")

    print('time=',(time.time()-starttime))