from selenium import webdriver
from bs4 import BeautifulSoup
from tabulate import tabulate
import numpy as np
import datetime
import pandas as pd
import time
import re
from maks_lib import output_path


print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()

#Csv file location
path = output_path+"Aggregator_BankRate_Data_Deposit"+today.strftime('%Y_%m_%d')+".csv"

#Making Bank_Offer_Feature Online or Offline based on online_banks
online_bank = ['Synchrony Bank', 'Ally Bank', 'Capital One 360']

#Filtering Banks(Required Banks Only) using neededBanks
neededBanks = {
    "Ally Bank":'ALLY',
    "Bank of America":"BANK OF AMERICA CORP",
    "Capital One":"CAPITAL ONE",
    "Capital One 360":"CAPITAL ONE",
    "Chase":"JP MORGAN CHASE & Co.",
    "Chase Bank":"JP MORGAN CHASE & Co.",
    "Citibank":"CITIGROUP INC",
    "PNC":"PNC FINANCIAL SERVICES GROUP INC",
    "Synchrony Bank":"SYNCHRONY",
    "Wells Fargo":"WELLS FARGO",
    "SunTrust":"SUNTRUST BANKS INC",


}

#Required Fields for scraping the data
table_headers = ['Bank_Name', 'Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term_in_Months', 'Interest', 'APY']
Excel_Table = []

#Create a driver object using selenium Module
driver = webdriver.Firefox()
driver.maximize_window()

# =========================Savings==============================================
try:
    driver.get("https://www.bankrate.com/banking/savings/rates/")
    time.sleep(8)
    driver.find_element_by_xpath("//input[@name='location']").clear()

    driver.find_element_by_xpath("//input[@name='location']").send_keys(10004)
    time.sleep(5)

    driver.find_element_by_tag_name('body').click()
    time.sleep(5)
    # size = driver.find_element_by_xpath('//*[@id="csstyle"]/div[5]/div[1]/div[3]/div[1]/p/strong').text

    # print(size)
    while True:
        try:

            time.sleep(3)
            element = driver.find_element_by_css_selector('#csstyle > main > section > button')#.click()
            driver.execute_script("arguments[0].click();", element)
            time.sleep(3)
        except Exception as e:
            print(e)
            break


    #Getting data from pageSource by using BeautifuSoup Module
    jsoup = BeautifulSoup(driver.page_source)
    trs = jsoup.find('tbody', attrs={'role':'rowgroup'}).find_all('tr')
    for tr in trs:
        try:
            Bank_Name = tr.find('a', attrs={'data-name': 'advertiserlink'})
            if Bank_Name is not None:
                Bank_Name = Bank_Name.text.strip().split('\n')

            elif tr.find('td', attrs={'class':'grid-cell size-4of12 rate-table-row__cell +pd-top no-logo'}) is not None:
                Bank_Name = tr.find('span', attrs={'class': '+text-size-md track +mg-bottom-xxs +display-block'}).text.strip().split('\n')
            elif tr.find('td', attrs={'class':'grid-cell size-4of12 rate-table-row__cell +pd-top'}) is not None:
                Bank_Name = tr.find('span', attrs={'class': '+text-size-md track +mg-bottom-xxs +display-block'}).text.strip().split('\n')

            if Bank_Name is None:
                continue
            apy = tr.find('a', attrs={'data-name':'advertiserAPY'})#div[1].text.split('%')[0]
            if apy is None:

                apy = tr.find_all('td')[1].find('span', attrs={'class':'numeral --beta +display-block +mg-bottom-xs'}).parent

                apy = apy.text.split()[0] if apy is not None else None
            apy = apy if apy is not None else None

            amount = tr.find_all('td')[2].find('span',attrs={'class':'numeral__accent --currency'}).parent
            amount = amount.text if amount is not None else None

            bank = Bank_Name

            if len(bank)>=2:
                bank_name = bank[0].strip()
                bank_product = bank[1].strip()
            else:
                bank_name = bank[0].strip()
                bank_product = None
            print([bank_name,bank_product, apy, amount.strip()])

            if bank_name in neededBanks:
                if bank_name in online_bank:
                    Bank_Offer_Feature = 'Online'
                else:
                    Bank_Offer_Feature = 'Offline'
                if bank_product is not None and '|' in bank_product:
                    bank_product = bank_product.split('|')[0].capitalize()

                a = [neededBanks[bank_name], 'Savings', 'Savings' if bank_product is None else bank_product, amount.strip(), Bank_Offer_Feature, None, 'Interest',apy.strip()]
                Excel_Table.append(a)
        except Exception as e:
            print(e)


