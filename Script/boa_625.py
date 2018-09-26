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

    def __init__(self, url = 'https://www.bankofamerica.com/mortgage/mortgage-rates/ ',Pur_pri='625,000', zipcode='10004',
                 down_pay = '125,000'):
        self.zipcode = zipcode
        self.down_pay = down_pay
        self.Pur_pri = Pur_pri
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        sleep(3)
        # write log in function



    def log_in(self):
        cust_rate = self.driver.find_element_by_xpath('//*[@id="change-mortgage-rates-medium"]')
        cust_rate.click()
        purchase = self.driver.find_element_by_xpath('//*[@id="purchase-price-input-medium"]')
        purchase.send_keys(self.Pur_pri)
        down = self.driver.find_element_by_xpath('//*[@id="down-payment-input-medium"]')
        down.send_keys(self.down_pay)
        zip_input = self.driver.find_element_by_xpath('//*[@id="zip-code-input-medium"]')
        zip_input.send_keys(self.zipcode)
        update = self.driver.find_element_by_xpath('//*[@id="update-button-medium"]')
        update.click()
        return self.Pur_pri, self.zipcode


    def data(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML")
        soup = bs(html, 'lxml')
        loan = soup.find('strong',attrs={'class':'partial-price'})
        loan = loan.getText()
        pd = soup.find_all('div', attrs={'class':'medium-3 columns'})
        A = []
        B = []
        C = []
        D = []
        E = ["30", "", "15", "", "30", "30"]
        for data in (pd[2]):
            d1 = data.find_all('p')
            for i in d1:
                A.append(i.getText().rstrip(' layer \xa0'))
        for data in (pd[4]):
            d1 = data.find_all('p')
            for i in d1:
                A.append(i.getText().rstrip(' layer \xa0'))
        for data in (pd[6]):
            d1 = data.find_all('p')
            for i in d1:
                A.append(i.getText().rstrip(' layer \xa0'))
        for data in (pd[8]):
            d1 = data.find_all('p')
            for i in d1:
                A.append(i.getText().rstrip(' layer variable'))
        for data in (pd[10]):
            d1 = data.find_all('p')
            for i in d1:
                A.append(i.getText().rstrip(' layer variable'))
        for data in (pd[12]):
            d1 = data.find_all('p')
            for i in d1:
                A.append(i.getText().rstrip(' layer variable'))
        pd2 = soup.find_all('div', attrs={'class': 'medium-2 columns'})
        for data in (pd2[3]):
            d1 = data.find_all('p')
            for i in d1:
                B.append(i.getText().lstrip("Rate "))
        for data in (pd2[4]):
            d1 = data.find_all('p')
            for i in d1:
                C.append(i.getText().lstrip("APR "))
        for data in (pd2[5]):
            d1 = data.find_all('p')
            for i in d1:
                D.append(i.getText().lstrip("Points "))
        for data in (pd2[6]):
            d1 = data.find_all('p')
            for i in d1:
                B.append(i.getText().lstrip("Rate "))
        for data in (pd2[7]):
            d1 = data.find_all('p')
            for i in d1:
                C.append(i.getText().lstrip("APR "))
        for data in (pd2[8]):
            d1 = data.find_all('p')
            for i in d1:
                D.append(i.getText().lstrip("Points "))
        for data in (pd2[9]):
            d1 = data.find_all('p')
            for i in d1:
                B.append(i.getText().lstrip("Rate "))
        for data in (pd2[10]):
            d1 = data.find_all('p')
            for i in d1:
                C.append(i.getText().lstrip("APR "))
        for data in (pd2[11]):
            d1 = data.find_all('p')
            for i in d1:
                D.append(i.getText().lstrip("Points "))
        for data in (pd2[12]):
            d1 = data.find_all('p')
            for i in d1:
                B.append(i.getText().lstrip("Rate "))
        for data in (pd2[13]):
            d1 = data.find_all('p')
            for i in d1:
                C.append(i.getText().lstrip("APR "))
        for data in (pd2[14]):
            d1 = data.find_all('p')
            for i in d1:
                D.append(i.getText().lstrip("Points "))
        for data in (pd2[15]):
            d1 = data.find_all('p')
            for i in d1:
                B.append(i.getText().lstrip("Rate "))
        for data in (pd2[16]):
            d1 = data.find_all('p')
            for i in d1:
                C.append(i.getText().lstrip("APR "))
        for data in (pd2[17]):
            d1 = data.find_all('p')
            for i in d1:
                D.append(i.getText().lstrip("Points "))
        for data in (pd2[18]):
            d1 = data.find_all('p')
            for i in d1:
                B.append(i.getText().lstrip("Rate "))
        for data in (pd2[19]):
            d1 = data.find_all('p')
            for i in d1:
                C.append(i.getText().lstrip("APR "))
        for data in (pd2[20]):
            d1 = data.find_all('p')
            for i in d1:
                D.append(i.getText().lstrip("Points "))
        return A, B, C, D, E, loan

    def browser_close(self):
        self.driver.close()

if __name__ == '__main__':
    app = App()
    price, zipcode = app.log_in()
    sleep(10)
    A, B, C, D, E, loan  = app.data()
    app.browser_close()
    df = pd.DataFrame({'Date':now.strftime("%m/%d/%Y"),"Bank Name":'Bank Of America','Purchase price':price,
                       "Loan Amount":loan,"Zipcode":zipcode,"Product Name":A,"Rate":B,"APR":C,"Points":D,"Credit Score":"740","Product term":E,"Payment Type":"principal + interest"})
    df = df.reindex(columns=['Date',"Bank Name","Purchase price",
                       "Loan Amount","Zipcode","Product Name","Rate","APR","Points","Credit Score","Product term","Payment Type"])
    df.to_csv(output_path + "BOA_Data_Mortgage_625.csv".format(now.strftime("%m_%d_%Y")), index=False)

df1 = pd.read_csv(output_path+"BOA_Data_Mortgage1.csv")
df2 = pd.read_csv(output_path+"BOA_Data_Mortgage_375.csv")
df3 = pd.read_csv(output_path+"BOA_Data_Mortgage_625.csv")
df_new = pd.concat([df1, df2, df3])

#######################################################################################################################
df2 = df_new[df_new.index != 13]
df2 = df2.iloc[0:14,:]
df1 = df_new.iloc[15:19,:]
df = pd.concat([df2,df1])
df["Date"] = now.strftime("%m-%d-%Y")
df["Bank_Name"] = "BANK OF AMERICA CORP"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Bank_Product_Name"] = df["Product Name"]
df["Product_Term"] = df["Product term"]
df["Balance"] = np.NAN
df["Product_Interest"] = df["Rate"]
df["Product_Apy"] = np.NAN
df["Mortgage_Down_Payment"] = "20%"
df["Mortgage_Loan"] = df["Loan Amount"]
df["Min_Credit_Score_Mortagage"] = df["Credit Score"]
df["Mortgage_Apr"] = df["APR"]
#df_new.columns = ["Date","Bank_Name","Purchase price","Mortgage_Loan","Zipcode","","Product_Interest","Mortgage_Apr","Points","Min_Credit_Score_Mortagage","Payment Type","Bank_Product_Type","Bank_Offer_Feature", "Bank_Product", "Product_Term", "Balance" ,"Product_Apy" ,"Mortgage_Down_Payment"]
df = df.reindex(columns=["Date", "Bank_Name","Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name", "Product_Term", "Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage", "Mortgage_Apr"])
df = df[df.index != 15]
df.to_csv(output_path + "Consolidate_BOA_Data_Mortgage{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
