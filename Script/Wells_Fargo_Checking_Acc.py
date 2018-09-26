# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
from maks_lib import output_path
import datetime
import numpy as np

now = datetime.datetime.now()

class App:

    def __init__(self, url='https://www.wellsfargo.com/checking/everyday/ ', zipcode='10004'):
        self.zipcode = zipcode
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        sleep(3)
        # write log in function
        self.log_in()
        sleep(5)


    def log_in(self):
        zip_input = self.driver.find_element_by_xpath('//*[@id="zipCode"]')
        zip_input.send_keys(self.zipcode)
        continue_button = self.driver.find_element_by_xpath('//*[@id="c28lastFocusable"]')
        continue_button.click()

    def data_page(self):
        page = self.driver.page_source
        soup = bs(page, 'lxml')
        product_name = soup.find('h1', attrs={'class':'c11'})
        product_name = product_name.getText()
        return product_name

    def browser_close(self):
        self.driver.close()

if __name__ == '__main__':
    app = App()
    product_name = app.data_page()
    app.browser_close()
    data = [(now.strftime("%m/%d/%Y"), "Wells Fargo", product_name)]
    df4 = pd.DataFrame.from_records(data, columns=["Date", "Bank Name", "Product Name"])
    df4.to_csv(output_path + "WellsF_Data_Checking_Acc.csv".format(now.strftime("%m_%d_%Y")), index=False)

##########################################################################################################################
df4["Date"] = now.strftime("%m-%d-%Y")
df4["Bank_Name"]="WELLS FARGO"
df4["Bank_Product"]= "Deposits"
df4["Bank_Product_Type"] = "Checking"
df4["Bank_Offer_Feature"] = "Offline"
df4["Bank_Product_Name"] = df4["Product Name"]
df4["Product_Term"] = np.NAN
df4["Balance"] = np.NAN
df4["Product_Interest"] = np.NAN
df4["Product_Apy"] = np.NAN
df4["Mortgage_Down_Payment"] = np.NAN
df4["Mortgage_Loan"] = np.NAN
df4["Min_Credit_Score_Mortagage"] = np.NAN
df4["Mortgage_Apr"] = np.NAN
df4 = df4.reindex(columns=["Date", "Bank_Name","Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name", "Product_Term", "Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage", "Mortgage_Apr"])
df4.to_csv(output_path +"Consolidate_WellsF_Data_Checking_Acc{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
