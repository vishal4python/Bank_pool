from selenium import webdriver
import re
from tabulate import tabulate
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import datetime
import time
from maks_lib import output_path

print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()
Excel_Data = []

#Csv file Location
path = output_path+'Consolidate_CITI_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'

#Create a selenium Driver.
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
driver.maximize_window()
print('Browser Loaded')

#Required Fields for scraping the data
table_headers = ['Bank_Product_Name','Product_Interest','Mortgage_Apr',"Mortgage_Loan","Product_Term","Balance"]
Excel_Data.append(table_headers)

#Three cases to scrap the data.
cases = [[125000,100000], [375000, 300000], [625000, 500000]]
for case in cases:
    try:
        filter_list = []
        #Getting pageSource by using Selenium Module.
        driver.get('https://online.citi.com/US/nccmi/purchase/ratequote/flow.action?fromLanding=true&selectedOption=CUSTOM&selectedOptionValue=CUSTOMpurChaseLanding&JFP_TOKEN=3GBHQLZG')
        driver.find_element_by_xpath('//*[@id="propertyUse"]/option[2]').click()
        driver.find_element_by_tag_name('body').click()
        driver.find_element_by_xpath('//*[@id="propCity"]').click()
        driver.find_element_by_xpath('//*[@id="propCity"]').send_keys('New York')
        driver.find_element_by_tag_name('body').click()
        driver.find_element_by_xpath('//*[@id="propState"]/option[34]').click()
        driver.find_element_by_tag_name('body').click()
        driver.find_element_by_xpath('//*[@id="propCounty"]/option[32]').click()
        driver.find_element_by_tag_name('body').click()
        driver.find_element_by_xpath('//*[@id="purchPrice"]').clear()
        driver.find_element_by_xpath('//*[@id="purchPrice"]').send_keys(case[0])
        driver.find_element_by_tag_name('body').click()
        driver.find_element_by_xpath('//*[@id="desiredLoanAmount"]').send_keys(case[1])
        driver.find_element_by_tag_name('body').click()
        driver.find_element_by_xpath('//*[@id="purchaseQuestionsForm"]/div[6]/div[2]/fieldset/div/div[2]/div').click()
        driver.find_element_by_tag_name('body').click()
        driver.find_element_by_xpath('//*[@id="submit-purchase"]').click()
        time.sleep(60)

        #Getting Required Data by using BeautifulSoup Moule
        jsoup = BeautifulSoup(driver.page_source).find('div', attrs={'id':'FeaturedProducts-container'})
        if jsoup is not None:
            for div in jsoup.find_all('div', attrs={'class':'rate-card-panel'}):
                try:
                    product_name = div.find('h1').text
                    text = div.text.replace('\n', ' ').strip()

                    rate = re.search('rate \d\.[0-9]*%',text,re.IGNORECASE)
                    rate = re.search('\d\.[0-9]*%', rate.group(0), re.IGNORECASE).group(0) if rate is not None else None

                    apr = re.search('apr \d\.[0-9]*%',text,re.IGNORECASE)
                    apr = re.search('\d\.[0-9]*%', apr.group(0), re.IGNORECASE).group(0) if apr is not  None else None

                    Amount = re.search('amount \$\d[0-9,\.]* ',text,re.IGNORECASE)
                    Amount = re.search('\$\d[0-9,\.]* ', Amount.group(0), re.IGNORECASE).group(0) if Amount is not  None else None

                    Product_Term = re.search('[0-9]* Year',product_name,re.IGNORECASE)
                    Product_Term = re.search('[0-9]*', Product_Term.group(0)).group(0)if Product_Term is not None else 30

                    a = [product_name, rate, apr, case[1], Product_Term,Amount]
                    filter_list.append(a)

                except Exception as e:
                    print(e)
        else:
            print('data not found')

        b_set = set(map(tuple,filter_list))
        filter_list = map(list,b_set)
        for k in filter_list:
            Excel_Data.append(k)

    except Exception as e:
        print(e)
try:
    driver.close()
except Exception as e:
    print(e)

print(tabulate(Excel_Data))

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
#Arrange all fileds based on required format
order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name",
         "Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage","Mortgage_Apr"]
df = pd.DataFrame(Excel_Data[1:], columns=table_headers)
df['Date'] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'CITIGROUP INC'
df['Bank_Product'] = 'Mortgage'
df['Bank_Product_Type'] = 'Mortgage'
df['Bank_Offer_Feature'] = 'Offline'
df['Mortgage_Down_Payment'] = '20%'
df['Min_Credit_Score_Mortagage'] = '720+'
df['Product_Apy'] = None
df = df[order]
df.to_csv(path, index=False) #Moving Data to Csv File.


print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')