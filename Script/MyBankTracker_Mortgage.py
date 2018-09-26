import requests
from tabulate import tabulate
import pandas as pd
Excel_Table = []
import datetime
import  time
from maks_lib import output_path
print('Program Execution Started...')
start_time = time.time()
today = datetime.datetime.now()

#Csv file Location
path = output_path+'Aggregator_mybanktracker_Data_US_Mortgage_'+today.strftime('%m-%d-%Y')+'.csv'

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

#Required Fields for scraping the data
table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest', 'APR', 'Mortgage_Loan_Amt', 'Mortgage_Down_Payment']
Excel_Table.append(table_headers)
cases = [100000, 300000, 500000]
terms = [[1,'30 Year Fixed', 'Fixed',30],[25,'20 Year Fixed', 'Fixed',20],[2,'15 Year Fixed', 'Fixed',15],[3,'10 Year Fixed', 'Fixed',30],[5,'7/1 ARM','Variable',30],[6,'5/1 ARM','Variable',30],[7,'3/1 ARM','Variable',30]]
for case in cases:
    for term in terms:
        print([case,term])
        try:
            # Getting API data by using requests module
            resp = requests.get('https://www.mybanktracker.com/mbt_media_analytics/mortgage_products.json?ad_unit=rate_table&amount='+str(case)+'&points=0-0&state=NY&term='+str(term[0])).json()
            for k in resp:
                Bank_Name = k['company']['name']
                APR = k['mortgage_product_rates'][0]['apr']* 100
                Interest = k['mortgage_product_rates'][0]['rate'] * 100
                if Bank_Name.lower().strip() in neededUsBanks:
                    a = [neededUsBanks[Bank_Name.lower().strip()], term[1], None, 'Offline', term[3], term[2], str(Interest)+'%', str(APR)+'%', case, '20%']
                    Excel_Table.append(a)
        except Exception as e:
            print(e)
print(tabulate(Excel_Table))

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
df = pd.DataFrame(Excel_Table[1:],columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df['Bank_Type'] ='Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Product_Code'] = None
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Source'] = 'mybanktracker.com'


#Arrange all fileds based on required format
order = ["Date", "Bank_Native_Country", "State", "Bank_Name","Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APR", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Source"]
df = df[order]
df.to_csv(path, index=False)    #Moving data to CSV File.


print('Total Execution Time is ',(time.time()-start_time),'Seconds') #Display total execution time.
print('Execution Completed.')