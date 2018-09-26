from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import output_path

warnings.simplefilter(action='ignore')

now = datetime.datetime.now()


class App:

    def __init__(self, url='https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/VA-Loan.html',
                 loan_amount=500000, zipcode='10004'):
        self.zipcode = zipcode
        self.loan_amount = loan_amount
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        sleep(3)
        # write log in function

    def log_in(self):
        purchase = self.driver.find_element_by_xpath('//*[@id="purchaseType"]/option[1]')
        purchase.click()
        loan_amount = self.driver.find_element_by_xpath('//*[@id="purchaseAmount"]')
        loan_amount.send_keys(self.loan_amount)
        zip_code = self.driver.find_element_by_xpath('// *[ @ id = "zipCode"]')
        zip_code.send_keys(self.zipcode)
        getrate_button = self.driver.find_element_by_xpath('//*[@id="ratesGet"]')
        getrate_button.click()
        return self.loan_amount, self.zipcode

    def data_page(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML")
        soup = bs(html, 'html.parser')
        pro_name = soup.find_all('div', attrs={'div', 'columnHeader grid-19 tablet-grid-20 mobile-grid-19'})
        Int_rate = soup.find_all('div', attrs={'div', 'rowItem grid-19 tablet-grid-20 mobile-grid-19 bigPrint'})
        product = []
        int_rate = []
        Term = []
        for pro in pro_name:
            if pro.getText() is not None:
                # print(pro.getText())
                product.append(pro.getText().rstrip("\xa0"))
        Term = ["30", "30", "30", ""]
        # for pro in pro_name:
        #     if pro.getText() is not None:
        #         # print(pro.getText())
        #         Term.append(pro.getText().rstrip(" Fixed \xa0 "))
        for int_r in Int_rate:
            int_rate.append(int_r.getText())

        return product, int_rate, Term

    def browser_close(self):
        self.driver.close()


if __name__ == '__main__':
    app = App()
    price, zipcode = app.log_in()
    sleep(5)
    product, int_rate, Term = app.data_page()
    Int_rate = int_rate[0:4]
    Apy_rate = int_rate[4:8]
    app.browser_close()

    data = [(now.strftime("%m/%d/%Y"), "PNC", product, Int_rate, Apy_rate)]
    df = pd.DataFrame(
        {'Date': now.strftime("%m/%d/%Y"), "Bank Name": 'PNC', 'Product Name': product, 'Interest Rate': Int_rate,
         "APY Rate": Apy_rate,
         "Loan Amount": price, "Zipcode": zipcode, "Term": Term})
    df = df.reindex(
        columns=["Date", "Bank Name", "Product Name", "Loan Amount", "Zipcode", "Term", "" "Interest Rate", "APY Rate"])
    df = df.iloc[0:2,:]
    df.to_csv(output_path + "PNC_Data_Mortgage_5lakh_VHR.csv".format(now.strftime("%m_%d_%Y")), index=False)

    df1 = pd.read_csv(output_path + "PNC_Data_Mortgage_1LAKH_complete.csv")
    df2 = pd.read_csv(output_path + "PNC_Data_Mortgage_3LAKH_complete.csv")
    df3 = pd.read_csv(output_path+"PNC_Data_Mortgage_5lakh_FixedR.csv")
    df4 = pd.read_csv(output_path + "PNC_Data_Mortgage_5lakh_AdjustR.csv")
    df5 = pd.read_csv(output_path + "PNC_Data_Mortgage_5lakh_FHAR.csv")
    df6 = pd.read_csv(output_path + "PNC_Data_Mortgage_5lakh_VHR.csv")
    df2 = pd.concat([df1, df2, df3, df4, df5, df6])

#####################################################################################################################
    df2["Date"] = now.strftime("%m-%d-%Y")
    df2["Bank_Name"]= "PNC FINANCIAL SERVICES GROUP INC"
    df2["Bank_Product"]= "Mortgages"
    df2["Bank_Product_Type"] = "Mortgages"
    df2["Bank_Offer_Feature"] = "Offline"
    df2["Bank_Product_Name"] = df2["Product Name"]
    df2["Product_Term"] = df2["Term"]
    df2["Balance"] = np.NAN
    df2["Product_Interest"] = df2["Interest Rate"]
    df2["Product_Apy"] = np.NAN
    df2["Mortgage_Down_Payment"] = "20%"
    df2["Mortgage_Loan"] = df2["Loan Amount"]
    df2["Min_Credit_Score_Mortagage"] = "720+"
    df2["Mortgage_Apr"] = df2["APY Rate"]
    df2 = df2.reindex(columns=["Date", "Bank_Name","Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name", "Product_Term", "Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage", "Mortgage_Apr"])
    for i in range(len(df2.index)):
        df2["Bank_Product_Name"].iloc[i]=str(df2["Bank_Product_Name"].iloc[i].replace("Loan Details", ""))
    df2.to_csv(output_path + "Consolidate_PNC_Data_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)

