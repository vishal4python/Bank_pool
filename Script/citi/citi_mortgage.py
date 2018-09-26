from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import  BeautifulSoup as bs
import pandas as pd
import time
import warnings
import datetime
import os


now = datetime.datetime.now()

warnings.simplefilter(action='ignore')


class Citi_mortgage:
    def __init__(self, url, eprice, dprice):
        self.url = url
        self.eprice = eprice
        self.dprice = dprice

    def start_driver(self):
        self.driver = webdriver.Firefox()

    def close_driver(self):
        return self.driver.close()

    def get_url(self):
        return self.driver.get(self.url)

    def fillform(self):
        time.sleep(6)
        self.driver.maximize_window()
        #time.sleep(1)
        select = Select(self.driver.find_element_by_id("propertyKind"))
        #time.sleep(1)
        select.select_by_visible_text("Single Family Home")
        #time.sleep(1)
        select = Select(self.driver.find_element_by_id("propertyUse"))
        select.select_by_value("P")
        #time.sleep(1)
        inutelement = self.driver.find_element_by_id("propCity")
        inutelement.send_keys('New York')
        #time.sleep(1)
        select = Select(self.driver.find_element_by_id("propState"))
        select.select_by_value("NY")
        #time.sleep(1)
        select = Select(self.driver.find_element_by_id("propCounty"))
        select.select_by_value("36061")
        #time.sleep(1)
        inutelement = self.driver.find_element_by_id("purchPrice")
        inutelement.send_keys(self.eprice[1])
        #time.sleep(1)
        inutelement = self.driver.find_element_by_id("desiredLoanAmount")
        inutelement.send_keys(self.dprice[1])
        #time.sleep(1)
        self.driver.find_element_by_id("creditScoreGoodLabel").click()
        self.driver.find_element_by_id("submit-purchase").click()
        time.sleep(15)


    def get_current_url(self):
        return self.driver.current_url

    def save_page(self):
        page = self.driver.page_source
        with open("citi_mortgage_"+self.eprice[0]+".html", 'w')as file:
            file.write(page)

    def unhide(self):
        pass

class ExtractInfo(Citi_mortgage):

    def __init__(self, page,tab, eprice, dprice):
        self.page = page
        self.tab = tab
        self.eprice = eprice
        self.dprice = dprice

    def findtables_tab1(self):
        soup = bs(self.page, "lxml")
        file = open("test.txt",'w')
        h = [ f.text for f in soup.find_all('h1', {'class':self.tab[0]})]
        d = [j.text for j in soup.find_all('div', {'class':self.tab[1]})]
        for l in zip(h,d):
            la= l[1].split('\n')
            if 'points' in la[30]:
                #f = l[0]+","+la[5]+","+la[12]+","+la[30]+'\n'
                f = l[0] + "\t" + la[5] + "\t" + la[12]+'\n'
                file.write(f)

            elif "points" in la[27]:
                f = l[0]+"\t"+la[5]+"\t"+la[12]+'\n'
                #f = l[0] + "," + la[5] + "," + la[12] + "," + la[27] + '\n'
                file.write(f)
        file.close()
        time.sleep(3)
        dataset = pd.read_table('test.txt',sep='\t',delimiter=None, header=None)
        #dataset['Expected_Price'] = self.eprice[1]
        dataset['Mortgage_Loan'] = self.dprice
        dataset["Product_Term"] = dataset.iloc[:,0].str.replace("Fixed","")

        loan_type = pd.DataFrame(dataset.iloc[:,0].str.split(" ").tolist())
        dataset["Loan_Type"] = loan_type.iloc[:,2].str.replace("ARM","Variable")

        dataset.columns = ['Bank_Product_Name','Product_Interest','Mortgage_Apr',"Mortgage_Loan","Product_Term",'Loan_Type']
        #print(dataset)
        dataset.to_csv("Citi_Mortgage_"+self.eprice[0]+".csv",index=False)


if __name__ == "__main__":
    #log.info("Starting scrapping")
    expected_price = [('case1','120000'),('case2','360000'),('case3','600000')]
    desired_price = [('case1','100000'),('case2','300000'),('case3','500000')]
    # url = "https://online.citi.com/US/nccmi/purchase/ratequote/flow.action?fromLanding=true&selectedOption=CUSTOM&selectedOptionValue=CUSTOMpurChaseLanding&JFP_TOKEN=3GBHQLZG"
    # for i in range(len(expected_price)):
    #     obj = Citi_mortgage(url, expected_price[i], desired_price[i])
    #     obj.start_driver()
    #     obj.get_url()
    #     obj.fillform()
    #     obj.save_page()
    #     obj.close_driver()
    #     time.sleep(5)

    tab1 = ['header-3 rate-card-panel-header-white', 'row rate-card-panel-items tb-hide']
    for i in range(len(expected_price)):
        extract = ExtractInfo(open("citi_mortgage_"+expected_price[i][0]+".html",'r'),tab1, expected_price[i], desired_price[i][1])
        extract.findtables_tab1()
    df1 = pd.read_csv("Citi_Mortgage_case1.csv")
    df2 = pd.read_csv("Citi_Mortgage_case2.csv")
    df3 = pd.read_csv("Citi_Mortgage_case3.csv")
    df = pd.concat([df1, df2, df3])
    df['Date'] = now.strftime("%m-%d-%Y")
    df['Bank_Name'] = "CITIGROUP INC"
    df['Bank_Product'] = "Mortgage"
    df['Bank_Product_Type'] = "Mortgage"
    df["Bank_Offer_Feature"] = "offline"
    df['Mortgage_Down_Payment'] = "20%"
    #print(df["Product_Term"].astype(str)[5])
    for val, row in df.iterrows():
        if "ARM" in row["Product_Term"]:
            df.ix[val,"Product_Term"] = "30 Year"
    dff = df.reindex(columns=["Date", "Bank_Name" , "Bank_Product" , 'Bank_Offer_Feature' ,
                                    'Bank_Product_Type' , 'Bank_Product_Name' ,
                                    'Mortgage_Loan' , 'Loan_Type' , 'Product_Term' , 'Mortgage_Down_Payment',
                                    'Product_Interest' , 'Mortgage_Apr'])

    dff.to_csv("final_citi.csv")
    os.remove("Citi_Mortgage_case1.csv")
    os.remove("Citi_Mortgage_case2.csv")
    os.remove("Citi_Mortgage_case3.csv")



