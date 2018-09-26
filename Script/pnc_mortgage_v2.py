import requests
from tabulate import tabulate
import pandas as pd
import time
import datetime
start_time = time.time()
today = datetime.datetime.now()
from maks_lib import output_path

#CSV File Location
path = output_path+'Consolidate_PNC_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'

Excel_Table = []

#Required Fields for scraping the data
table_headers = ["Bank_Product_Name", "Mortgage_Loan", "Product_Term", "Product_Interest", "Mortgage_Apr"]
Excel_Table.append(table_headers)

#Post Data for https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/FHA-Loan.html
fhaData = {"appType":"purchase","amount":100000,"zipCode":10004,"f1pp":23,"f1pn":"","f1pu":"","f1ap":38,"f1an":"FHA%2B30%2BYR%2BFIXED",
           "f1au":"","f2pp":22,"f2pn":"","f2pu":"","f2ap":270,"f2an":"FHA%2B5-1%2BARM","f2au":"","f3pp":"","f3pn":"","f3pu":"","f3ap":"",
           "f3an":"","f3au":"","f4pp":"","f4pn":"","f4pu":"","f4ap":"","f4an":"","f4au":"","fDM":"%253Cp%2Bstyle%253D%2522font-size%253A80%2525%253B%2522%253EYour%2Bactual%2Binterest%2Brate%2Bwill%2Bdepend%2Bon%2Byour%2Bown%2Bfinancial%2Bsituation%252C%2Bproperty%2Btype%252C%2Bhousing%2Bmarket%2Band%2Bother%2Bfactors.%253C%252Fp%253E%250A%250A%253Cp%2Bstyle%253D%2522font-size%253A80%2525%253B%2522%253E%253Cstrong%253ENotice%2BRegarding%2BAdjustable%2BRate%2BMortagages%253A%253C%252Fstrong%253E%2BInterest%2Bis%2Bfixed%2Bfor%2Ba%2Bset%2Bperiod%2Bof%2Btime%252C%2Band%2Badjusts%2Bperiodically%2Bthereafter.%2BAt%2Bthe%2Bend%2Bof%2Bthe%2Bfixed%2Brate%2Bperiod%252C%2Bthe%2Binterest%2Band%2Bmonthly%2Bpayments%2Bmay%2Bincrease.%2B%253C%252Fp%253E%250A%250A%253C%2521--FHA%2BRate%2BModule--%253E",
           "o1H":"","o1D":False,"o1c1pp":"","o1c1pn":"","o1c1pu":"","o1c1ap":"","o1c1an":"","o1c1au":"","o1c2pp":"","o1c2pn":"","o1c2pu":"",
           "o1c2ap":"","o1c2an":"","o1c2au":"","o1c3pp":"","o1c3pn":"","o1c3pu":"","o1c3ap":"","o1c3an":"","o1c3au":"","o1c4pp":"","o1c4pn":"","o1c4pu":"",
           "o1c4ap":"","o1c4an":"","o1c4au":"","o1UA":False,"o1AM":"","o1DM":"","o2H":"","o2D":False,"o2c1pp":"","o2c1pn":"","o2c1pu":"",
           "o2c1ap":"","o2c1an":"","o2c1au":"","o2c2pp":"","o2c2pn":"","o2c2pu":"","o2c2ap":"","o2c2an":"","o2c2au":"","o2c3pp":"","o2c3pn":"",
           "o2c3pu":"","o2c3ap":"","o2c3an":"","o2c3au":"","o2c4pp":"","o2c4pn":"","o2c4pu":"","o2c4ap":"","o2c4an":"","o2c4au":"","o2UA":False,"o2AM":"",
           "o2DM":"","o3H":"","o3D":False,"o3c1pp":"","o3c1pn":"","o3c1pu":"","o3c1ap":"","o3c1an":"","o3c1au":"","o3c2pp":"","o3c2pn":"","o3c2pu":"","o3c2ap":"",
           "o3c2an":"","o3c2au":"","o3c3pp":"","o3c3pn":"","o3c3pu":"","o3c3ap":"","o3c3an":"","o3c3au":"","o3c4pp":"","o3c4pn":"","o3c4pu":"","o3c4ap":"","o3c4an":"",
           "o3c4au":"","o3UA":False,"o3AM":"","o3DM":"","o4H":"","o4D":False,"o4c1pp":"","o4c1pn":"","o4c1pu":"","o4c1ap":"","o4c1an":"","o4c1au":"","o4c2pp":"",
           "o4c2pn":"","o4c2pu":"","o4c2ap":"","o4c2an":"","o4c2au":"","o4c3pp":"","o4c3pn":"","o4c3pu":"","o4c3ap":"","o4c3an":"","o4c3au":"","o4c4pp":"","o4c4pn":"",
           "o4c4pu":"","o4c4ap":"","o4c4an":"","o4c4au":"","o4UA":False,"o4AM":"","o4DM":"","o5H":"","o5D":False,"o5c1pp":"","o5c1pn":"","o5c1pu":"","o5c1ap":"",
           "o5c1an":"","o5c1au":"","o5c2pp":"","o5c2pn":"","o5c2pu":"","o5c2ap":"","o5c2an":"","o5c2au":"","o5c3pp":"","o5c3pn":"","o5c3pu":"","o5c3ap":"",
           "o5c3an":"","o5c3au":"","o5c4pp":"","o5c4pn":"","o5c4pu":"","o5c4ap":"","o5c4an":"","o5c4au":"","o5UA":False,"o5AM":"","o5DM":"","o6H":"",
           "o6D":False,"o6c1pp":"","o6c1pn":"","o6c1pu":"","o6c1ap":"","o6c1an":"","o6c1au":"","o6c2pp":"","o6c2pn":"","o6c2pu":"","o6c2ap":"","o6c2an":"","o6c2au":"",
           "o6c3pp":"","o6c3pn":"","o6c3pu":"","o6c3ap":"","o6c3an":"","o6c3au":"","o6c4pp":"","o6c4pn":"","o6c4pu":"","o6c4ap":"","o6c6an":"","o6c4au":"","o6UA":False,
           "o6AM":"","o6DM":""
           }

