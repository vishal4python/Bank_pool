from selenium import webdriver
import pandas as pd
from time import sleep
import numpy as np
import datetime
import warnings
from maks_lib import output_path
warnings.simplefilter(action='ignore')

now = datetime.datetime.now()

class Accountdata:

    def __init__(self, zipcode=10004, url = 'https://www.wellsfargo.com/savings-cds/rates/'):
        self.zipcode = zipcode
        self.url = url
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        sleep(3)
        self.login()

    def login(self):
        zipcode_input = self.driver.find_element_by_xpath('//*[@id="zipCode"]')
        zipcode_input.send_keys(self.zipcode)
        continue_btn = self.driver.find_element_by_xpath('//*[@id="c28lastFocusable"]')
        continue_btn.click()

    def datable(self):
        html_source = self.driver.page_source
        df = pd.read_html(html_source)
        return df

    def browser_close(self):
        self.driver.close()

if __name__ == '__main__':
    app = Accountdata()
    sleep(10)
    df = app.datable()
    df[0]["Term"] = np.NAN
    df[0]["Product Name"] = "Wells Fargo Way2Save"
    df[0] = df[0].reindex(columns=["Product Name","Term", "Balance", "Interest Rate", "APY"])
    df[1].drop(columns=["Bonus Interest Rate", "Bonus APYFootnote 11"], inplace=True)
    df[1]["Term"] = np.NAN
    df[1]["Product Name"] = "Platinum Savings - Special Interest"
    df[1] = df[1].reindex(columns=["Product Name","Term", "Balance", "Interest Rate", "APY"])
    df[1].drop([3], inplace=True)
    df[2].drop(columns=["Bonus Interest Rate", "Bonus APY1"], inplace=True)
    df[2]["Term"] = np.NAN
    df[2]["Product Name"] = "Platinum Savings - Standard Interest"
    df[2] = df[2].reindex(columns=["Product Name","Term", "Balance", "Interest Rate", "APY"])
    df[3]["Balance"] = np.NAN
    df[3]["Product Name"] = "Special CD"
    df[3].drop(columns=["Bonus Interest Rate", "Bonus APYFootnote 11", "Renewal term"], inplace=True)
    df[3] = df[3].reindex(columns=["Product Name","Term", "Balance", "Interest Rate", "APY"])
    df[5]["Balance"] = np.NAN
    df[5]["Product Name"] = "Standard CD"
    df[5].drop(columns=["Bonus Interest Rate", "Bonus APYFootnote 55,Footnote 11"], inplace=True)
    df[5] = df[5].reindex(columns=["Product Name","Term", "Balance", "Interest Rate", "APY"])

    last_df = df[4]
    final_df = pd.DataFrame()
    res = np.split(last_df, 3)
    for mini_df in res:
        first_line = pd.DataFrame(mini_df.iloc[0, :]).transpose()
        rest_lines = mini_df.iloc[1:, :]
        rest_lines["Balance"] = rest_lines["Bonus APYFootnote 11"]
        rest_lines["Bonus APYFootnote 11"] = rest_lines["Bonus Interest Rate"]
        rest_lines["Bonus Interest Rate"] = rest_lines["APY"]
        rest_lines["APY"] = rest_lines["Interest Rate"]
        rest_lines["Interest Rate"] = rest_lines["Term"]
        rest_lines["Term"] = np.NAN
        mini_df = pd.concat([first_line, rest_lines])
        final_df = pd.concat([final_df, mini_df])
    df[4] = final_df
    df[4]["Product Name"] = "CD"
    df[4].drop(columns=["Bonus Interest Rate", "Bonus APYFootnote 11"], inplace=True)
    df[4] = df[4].reindex(columns=["Product Name","Term", "Balance", "Interest Rate", "APY"])
    df = pd.concat([df[0], df[1], df[2], df[3], df[4], df[5]])
    app.browser_close()
    df["Date"] = now.strftime("%m/%d/%Y")
    df["Bank Name"] = "Wells Fargo"
    df5 = df.reindex(columns=["Date","Bank Name","Product Name","Term", "Balance", "Interest Rate", "APY"])

#####################################################################################################################
    df5["Date"] = now.strftime("%m-%d-%Y")
    df5["Bank_Name"] = "WELLS FARGO"
    df5["Bank_Product"] = "Deposits"
    df5["Bank_Product_Type"] = "CD"
    df5["Bank_Offer_Feature"] = "Offline"
    df5["Bank_Product_Name"] = df5["Product Name"]
    df5["Product_Term"] = df5["Term"].str.strip("  months")
    df5["Balance"] = df5["Balance"]
    df5["Product_Interest"] = df5["Interest Rate"]
    df5["Product_Apy"] = df5["APY"]
    df5["Mortgage_Down_Payment"] = np.NAN
    df5["Mortgage_Loan"] = np.NAN
    df5["Min_Credit_Score_Mortagage"] = np.NAN
    df5["Mortgage_Apr"] = np.NAN
    df5 = df5.reindex(
        columns=["Date", "Bank_Name", "Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name",
                 "Product_Term", "Balance", "Product_Interest", "Product_Apy", "Mortgage_Down_Payment", "Mortgage_Loan",
                 "Min_Credit_Score_Mortagage", "Mortgage_Apr"])
    df5.iloc[0:5]["Bank_Product_Type"]="Savings"
    df5.iloc[11:16]["Product_Term"]='3'
    df5.iloc[17:22]["Product_Term"]='6'
    df5.iloc[22:28]["Product_Term"]='12'
    df5 = df5.drop(df5.index[28])
    df6 = df5.iloc[4:,:]
    df5 = df5.iloc[0:1,:]
    df = pd.concat([df5, df6])
    df.to_csv(output_path + "Consolidate_WellsF_Data_Saving_Acc{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