except Exception as e:
    print(e)




##==============================================CDS===========================================================================================
try:
    driver.get("https://www.bankrate.com/cd.aspx")
    driver.find_element_by_xpath("//input[@name='location']").clear()
    driver.find_element_by_xpath("//input[@name='location']").send_keys(10004)
    # driver.find_element_by_xpath('//*[@id="csstyle"]/div[5]/div[1]/div[3]/div[4]/div/div[1]/div/div/input').clear()
    # driver.find_element_by_xpath('//*[@id="csstyle"]/div[5]/div[1]/div[3]/div[4]/div/div[1]/div/div/input').send_keys(10004)
    driver.find_element_by_tag_name('body').click()
    time.sleep(5)
    driver.find_element_by_css_selector('.tabs__link--all-products').click()
    time.sleep(5)

    for i in range(20):
        try:

            element = driver.find_element_by_css_selector('button.button:nth-child(4)')#/html/body/main/section/div/div[2]/button

            # element = driver.find_element_by_css_selector('button.button')#.click()
            driver.execute_script("arguments[0].click();", element)
            # print('element found')
            time.sleep(3)
        except Exception as e:
            print(e)
            break
    time.sleep(3)
    jsoup = BeautifulSoup(driver.page_source)
    trs = jsoup.find('table', attrs={'class': 'table --bordered-rows --spacing-xs rate-table rate-table-cd'}).find('tbody').find_all('tr')
    print('-------------------------')

    for tr in trs:
        try:
            tds = tr.find_all('td')
            Bank_name = tds[0].find('a', attrs={'data-name':'advertiserlink'})
            # print(Bank_name)
            if Bank_name is None:
                Bank_name = tds[0].find('span', attrs={'class':'+text-size-md track +mg-bottom-xxs +display-block'})
                # print(Bank_name)
            apy = tds[1].find('a', attrs={'data-name': 'advertiserAPY'})
            # print(apy)
            if apy is None:
                apy = tds[1].find('div', attrs={'class':'numeral --beta size-full'})
                # print(apy)
            amount = tds[3].find('div',attrs={'class':'numeral --beta'})
            if amount is None:
                amount = tds[3].find('div',attrs={'class':'numeral --beta size-full'})
            # print(amount)
            Bank_name = Bank_name.text if Bank_name is not None else None
            print(Bank_name)
            apy = apy.text if apy is not None else None
            # print(apy)
            amount = amount.text if amount is not None else None
            # print(amount)
            bank = Bank_name#.strip().split('\n')
            terms_in_month = tds[2].find('div', attrs={'class':'numeral --beta size-full'}).text
            # print(terms_in_month)

            # if len(bank)>=2:#csstyle > main > section > button
            #     bank_name = bank[0]
            #     bank_product = bank[1]
            # else:
            #     bank_name = bank[0]
            #     bank_product = None

            if bank in neededBanks:
                if bank in online_bank:
                    Bank_Offer_Feature= 'Online'
                else:
                    Bank_Offer_Feature = 'Offline'
                a = [neededBanks[bank], 'CD', 'CD', amount.strip() if amount is not None else None,
                     Bank_Offer_Feature, terms_in_month.strip() if terms_in_month is not None else None, 'Interest',
                     apy.strip() if apy is not None else None]
                Excel_Table.append(a)

        except Exception as e:
            print(e)

