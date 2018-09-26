from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import warnings
from maks_lib import output_path

warnings.simplefilter(action='ignore')

now = datetime.datetime.now()


class App:

    def __init__(self, url='https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/adjustable-mortgage.html',
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
        Term = ["30","30","30",""]
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
    df = df.iloc[0:3,:]
    df.to_csv(output_path + "PNC_Data_Mortgage_5lakh_AdjustR.csv".format(now.strftime("%m_%d_%Y")), index=False)