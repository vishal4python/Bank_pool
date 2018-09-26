import requests
from  tabulate import tabulate
import pandas as pd
import re
import time
import datetime
from maks_lib import output_path

print('Program Execution Started..')
starttime = time.time()
today = datetime.datetime.now()

#Csv file location to store the scraped data.
path = output_path+'Consolidate_BOA_Data_Mortgage_v2_'+today.strftime('%m_%d_%Y')+'.csv'


#Required fields for scraping the data
table_headers = ['Bank_Product_Name','Product_Interest','Mortgage_Apr',"Mortgage_Loan","Product_Term","Balance"]
Excel_Table = []

#Three cases for scraping the data
cases = [[125000, 25000], [375000, 75000], [625000, 125000]]
for case in cases:
    #Geeting json data by passing url and data through post method in requests module
    response = requests.post('https://www.bankofamerica.com/home-loans-sales/getProductRates',json={"rateInputs":{"purchasePrice":case[0],"amountBorrowed":100000,"postalCode":"10004","ficoScore":740,"lockPeriod":45,"financeType":1,"branchCode":"3018","loantoValueRatio":"80","downPayment":case[1]},"mortgageProducts":[{"productCode":3,"productName":"Fixed 30 Years","productSubCode":"360"},{"productCode":2,"productName":"Fixed 20 Years","productSubCode":"240"},{"productCode":1,"productName":"Fixed 15 Years","productSubCode":"180"},{"productCode":561,"productName":"ARM Fixed First 10 Years, Then Adjusts Yearly","productSubCode":"360"},{"productCode":558,"productName":"ARM Fixed First 7 Years, Then Adjusts Yearly","productSubCode":"360"},{"productCode":555,"productName":"ARM Fixed First 5 Years, Then Adjusts Yearly","productSubCode":"360"}]}).json()
    for data in response['mortgageProducts']:
        if 'Adjusts Yearly' in data['productName']:
            product_name1 = re.search('[0-9]* Years',data['productName'])[0]
            product_name = re.sub('[^0-9]','',product_name1) +'/1 ARM variable'
        else:
            product_name = data['productName']

        if 'variable' in product_name:
            product_term = '30'
        else:
            product_term = re.search('[0-9]* Years',product_name)
            product_term = re.sub('[^0-9]','', product_term.group(0)) if product_term is not None else None

        interest =  str(round(data['rateDetails']['rate'], 3)) +'%'
        apr = str(round(data['rateDetails']['apr'], 3)) +'%'
        mortgage_amt = case[0]-case[1]
        a = [product_name, interest,apr,mortgage_amt, product_term, None]
        Excel_Table.append(a)



#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
#Arrange all fileds based on required format
order = ["Date", "Bank_Name", "Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name",
         "Product_Term", "Balance", "Product_Interest", "Product_Apy", "Mortgage_Down_Payment", "Mortgage_Loan",
         "Min_Credit_Score_Mortagage", "Mortgage_Apr"]
df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Date'] = ' ' + today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'BANK OF AMERICA CORP'
df['Bank_Product'] = 'Mortgage'
df['Bank_Product_Type'] = 'Mortgage'
df['Bank_Offer_Feature'] = 'Offline'
df['Mortgage_Down_Payment'] = '20%'
df['Min_Credit_Score_Mortagage'] = '740+'
df['Product_Apy'] = None
df = df[order]
df.to_csv(path, index=False) #Moving data to csv.

print(tabulate(Excel_Table))
print('Total Execution Time is ', (time.time() - starttime), 'Seconds') #Display Execution time of the program
print('Program Execution Completed')