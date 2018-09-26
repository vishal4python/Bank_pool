# -*-coding:utf-8 -*-
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import time
import numpy as np
from maks_lib import output_path

print('Program Execution Started...')
start_time = time.time()

#Required Fields for scraping the data
table_headers = ['Balance', 'Product_Interest', 'Product_Apy', 'Bank_Name', 'Date','Bank_Product_Name', 'Bank_Product_Type', 'Product_Term','Bank_Product','Bank_Offer_Feature']
today = datetime.datetime.now().strftime("%m-%d-%Y")
resp = requests.get("https://apps.pnc.com/rates/servlet/DepositRatesSearch?productGroup=saving&zipCode=10004")
table = []
order= ['Date', 'Bank_Name', 'Bank_Product', 'Bank_Product_Type', 'Bank_Offer_Feature','Bank_Product_Name', 'Product_Term', 'Balance', 'Product_Interest','Product_Apy']
bank_name = 'PNC FINANCIAL SERVICES GROUP INC'
Bank_Product = 'Deposits'
Bank_Offer_Feature = 'Offline'

#CSV File location
locationPath = output_path+'Consolidate_PNC_Data_Deposits'+str(today)+'.csv'

jsoup = BeautifulSoup(resp.content, "html.parser")
result = jsoup.find("div", attrs={"id": "results"})
if result is not None:
    # Checking Current Rates.
    currentRates = result.find("div", attrs={"id": "conCheckingDiv"})
    if currentRates is not None:
        rows = currentRates.find_all("tr")
        count = 0
        for row in rows:
            tds = row.find_all("td")
            if tds is not None:

                if len(tds) == 1:
                    heading = tds[0].find("th").text
                    count = count+1
                elif len(tds) == 3:
                    tdData = []
                    bFount = False
                    for td in tds:
                        td = re.sub(r'[ +,\n,\t]', '', td.text.strip())
                        if 'Bala' in td:
                            bFount = True
                            break
                        else:
                            tdData.append(td)
                    if not bFount:
                        tds = tdData
                        tds.append(bank_name)
                        tds.append(today)
                        tds.append(heading)
                        tds.append("Checking")
                        tds.append(None)
                        tds.append(Bank_Product)
                        tds.append(Bank_Offer_Feature)
                        table.append(tds)

        df = pd.DataFrame(table[1:],columns=table_headers)
        Checking_df = df[order]

    else:
        print("currentRates Not Found")

    # Savings :
    savingsTable = []
    conSavingsLink = result.find("div", attrs={"id": "conSavingsDiv"})
    if conSavingsLink is not None:

        # Standard Savings:
        stdSavings = conSavingsLink.find("div", attrs={"id": "Standard Savings"})
        if stdSavings is not None:
            stdSavings_heading = stdSavings.find("tr", attrs={"class": "headingtext"})
            if stdSavings_heading is not None:
                stdSavings_heading = stdSavings_heading.text
                stdSavings_heading =re.sub('[\t,\n]', '', stdSavings_heading)
                savingsTable.append([stdSavings_heading.strip(), '', ''])
                stdSavings_sub_heading = stdSavings.find_all("th")
                if stdSavings_sub_heading is not None:
                    savingsTable.append([th.text for th in stdSavings_sub_heading])

                stdSaving_data = stdSavings.find_all("tr")
                if stdSaving_data is not None:

                    for std_s_d in stdSaving_data[2:]:
                        std_s_d_tds = std_s_d.find_all('td')
                        if std_s_d_tds is not None:
                            stdDataTable = [re.sub(r'[ +,\n,\t]', '', std_s_d_td.text.strip()) for std_s_d_td in
                                            std_s_d_tds]
                            stdDataTable.append(bank_name)
                            stdDataTable.append(today)
                            stdDataTable.append(stdSavings_heading)
                            stdDataTable.append('Savings')
                            stdDataTable.append(None)
                            stdDataTable.append(Bank_Product)
                            stdDataTable.append(Bank_Offer_Feature)
                            savingsTable.append(stdDataTable)

            stdf = pd.DataFrame(savingsTable[2:],columns=table_headers)
            stdf = stdf[order]
        else:
            print("Standard Savings Not Found")

        # s for savings:
        savingsTable = []
        sSavings = conSavingsLink.find("div", attrs={"id": "'S' is for Savings"})
        if sSavings is not None:
            sSavings_heading = sSavings.find("tr", attrs={"class": "headingtext"})
            if sSavings_heading is not None:
                sSavings_heading = sSavings_heading.text
                savingsTable.append([re.sub('[\n]', '', sSavings_heading).strip(), '', ''])
                sSavings_sub_heading = sSavings.find_all("th", attrs={"class": "headerColumn"})
                if sSavings_sub_heading is not None:
                    ss_sub_heading_list = [th.text for th in sSavings_sub_heading]
                    savingsTable.append(ss_sub_heading_list)

                sSavings_data = sSavings.find_all("tr")
                if sSavings_data is not None:
                    for ssd_s_d in sSavings_data[3:]:
                        ssd_s_d_tds = ssd_s_d.find_all('td')
                        if ssd_s_d_tds is not None:
                            savingsTableData = []
                            for ssd_s_d_td in ssd_s_d_tds:
                                ssd_s_d_td = re.sub(r'[ +,\n,\t]', '', ssd_s_d_td.text.strip())
                                if len(ssd_s_d_td)!=0:
                                    savingsTableData.append(ssd_s_d_td)
                            savingsTableData.append(bank_name)
                            savingsTableData.append(today)
                            savingsTableData.append(sSavings_heading.strip())
                            savingsTableData.append('Savings')
                            savingsTableData.append(None)
                            savingsTableData.append(Bank_Product)
                            savingsTableData.append(Bank_Offer_Feature)
                            savingsTable.append(savingsTableData)

            s_saving_df = pd.DataFrame(savingsTable[2:],columns=table_headers)
            s_saving_df = s_saving_df[order]

            # print(s_saving_df)
        else:
            print("'S' is for Savings Not Found")

    else:
        print("conSavingsLink Not Found")

    # Money Market Account
    MMA = result.find("div", attrs={"id": "conMMDiv"})
    moneyTable = []
    if MMA is not None:
        MMA_heading = MMA.find("th", attrs={"class": "l orangeText"})
        if MMA_heading is not None:
            moneyTable.append([MMA_heading.text, '', ''])
        MMA_sub = MMA.find("tr", attrs={"class": "prodHeader headingtext"})
        if MMA_sub is not None:
            MMA_sub_heading = MMA_sub.find_all("th")
            if MMA_sub_heading is not None:
                moneyTable.append([MMA_sub_heading[1].text, '', ''])
        MMA_sec_sub = MMA.find("tr", attrs={"class": "b rowDataMM indent8"})
        if MMA_sec_sub is not None:
            MMA_sec_sub_tds = MMA_sec_sub.find_all("td")
            if MMA_sec_sub_tds is not None:
                moneyTable.append([MMA_sec_sub_tds[0].text, MMA_sec_sub_tds[1].text, MMA_sec_sub_tds[2].text])

        MMA_DATA = MMA.find_all("tr", attrs={"class": "indent8 rowDataMM"})
        if MMA_DATA is not None:
            for mmaData in MMA_DATA:
                mmaData_tds = mmaData.find_all("td")
                if mmaData_tds is not None:
                    mmDataTable = []
                    for id, mmaData_td in enumerate(mmaData_tds):
                        if id in [0, 1, 2]:
                            mmDataTable.append(re.sub(r'[ ,\n,\t]', '', mmaData_td.text))
                    moneyTable.append(mmDataTable)

        mf = pd.DataFrame(moneyTable[3:], columns=['Balance', 'Product_Interest', 'Product_Apy'])
        ['Balance', 'Product_Interest', 'Product_Apy', 'Bank_Name', 'Date', 'Bank_Product_Name', 'Bank_Product_Type']
        mf.loc[:, 'Bank_Name'] = bank_name
        mf.loc[:, 'Date'] = today
        mf.loc[:, 'Bank_Product_Name'] = MMA_heading.text.rstrip('\n')
        mf.loc[:, 'Bank_Product_Type'] = 'Money Market'
        mf.loc[:, 'Bank_Product'] = Bank_Product
        mf.loc[:, 'Bank_Offer_Feature'] = Bank_Offer_Feature
        mf.loc[:, 'Product_Term'] = None
        mf = mf[order]

    else:
        print("Money Market Account Not Found")

    # CDs
    cdTable = []
    CD = result.find("div", attrs={"id": "conCdsDiv"})
    if CD is not None:
        cd_heading = CD.find("tr", attrs={"class": "prodHeader"})
        if cd_heading is not None:
            cd_heading = cd_heading.find_all("span")
            if cd_heading is not None:
                cdTable.append([cd_heading[0].text, '', '', '', ''])
        cd_main_headings = CD.find("tr", attrs={"class": "indent8 headingtext"})
        if cd_main_headings is not None:
            cd_main_headings = cd_main_headings.find_all("th")
            if cd_main_headings is not None:
                cdTable.append([cd_main_headings[0].text, '', '', cd_main_headings[-1].text, ''])
        cd_sub_heading = CD.find("tr", attrs={"class": "b rowData indent8"})
        if cd_sub_heading is not None:
            cd_sub_heading = cd_sub_heading.find_all("td")
            if cd_sub_heading is not None:
                cdTable.append(
                    [cd_sub_heading[0].text, cd_sub_heading[1].text, cd_sub_heading[2].text, cd_sub_heading[-2].text,
                     cd_sub_heading[-1].text])

        tableData = CD.find("div", attrs={"class": "accordion-content"})
        tableData = str(tableData)
        try:
            tableData1 = tableData[:tableData.rindex('<tr class="prodHeader">')]
            tableData1 = BeautifulSoup(tableData1, "html.parser")

            tableData2 = tableData[tableData.rindex('<tr class="prodHeader">'):]
            tableData2 = BeautifulSoup(tableData2, "html.parser")

            cd_datas = tableData1.find_all("tr", attrs={"class": "indent8 rowData"})

            for cd_data in cd_datas:
                cd_data_tds = cd_data.find_all("td")
                cdList = []
                for id, cd_data_td in enumerate(cd_data_tds):
                    if id not in [3, 4, 5, 6]:
                        cd_data_td = re.sub(r'[\t, ,\n]', '', cd_data_td.text)
                        if len(cd_data_td) == 0:
                            cd_data_td = None
                        cdList.append(cd_data_td)
                cdTable.append(cdList)

            # Ready Access Certificate of Deposit in CD's
            RACDTable = []
            racdHeading = tableData2.find("th", attrs={"class": "l orangeText"})
            if racdHeading is not None:
                racdHeading = racdHeading.find("span").text
                RACDTable.append([racdHeading, '', '', ''])
            racdSubHeading = tableData2.find("tr", attrs={"class": "indent8 headingtext"})
            if racdSubHeading is not None:
                racdSubHeading = racdSubHeading.find_all("th")[3].text
                RACDTable.append(['', '', racdSubHeading, ''])
            racdData = tableData2.find_all("tr", attrs={"class": "indent8 rowData"})
            if racdData is not None:
                for row in racdData[1:]:

                    racdTData = []
                    for id, td in enumerate(row.find_all("td")):
                        if id not in [2, 3, 4, 5]:
                            racdTData.append(re.sub('[\t,\n]', '', td.text).strip())
                    RACDTable.append(racdTData)

            cdf = pd.DataFrame(cdTable)

            cdf[[0, 1]] = cdf[[0, 1]].ffill()
            df_to_list = cdf.values.tolist()
            dummyDict = {"6MONTHS": [], "12MONTHS": [], "36MONTHS": []}
            filterList = [l for l in df_to_list[:3]]

            for lo in df_to_list[3:]:
                for key in dummyDict.keys():
                    if lo[0] == key:
                        a = dummyDict[key]
                        a.append(lo)
                        dummyDict[key] = a

            for key in dummyDict.keys():
                for k in dummyDict[key]:
                    filterList.append(k)

            cdTableDF = pd.DataFrame(filterList[3:], columns=['Product_Term', '', 'Balance', 'Product_Interest', 'Product_Apy'])
            cdTableDF.loc[:, 'Bank_Name'] = 'PNC FINANCIAL SERVICES GROUP INC'
            cdTableDF.loc[:,'Date'] = today
            cdTableDF.loc[:, 'Bank_Product_Name'] = cd_heading[0].text
            cdTableDF.loc[:, 'Bank_Product_Type'] = 'CD'
            cdTableDF.loc[:, 'Bank_Product'] = Bank_Product
            cdTableDF.loc[:, 'Bank_Offer_Feature'] = Bank_Offer_Feature
            cdTableDF['Product_Term'] = cdTableDF['Product_Term'].apply(lambda x: re.sub('[^0-9]','',x))
            cdTableDF = cdTableDF[order]

            racdf = pd.DataFrame(RACDTable[2:], columns=['Product_Term', 'Balance', 'Product_Interest', 'Product_Apy'])
            racdf['Product_Term'] = racdf['Product_Term'].apply(lambda x: re.sub('[^0-9]', '', x))
            racdf.loc[:, 'Bank_Name'] = 'PNC FINANCIAL SERVICES GROUP INC'
            racdf.loc[:, 'Date'] = today
            racdf.loc[:, 'Bank_Product_Name'] = racdHeading
            racdf.loc[:, 'Bank_Product_Type'] = 'CD'
            racdf.loc[:, 'Bank_Product'] = Bank_Product
            racdf.loc[:, 'Bank_Offer_Feature'] = Bank_Offer_Feature
            racdf = racdf[order]
            bigdata = Checking_df.append(stdf, ignore_index=True)
            bigdata = bigdata.append(s_saving_df, ignore_index=True)
            bigdata = bigdata.append(mf, ignore_index=True)
            bigdata = bigdata.append(cdTableDF, ignore_index=True)
            bigdata = bigdata.append(racdf, ignore_index=True)
            bigdata["Mortgage_Down_Payment"] = np.nan
            bigdata["Mortgage_Loan"] = np.nan
            bigdata["Min_Credit_Score_Mortagage"] = np.nan
            bigdata["Mortgage_Apr"] = np.nan
            bigdata['Bank_Product_Type'] = bigdata['Bank_Product_Type'].apply(lambda x:'Savings' if 'money' in x.lower() else x)
            bigdata.to_csv(locationPath, index= False)
        except Exception as e:
            print(e)

    else:
        print("CD Not Found")

else:
    print("Data Not Found")

print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')