#Post data for https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/VA-Loan.html
vaLoanData = {"appType":"purchase","amount":100000,"zipCode":10004,"f1pp":26,"f1pn":"","f1pu":"","f1ap":1338,"f1an":"VA%2B30%2BYR%2BFIXED",
              "f1au":"","f2pp":25,"f2pn":"","f2pu":"","f2ap":1669,"f2an":"VA%2B5-1%2BARM","f2au":"","f3pp":"","f3pn":"","f3pu":"","f3ap":"","f3an":"",
              "f3au":"","f4pp":"","f4pn":"","f4pu":"","f4ap":"","f4an":"","f4au":"","fDM":"%253Cp%2Bstyle%253D%2522font-size%253A80%2525%253B%2522%253EYour%2Bactual%2Binterest%2Brate%2Bwill%2Bdepend%2Bon%2Byour%2Bown%2Bfinancial%2Bsituation%252C%2Bproperty%2Btype%252C%2Bhousing%2Bmarket%2Band%2Bother%2Bfactors.%253C%252Fp%253E%250A%250A%253Cp%2Bstyle%253D%2522font-size%253A80%2525%253B%2522%253E%253Cstrong%253ENotice%2BRegarding%2BAdjustable%2BRate%2BMortagages%253A%253C%252Fstrong%253E%2BInterest%2Bis%2Bfixed%2Bfor%2Ba%2Bset%2Bperiod%2Bof%2Btime%252C%2Band%2Badjusts%2Bperiodically%2Bthereafter.%2BAt%2Bthe%2Bend%2Bof%2Bthe%2Bfixed%2Brate%2Bperiod%252C%2Bthe%2Binterest%2Band%2Bmonthly%2Bpayments%2Bmay%2Bincrease.%2B%253C%252Fp%253E%250A%250A%253C%2521--VA%2BLoan%2BModule--%253E",
              "o1H":"","o1D":False,"o1c1pp":"","o1c1pn":"","o1c1pu":"","o1c1ap":"","o1c1an":"","o1c1au":"","o1c2pp":"","o1c2pn":"","o1c2pu":"","o1c2ap":"","o1c2an":"",
              "o1c2au":"","o1c3pp":"","o1c3pn":"","o1c3pu":"","o1c3ap":"","o1c3an":"","o1c3au":"","o1c4pp":"","o1c4pn":"","o1c4pu":"","o1c4ap":"","o1c4an":"",
              "o1c4au":"","o1UA":False,"o1AM":"","o1DM":"","o2H":"","o2D":False,"o2c1pp":"","o2c1pn":"","o2c1pu":"","o2c1ap":"","o2c1an":"","o2c1au":"",
              "o2c2pp":"","o2c2pn":"","o2c2pu":"","o2c2ap":"","o2c2an":"","o2c2au":"","o2c3pp":"","o2c3pn":"","o2c3pu":"","o2c3ap":"","o2c3an":"","o2c3au":"","o2c4pp":"",
              "o2c4pn":"","o2c4pu":"","o2c4ap":"","o2c4an":"","o2c4au":"","o2UA":False,"o2AM":"","o2DM":"","o3H":"","o3D":False,"o3c1pp":"","o3c1pn":"","o3c1pu":"",
              "o3c1ap":"","o3c1an":"","o3c1au":"","o3c2pp":"","o3c2pn":"","o3c2pu":"","o3c2ap":"","o3c2an":"","o3c2au":"","o3c3pp":"","o3c3pn":"","o3c3pu":"","o3c3ap":"",
              "o3c3an":"","o3c3au":"","o3c4pp":"","o3c4pn":"","o3c4pu":"","o3c4ap":"","o3c4an":"","o3c4au":"","o3UA":False,"o3AM":"","o3DM":"","o4H":"","o4D":False,
              "o4c1pp":"","o4c1pn":"","o4c1pu":"","o4c1ap":"","o4c1an":"","o4c1au":"","o4c2pp":"","o4c2pn":"","o4c2pu":"","o4c2ap":"","o4c2an":"","o4c2au":"","o4c3pp":"",
              "o4c3pn":"","o4c3pu":"","o4c3ap":"","o4c3an":"","o4c3au":"","o4c4pp":"","o4c4pn":"","o4c4pu":"","o4c4ap":"","o4c4an":"","o4c4au":"","o4UA":False,"o4AM":"",
              "o4DM":"","o5H":"","o5D":False,"o5c1pp":"","o5c1pn":"","o5c1pu":"","o5c1ap":"","o5c1an":"","o5c1au":"","o5c2pp":"","o5c2pn":"","o5c2pu":"","o5c2ap":"",
              "o5c2an":"","o5c2au":"","o5c3pp":"","o5c3pn":"","o5c3pu":"","o5c3ap":"","o5c3an":"","o5c3au":"","o5c4pp":"","o5c4pn":"","o5c4pu":"","o5c4ap":"","o5c4an":"",
              "o5c4au":"","o5UA":False,"o5AM":"","o5DM":"","o6H":"","o6D":False,"o6c1pp":"","o6c1pn":"","o6c1pu":"","o6c1ap":"","o6c1an":"","o6c1au":"","o6c2pp":"",
              "o6c2pn":"","o6c2pu":"","o6c2ap":"","o6c2an":"","o6c2au":"","o6c3pp":"","o6c3pn":"","o6c3pu":"","o6c3ap":"","o6c3an":"","o6c3au":"","o6c4pp":"","o6c4pn":"",
              "o6c4pu":"","o6c4ap":"","o6c6an":"","o6c4au":"","o6UA":False,"o6AM":"","o6DM":""
              }

