import requests
from tabulate import tabulate
import pandas as pd
import datetime
import time
from maks_lib import output_path


print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()
Excel_Table = []

#Csv file Location
path = output_path+'Aggregator_mybanktracker_Data_US_Deposit_'+today.strftime('%m-%d-%Y')+'.csv'

#Required Fields for scraping the data
table_headers = ['Bank_Name', 'Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term_in_Months', 'Interest', 'APY']
Excel_Table.append(table_headers)

#Filternig Required Bank Names by using neededUsBanks
neededUsBanks = {
    "ally bank":'ALLY',
    "bank of america":"BANK OF AMERICA CORP",
    "capital one":"CAPITAL ONE",
    "capital one 360":"CAPITAL ONE",
    "chase":"JP MORGAN CHASE & Co.",
    "citibank":"CITIGROUP INC",
    "pnc":"PNC FINANCIAL SERVICES GROUP INC",
    "pnc bank":"PNC FINANCIAL SERVICES GROUP INC",
    "synchrony bank":"SYNCHRONY",
    "wells fargo":"WELLS FARGO",
    "suntrust":"SUNTRUST BANKS INC"

}

#Making Bank_Offer_Feature Online or Offline based on online_banks
online_bank = [k.lower() for k in ['Synchrony Bank', 'Ally Bank', 'Capital One 360']]

#================================Savings============================================
urls = [['Savings','https://www.mybanktracker.com/mbt_media_analytics/placements?slug=rate_table-savings-organic'], ['Checking','https://www.mybanktracker.com/mbt_media_analytics/placements?slug=rate_table-checking-organic'],
        ['CD','https://www.mybanktracker.com/mbt_media_analytics/placements?slug=rate_table-cd-organic']]

for url in urls:
    #Getting API data by using requests module
    resp = requests.get(url[1]).json()
    products = resp['products']
    for product in products:
        try:
            Bank_Name = product['company']['name']
            Bank_Product_Name = product['meta']['name']
            Bank_Offer_Feature = 'Online' if 'online' in Bank_Product_Name.lower() else 'Offline'
            Bank_Offer_Feature = 'Online' if Bank_Name.lower().strip() in online_bank else 'Offline'
            if url[0] == 'CD':
                years = [6, 12, 36]
                for cd in product['rate_tiers']:
                    year = cd['term_in_months']
                    if year in years:
                        if Bank_Name.lower().strip() in neededUsBanks:
                            a = [neededUsBanks[Bank_Name.lower().strip()], url[0], Bank_Product_Name, int(cd['min_amount']), Bank_Offer_Feature, year, None,str(cd['rate']*100)+'%']
                            Excel_Table.append(a)

            else:
                Term = None
                if Bank_Name.lower().strip() in neededUsBanks:
                    for k in product['rate_tiers']:
                        a = [neededUsBanks[Bank_Name.lower().strip()],  url[0], Bank_Product_Name, int(k['min_amount']), Bank_Offer_Feature, Term, None, str(k['rate']*100)+'%']
                        Excel_Table.append(a)
        except Exception as e:
            print(e)

print(tabulate(Excel_Table))

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
df = pd.DataFrame(Excel_Table[1:], columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Product_Code'] = None
df['Interest_Type'] = 'Fixed'
df['Source'] = 'mybanktracker.com'

#Arrange all fileds based on required format
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term_in_Months", "Interest_Type", "Interest", "APY", "Source"]
df = df[order]
df.to_csv(path, index=False)    #Moving data to CSV File.


print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')