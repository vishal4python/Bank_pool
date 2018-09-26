from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
today = datetime.datetime.now()
import pandas as pd
import time
import re
from tabulate import tabulate
from maks_lib import output_path
path = output_path+"Aggregator_BankRate_Data_Mortgage"+today.strftime('%Y_%m_%d')+".csv"
online_bank = ['Synchrony Bank', 'Ally Bank', 'Capital One 360']
start_time = time.time()
neededBanks = {
    "Ally Bank":'ALLY',
    "Bank of America":"BANK OF AMERICA CORP",
    "Capital One":"CAPITAL ONE",
    "Capital One 360":"CAPITAL ONE",
    "Chase":"JP MORGAN CHASE & Co.",
    "Citibank":"CITIGROUP INC",
    "Citibank, N. A.":"CITIGROUP INC",
    "PNC":"PNC FINANCIAL SERVICES GROUP INC",
    "Synchrony Bank":"SYNCHRONY",
    "Wells Fargo":"WELLS FARGO",
    "SunTrust":"SUNTRUST BANKS INC",
    "Visit Ally Bank  site":"ALLY",
    "Visit Citibank, N. A. site":"CITIGROUP INC"

}

Excel_Table = []
table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest',
                 'APR', 'Mortgage_Loan_Amt']
# Excel_Table.append(table_headers)
driver = webdriver.Firefox()
driver.maximize_window()

cases = [[125000,25000],[375000,75000], [625000,125000]]
for case in cases:
    driver.get("https://www.bankrate.com/mortgage.aspx?propertyvalue="+str(case[0])+"&loan="+str(case[0]-case[1])+"&perc=20&prods=1,2,3,8,6,9,10&fico=740&points=Zero&zipcode=10004&cs=1&type=newmortgage")
    # time.sleep(10)
    # driver.find_element_by_xpath('//*[@id="purchase-price"]').clear()
    # driver.find_element_by_xpath('//*[@id="purchase-price"]').send_keys(case[0])
    driver.find_element_by_tag_name('body').click()
    # driver.find_element_by_xpath('//*[@id="property-downpayment"]').clear()
    # driver.find_element_by_xpath('//*[@id="property-downpayment"]').send_keys(case[1])
    driver.find_element_by_tag_name('body').click()
    driver.find_element_by_css_selector('form.\+mg-bottom-none > input:nth-child(1)').clear()   #/html/body/div[5]/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/form/input
    driver.find_element_by_css_selector('form.\+mg-bottom-none > input:nth-child(1)').send_keys(10004)    #//*[@id="property-location"]/div/form/input
    driver.find_element_by_tag_name('body').click()
    # time.sleep(8)
    driver.find_element_by_css_selector('button.--primary').click()     #//*[@id="search"]/ul/li[8]/button
    # driver.find_element_by_xpath('//*[@id="search"]/ul/li[8]/button').click()
    time.sleep(5)


    while True:
        try:

            time.sleep(3)
            element = driver.find_element_by_xpath("//tr[@class='+text-center']//button[@class='offer__expand-offers-button button --secondary --small +mg-top-sm']")#.click()
            driver.execute_script("arguments[0].click();", element)
            print("@@@@@@@@")
            time.sleep(3)
        except Exception as e:
            print(e)
            break

    jsoup = BeautifulSoup(driver.page_source)
    result = jsoup.find('div', attrs={'class':'offers-list-expanded-wrap rate-table'})
    table_list = result.find_all('table')

    for table in table_list:
        # print(table)

        trs = table.find('tbody').find_all('tr')

        for tr in trs:
            print('-'.center(100, '-'))
            try:
                divs = tr.find_all('div', attrs={'class':re.compile('offer__column|offer__payment')})
                print(len(divs))
                if len(divs) >= 3:
                    h4 = divs[0].find('h4')
                    if h4 is None:
                        h4 = divs[0].find('img')['alt']
                    else:
                        h4 = h4.text
                    Bank_name = h4.strip()
                    bank_product_name = divs[0].find('div', attrs={'class':re.compile('offer__fees')})
                    bank_product_name = bank_product_name.text.split('|')[0] if bank_product_name is not None else None
                    apr = divs[1].find('div', attrs={'data-test':re.compile('apr')})
                    apr = apr.text if apr is not None else None

                    rate = divs[1].find('div', attrs={'data-test': re.compile('rate')})
                    rate = rate.text if rate is not None else None

                    print('Bank_name = ', Bank_name)
                    print('bank_product_name = ', bank_product_name)
                    print('apr = ', apr)
                    print('rate = ', rate)

                    if Bank_name in neededBanks:

                        if Bank_name in online_bank:
                            Bank_Offer_Feature = 'Online'
                        else:
                            Bank_Offer_Feature = 'Offline'
                        a = [neededBanks[Bank_name.strip()], bank_product_name.strip(), None, Bank_Offer_Feature, None,'Interest_Type', rate.strip(),apr.strip(), case[0] - case[1]]
                        print(a)
                        Excel_Table.append(a)

            except Exception as e:
                print(e)



#
driver.close()
print(len(Excel_Table))
print(tabulate(Excel_Table))
# print('total length', t)
df = pd.DataFrame(Excel_Table, columns=table_headers)

df['Interest_Type'] = df['Bank_Product_Name'].apply(lambda x: 'Fixed' if 'fixed' in x.lower() else 'Variable')
df['Term (Y)'] = df['Term (Y)'].apply(lambda x: re.sub('[^0-9.]','',re.findall('\d.*yr',str(x),re.IGNORECASE)[0]) if len(re.findall('\d.*yr',str(x),re.IGNORECASE))>=1 else None)
df['Mortgage_Down_Payment'] = '20%'
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Term (Y)'] = df['Term (Y)'].apply(lambda x:30 if x is None else x)


df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = None
df["Source"] = "Bankrate.com"
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(lambda x:re.sub('\n',' ',x))
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APR", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode","Source"]
df = df[order]
print(df)
df.to_csv(path, index=False)