#Post data for https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/adjustable-mortgage.html
adjustableData = {"appType":"purchase","amount":100000,"zipCode":10004,"f1pp":132,"f1pn":"","f1pu":"","f1ap":139,"f1an":"5-1+YR+ARM",
                  "f1au":"%2Fcontent%2Fpnc-com%2Fen%2Fpersonal-banking%2Fborrowing%2Fhome-lending%2Fmortgages%2Fjumbo-loan.html",
                  "f2pp":133,"f2pn":"","f2pu":"","f2ap":140,"f2an":"7-1+YR+ARM","f2au":"%2Fcontent%2Fpnc-com%2Fen%2Fpersonal-banking%2Fborrowing%2Fhome-lending%2Fmortgages%2Fjumbo-loan.html",
                  "f3pp":134,"f3pn":"","f3pu":"","f3ap":141,"f3an":"10-1+YR+ARM","f3au":"%2Fcontent%2Fpnc-com%2Fen%2Fpersonal-banking%2Fborrowing%2Fhome-lending%2Fmortgages%2Fjumbo-loan.html",
                  "f4pp":135,"f4pn":"","f4pu":"","f4ap":"","f4an":"","f4au":"","fDM":"%3Cp+style%3D%22font-size%3A80%25%3B%22%3EYour+actual+interest+rate+will+depend+on+your+own+financial+situation%2C+property+type%2C+housing+market+and+other+factors.%3C%2Fp%3E%0A%0A%3Cp+style%3D%22font-size%3A80%25%3B%22%3E%3Cstrong%3ENotice+Regarding+Adjustable+Rate+Mortagages%3A%3C%2Fstrong%3E+Interest+is+fixed+for+a+set+period+of+time%2C+and+adjusts+periodically+thereafter.+At+the+end+of+the+fixed+rate+period%2C+the+interest+and+monthly+payments+may+increase.+%3C%2Fp%3E%0A%0A%3C%21--Adjustable+Rate+Module--%3E",
                  "o1H":"","o1D":False,"o1c1pp":"","o1c1pn":"","o1c1pu":"","o1c1ap":"","o1c1an":"","o1c1au":"","o1c2pp":"","o1c2pn":"","o1c2pu":"","o1c2ap":"",
                  "o1c2an":"","o1c2au":"","o1c3pp":"","o1c3pn":"","o1c3pu":"","o1c3ap":"","o1c3an":"","o1c3au":"","o1c4pp":"","o1c4pn":"","o1c4pu":"","o1c4ap":"",
                  "o1c4an":"","o1c4au":"","o1UA":False,"o1AM":"","o1DM":"","o2H":"","o2D":False,"o2c1pp":"","o2c1pn":"","o2c1pu":"","o2c1ap":"","o2c1an":"","o2c1au":"",
                  "o2c2pp":"","o2c2pn":"","o2c2pu":"","o2c2ap":"","o2c2an":"","o2c2au":"","o2c3pp":"","o2c3pn":"","o2c3pu":"","o2c3ap":"","o2c3an":"","o2c3au":"","o2c4pp":"",
                  "o2c4pn":"","o2c4pu":"","o2c4ap":"","o2c4an":"","o2c4au":"","o2UA":False,"o2AM":"","o2DM":"","o3H":"","o3D":False,"o3c1pp":"","o3c1pn":"","o3c1pu":"",
                  "o3c1ap":"","o3c1an":"","o3c1au":"","o3c2pp":"","o3c2pn":"","o3c2pu":"","o3c2ap":"","o3c2an":"","o3c2au":"","o3c3pp":"","o3c3pn":"","o3c3pu":"","o3c3ap":"",
                  "o3c3an":"","o3c3au":"","o3c4pp":"","o3c4pn":"","o3c4pu":"","o3c4ap":"","o3c4an":"","o3c4au":"","o3UA":False,"o3AM":"","o3DM":"","o4H":"",
                  "o4D":False,"o4c1pp":"","o4c1pn":"","o4c1pu":"","o4c1ap":"","o4c1an":"","o4c1au":"","o4c2pp":"","o4c2pn":"","o4c2pu":"","o4c2ap":"","o4c2an":"",
                  "o4c2au":"","o4c3pp":"","o4c3pn":"","o4c3pu":"","o4c3ap":"","o4c3an":"","o4c3au":"","o4c4pp":"","o4c4pn":"",
                  "o4c4pu":"","o4c4ap":"","o4c4an":"","o4c4au":"","o4UA":False,"o4AM":"","o4DM":"","o5H":"","o5D":False,"o5c1pp":"","o5c1pn":"",
                  "o5c1pu":"","o5c1ap":"","o5c1an":"","o5c1au":"","o5c2pp":"","o5c2pn":"","o5c2pu":"","o5c2ap":"","o5c2an":"","o5c2au":"","o5c3pp":"","o5c3pn":"",
                  "o5c3pu":"","o5c3ap":"","o5c3an":"","o5c3au":"","o5c4pp":"","o5c4pn":"","o5c4pu":"","o5c4ap":"","o5c4an":"","o5c4au":"","o5UA":False,"o5AM":"","o5DM":"",
                  "o6H":"","o6D":False,"o6c1pp":"","o6c1pn":"","o6c1pu":"","o6c1ap":"","o6c1an":"","o6c1au":"","o6c2pp":"","o6c2pn":"","o6c2pu":"","o6c2ap":"","o6c2an":"",
                  "o6c2au":"","o6c3pp":"","o6c3pn":"","o6c3pu":"","o6c3ap":"","o6c3an":"","o6c3au":"","o6c4pp":"","o6c4pn":"","o6c4pu":"","o6c4ap":"","o6c6an":"","o6c4au":"",
                  "o6UA":False,"o6AM":"","o6DM":""
                  }