except Exception as e:
    print(e)

#=======================================Checkings==========================================================
try:

    driver.get("https://www.bankrate.com/banking/checking/rates/")
    time.sleep(15)
    driver.find_element_by_css_selector('.gearbox-input').clear()
    driver.find_element_by_css_selector('.gearbox-input').send_keys(10004)
    driver.find_element_by_tag_name('body').click()
    time.sleep(15)
    while True:
        try:
            element = driver.find_element_by_css_selector('.--secondary')#.click()
            driver.execute_script("arguments[0].click();", element)
            time.sleep(3)
        except Exception as e:
            print(e)
            break

    jsoup = BeautifulSoup(driver.page_source)
    trs = jsoup.find('div', attrs={'class':re.compile('table')}).find('tbody').find_all('tr')
    print(len(trs))
    for tr in trs:
        print('-'.center(100, '-'))
        div  = tr.find_all('div', attrs={'class':re.compile('grid-cell')})
        Bank_Name = div[0].find('div', attrs={'data-name':re.compile('advertiserlink')})
        if Bank_Name is not None:
            Bank_Name = Bank_Name.text.strip().split('\n')[0]
        elif div[0].find('div', attrs={'class':'rate-table__row-copy --dark-gray'}) is not None:
            Bank_Name = div[0].find('div', attrs={'class': 'rate-table__row-copy --dark-gray'}).text.strip().split('\n')[0]

        print(Bank_Name)
        # Bank_Name = ul.find('li', attrs={'class':'rtLender'}).find('a')
        # if Bank_Name is not None:
        #     Bank_Name = Bank_Name.text
        # else:
        #     Bank_Name = ul.find('li', attrs={'class': 'rtLender'}).find('div').text
        # print(Bank_Name)
        Apy = div[1].text.split('%')[0]
        print(Apy)
        #
        #
        if Bank_Name is None:
            continue
        if Bank_Name.strip() in neededBanks:
            if Bank_Name.strip() in online_bank:
                Bank_Offer_Feature = 'Online'
            else:
                Bank_Offer_Feature = 'Offline'
            a = [neededBanks[Bank_Name.strip()], 'Checking', 'Checking', None, Bank_Offer_Feature, None, None,
                 Apy.strip() if Apy is not None else None]
            print(a)
            Excel_Table.append(a)

except Exception as e:
    print(e)

try:
    #Close the drive
    driver.close()
except Exception as e:
    print(e)

# #--------------------------------------Moving Data to CSV File using Pandas----------------------------------
# #Arrange all fileds based on required format
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term_in_Months", "Interest_Type", "Interest", "APY", "Source"]
print(tabulate(Excel_Table))

# #Formating Years into Months
def getMonths(x):
    if x is not None:
        if 'm' in x.lower():
            return re.sub('[^0-9.]','',x)
        elif 'y' in x.lower():
            y = re.sub('[^0-9.]', '', x)
            return int(y.split('.')[0]) * 12 + int(y.split('.')[1]) if '.' in y else int(y)*12
        else:
            return x

df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Interest'] = np.nan
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Interest_Type'] = 'Fixed'
df['Bank_Product_Code'] = np.nan
df['Balance'] = df['Balance'].apply(lambda x:re.sub('[^0-9,.]','',x) if x is not None else None)
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(lambda x:re.sub('[^0-9A-Za-z|]','',x) if x is not None else x)
df['Source'] = 'Bankrate.com'
df['Term_in_Months'] = df['Term_in_Months'].apply(getMonths)
df = df[order]
df.to_csv(path, index=False) #Moving data to csv File

print('Total Execution Time:',time.time()-start_time,' Seconds') #Display total time taken to Execute the program
print('Execution Completed.')