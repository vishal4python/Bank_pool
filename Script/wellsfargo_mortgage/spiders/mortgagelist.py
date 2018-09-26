# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
import numpy as np
import datetime
import warnings
now = datetime.datetime.now()
import pandas as pd


class MortgagelistSpider(scrapy.Spider):
    name = "mortgagelist"
    allowed_domains = ["wellsfargo.com"]

    def start_requests(self):
        #self.count = count
        for i in range(1, 11):
            url = 'https://www.wellsfargo.com/mortgage/rates/purchase-assumptions?prod='+str(i)
            print("URL:", url)
            yield Request(url, self.parse)


    def parse(self, response):
        fun_type = ""
        loan = response.css('h1.c11::text').extract_first()
        if loan == "Purchase Rate Assumptions and APR Information":
            l = loan
        fun_type=[]
        fund_confir = response.css('h2.c66title > a[data-content-id="844563216"]::text').extract_first()
        fund_jumbo = response.css('h2.c66title > a[data-content-id="844563516"]::text').extract_first()
        fund_gover = response.css('h2.c66title > a[data-content-id="849750316"]::text').extract_first()
        if fund_confir is not None:
            fun_type.append(fund_confir)
        elif fund_jumbo is not None:
            fun_type.append(fund_jumbo)
        elif fund_gover is not None:
            fun_type.append(fund_gover)
        # if fund_confir == "Conforming Loan":
        #     fun_type.append(fund_confir)
        # elif fund_jumbo == "Jumbo Loan":
        #     fun_type.append(fund_jumbo)
        # elif fund_gover == "Government Loan":
        #     fun_type.append(fund_gover)
        # print(fun_type)

        Down_Payment= response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[4]/td/text()').extract_first()
        Down_Payment = Down_Payment.strip()
        url_str =response.url
        final = url_str.lstrip('https://www.wellsfargo.com/mortgage/rates/purchase-assumptions?prod=')
        # 'Loan Category': l,
        # 'Credit Score': response.css('div#contentBody > p::text').extract_first(),
        # 'Funding Type': fun_type,
        # 'Product Name': response.css('table.c65Table > thead > tr > th.c66tableTitle::text').extract(),
        # 'Interest Rate': response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[1]/td/text()').extract(),
        # 'APY': response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[2]/td/text()').extract(),
        # 'Loan Amount': response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[3]/td/text()').extract(),
        # 'Down Payment':Down_Payment,
        # 'Term Tenor': response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[5]/td/text()').extract(),
        # 'Bank Name':'Wellsfargo',
        # 'Date': now.strftime("%m-%d-%Y"),
        item ={
            'Loan Category': l,
            'Credit Score' : response.css('div#contentBody > p::text').extract_first(),
            'Funding Type' : fun_type,
            'Product Name' : response.css('table.c65Table > thead > tr > th.c66tableTitle::text').extract(),
            'Interest Rate' : response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[1]/td/text()').extract(),
            'APY' : response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[2]/td/text()').extract(),
            'Loan Amount': response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[3]/td/text()').extract(),
            'Down Payment':Down_Payment,
            'Term Tenor' : response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[5]/td/text()').extract(),
            'Bank Name':'Wellsfargo',
            'Date': now.strftime("%m-%d-%Y"),
        }
        yield item


        df = pd.read_csv('output.csv')
        df = df.reindex(columns= ["Date","Bank Name","Funding Type","Loan Amount","Credit Score","Product Name","Term Tenor",'Interest Rate', 'APY',
                                  "Down Payment"])
        df.to_csv("WellsF_Data_Mortgage.csv".format(now.strftime("%m_%d_%Y")), index=False)
        df9 = pd.read_csv("C:\\Users\\Nimmi\\wellsfargo\\wellsfargo\\spiders\\WellsF_Data_Mortgage.csv")
        df9["Date"] = now.strftime("%m-%d-%Y")
        df9["Bank_Name"] = "WELLS FARGO"
        df9["Bank_Product"] = "Mortgages"
        df9["Bank_Product_Type"] = "Mortgages"
        df9["Bank_Offer_Feature"] = "Offline"
        df9["Bank_Product_Name"] = df9["Product Name"]
        df9["Product_Term"] = df9["Term Tenor"].str.strip(' yrs ')
        df9["Balance"] = np.NAN
        df9["Product_Interest"] = df9["Interest Rate"]
        df9["Product_Apy"] = np.NAN
        df9["Mortgage_Down_Payment"] = df9["Down Payment"].str.replace('.0%', '') + "%"
        df9["Mortgage_Loan"] = df9["Loan Amount"].str.strip('$')
        df9["Min_Credit_Score_Mortagage"] = "740"
        df9["Mortgage_Apr"] = df9["APY"]
        df9 = df9.reindex(columns=["Date", "Bank_Name", "Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature",
                                   "Bank_Product_Name", "Product_Term", "Balance", "Product_Interest", "Product_Apy",
                                   "Mortgage_Down_Payment", "Mortgage_Loan", "Min_Credit_Score_Mortagage",
                                   "Mortgage_Apr"])
        df9.to_csv("Consolidate_WellsF_Data_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")),
                   index=False)