#Post data for https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/fixed-rate-mortgage.html
frdata = {"appType":"purchase","amount":100000,"zipCode":10004,
            "f1pp":4,"f1pn":'',"f1pu":'',"f1ap":15,"f1an":"30+YR+FIXED",
            "f1au":"%2Fcontent%2Fpnc-com%2Fen%2Fpersonal-banking%2Fborrowing%2Fhome-lending%2Fmortgages%2Fjumbo-loan",
            "f2pp":3,"f2pn":'',"f2pu":'',"f2ap":13,"f2an":'15+YR+FIXED',"f2au":'%2Fcontent%2Fpnc-com%2Fen%2Fpersonal-banking%2Fborrowing%2Fhome-lending%2Fmortgages%2Fjumbo-loan',
            "f3pp":2,"f3pn":'',"f3pu":'',"f3ap":'',"f3an":'',"f3au":'',
            "f4pp":1,"f4pn":'',"f4pu":'',"f4ap":'',"f4an":"10+YR+FIXED","f4au":'',
            "fDM":"%3Cp+style%3D%22font-size%3A80%25%3B%22%3EYour+actual+interest+rate+will+depend+on+your+own+financial+situation%2C+property+type%2C+housing+market+and+other+factors.%3C%2Fp%3E%0A%0A%3Cp+style%3D%22font-size%3A80%25%3B%22%3E%3Cstrong%3ENotice+Regarding+Adjustable+Rate+Mortagages%3A%3C%2Fstrong%3E+Interest+is+fixed+for+a+set+period+of+time%2C+and+adjusts+periodically+thereafter.+At+the+end+of+the+fixed+rate+period%2C+the+interest+and+monthly+payments+may+increase.+%3C%2Fp%3E%0A%0A%0A%3C%21--Fixed+Rate+Module--%3E",
            "o1H":'',"o1D":False,"o1c1pp":'',"o1c1pn":'',"o1c1pu":'',"o1c1ap":'',"o1c1an":'',"o1c1au":'',"o1c2pp":'',"o1c2pn":'',
            "o1c2pu":'',"o1c2ap":'',"o1c2an":'',"o1c2au":'',"o1c3pp":'',"o1c3pn":'',"o1c3pu":'',"o1c3ap":'',"o1c3an":'',"o1c3au":'',
            "o1c4pp":'',"o1c4pn":'',"o1c4pu":'',"o1c4ap":'',"o1c4an":'',"o1c4au":'',"o1UA":False,"o1AM":'',"o1DM":'',"o2H":'',"o2D":False,"o2c1pp":'',
            "o2c1pn":'',"o2c1pu":'',"o2c1ap":'',"o2c1an":'',"o2c1au":'',"o2c2pp":'',"o2c2pn":'',"o2c2pu":'',"o2c2ap":'',"o2c2an":'',"o2c2au":'',"o2c3pp":'',
            "o2c3pn":'',"o2c3pu":'',"o2c3ap":'',"o2c3an":'',"o2c3au":'',"o2c4pp":'',"o2c4pn":'',"o2c4pu":'',"o2c4ap":'',"o2c4an":'',"o2c4au":'',"o2UA":False,"o2AM":'',
            "o2DM":'',"o3H":'',"o3D":False,"o3c1pp":'',"o3c1pn":'',"o3c1pu":'',"o3c1ap":'',"o3c1an":'',"o3c1au":'',"o3c2pp":'',"o3c2pn":'',"o3c2pu":'',"o3c2ap":'',
            "o3c2an":'',"o3c2au":'',"o3c3pp":'',"o3c3pn":'',"o3c3pu":'',"o3c3ap":'',"o3c3an":'',"o3c3au":'',"o3c4pp":'',"o3c4pn":'',"o3c4pu":'',"o3c4ap":'',"o3c4an":'',
            "o3c4au":'',"o3UA":False,"o3AM":'',"o3DM":'',"o4H":'',"o4D":False,"o4c1pp":'',"o4c1pn":'',"o4c1pu":'',"o4c1ap":'',"o4c1an":'',"o4c1au":'',"o4c2pp":'',"o4c2pn":'',
            "o4c2pu":'',"o4c2ap":'',"o4c2an":'',"o4c2au":'',"o4c3pp":'',"o4c3pn":'',"o4c3pu":'',"o4c3ap":'',"o4c3an":'',"o4c3au":'',"o4c4pp":'',"o4c4pn":'',"o4c4pu":'',
            "o4c4ap":'',"o4c4an":'',"o4c4au":'',"o4UA":False,"o4AM":'',"o4DM":'',"o5H":'',"o5D":False,"o5c1pp":'',"o5c1pn":'',"o5c1pu":'',"o5c1ap":'',"o5c1an":'',"o5c1au":'',
            "o5c2pp":'',"o5c2pn":'',"o5c2pu":'',"o5c2ap":'',"o5c2an":'',"o5c2au":'',"o5c3pp":'',"o5c3pn":'',"o5c3pu":'',"o5c3ap":'',"o5c3an":'',"o5c3au":'',"o5c4pp":'',
            "o5c4pn":'',"o5c4pu":'',"o5c4ap":'',"o5c4an":'',"o5c4au":'',"o5UA":False,"o5AM":'',"o5DM":'',"o6H":'',"o6D":False,"o6c1pp":'',"o6c1pn":'',"o6c1pu":'',"o6c1ap":'',
            "o6c1an":'',"o6c1au":'',"o6c2pp":'',"o6c2pn":'',"o6c2pu":'',"o6c2ap":'',"o6c2an":'',"o6c2au":'',"o6c3pp":'',"o6c3pn":'',"o6c3pu":'',"o6c3ap":'',"o6c3an":'',
            "o6c3au":'',"o6c4pp":'',"o6c4pn":'',"o6c4pu":'',"o6c4ap":'',"o6c6an":'',"o6c4au":'',"o6UA":False,"o6AM":'',"o6DM":''
            }
