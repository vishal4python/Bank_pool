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

    def __init__(self, url = 'https://www.bankofamerica.com/mortgage/mortgage-rates/ ',Pur_pri='375,000', zipcode='10004',
                 down_pay = '75,000'):
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
        E = ["30", "20", "15", "30", "30", "30"]
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
    sleep(5)
    A, B, C, D, E, loan  = app.data()
    app.browser_close()
    df = pd.DataFrame({'Date':now.strftime("%m/%d/%Y"),"Bank Name":'Bank Of America','Purchase price':price,
                       "Loan Amount":loan,"Zipcode":zipcode,"Product Name":A,"Rate":B,"APR":C,"Points":D,"Credit Score":"740","Product term":E,"Payment Type":"principal + interest"})
    df = df.reindex(columns=['Date',"Bank Name","Purchase price",
                       "Loan Amount","Zipcode","Product Name","Rate","APR","Points","Product term","Credit Score","Payment Type"])
    df.to_csv(output_path + "BOA_Data_Mortgage_375.csv".format(now.strftime("%m_%d_%Y")), index=False)