loans = [[100000, 10004],[300000, 10004],[500000, 10004]]
dummDict = dict()
dataList = [[fhaData, 'fhaData','https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/FHA-Loan.html'],
            [vaLoanData, 'vaLoanData', 'https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/VA-Loan.html'],
            [adjustableData, 'adjustableData', 'https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/adjustable-mortgage.html'],
            [frdata, 'frdata', 'https://www.pnc.com/en/personal-banking/borrowing/home-lending/mortgages/fixed-rate-mortgage.html']]
for d in dataList:
    for loan in loans:
        d[0]['amount'] = loan[0]
        d[0]['zipCode'] = loan[1]
        url = d[2]
        #Create a Session
        session = requests.session()
        p = session.get(url)
        headers = {"Host": "www.pnc.com",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
                   "Accept": "application/json, text/javascript, */*; q=0.01",
                   "Accept-Language": "en-US,en;q=0.5",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Referer": url,
                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "X-Requested-With": "XMLHttpRequest",
                   "CSRF-Token": "undefined",
                   "Content-Length": "2554",
                   "Connection": "keep-alive"}
        # Getting API data by posting data and url through requests module in python
        resp = session.post('https://www.pnc.com/bin/pnc/mortgage/regionalizedrates', data=d[0], headers=headers,
                            cookies=p.cookies).json()
        #Getting data by using json module
        for data in resp['loanOptions']:
            if len(data['responseProducts']) != 0:
                for dt in data['responseProducts']:
                    interestRate = dt['interestRate']
                    productName = dt['productName'].replace('+',' ')
                    APR = dt['apr']
                    a = [productName, loan[0], dt['productTermYears'], str(interestRate)+'%', str(APR)+'%']
                    Excel_Table.append(a)

print(tabulate(Excel_Table))

#--------------------------------------Moving Data to CSV File using Pandas----------------------------------
df = pd.DataFrame(Excel_Table[1:], columns=table_headers)
df["Date"] = ' '+today.strftime("%m-%d-%Y")
df["Bank_Name"] = "PNC FINANCIAL SERVICES GROUP INC"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df['Mortgage_Down_Payment'] ='20%'
df["Bank_Offer_Feature"] = "Offline"
df['Product_Apy'] = None
df['Min_Credit_Score_Mortagage'] ='720+'
df['Balance'] = None
#Arrange all fileds based on required format
order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage","Mortgage_Apr"]
df = df[order]
df.to_csv(path, index=False) #Moving data to CSV File.
print('Execution Completed...')
print('Total Execution Time is ',(time.time()-start_time)/60, 'Seconds')