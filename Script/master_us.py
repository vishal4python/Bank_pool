"""
Purpose     : Extract data for UK Banks

        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Moody's Analytics    ##16th March,2018    ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date                   Version     Author      Description
        16th March,2018        v 0.1       Deepak      Initial development
"""
import glob
import subprocess as sp
from maks_lib import log_config
from maks_lib import logpath
import logging
import time
start_time = time.time()
# banks = glob.glob("*.py")
#
# Bank_Names = ['wellsfargo_deposit_v2.py','wellsfargo_mortgage_v2.py','pnc_mortgage_v2.py','pnc_deposit.py','suntrust_deposit_v2.py','suntrust_mortgage_v2.py',
# 'capital_one_deposits_v2.py','Ally_deposits_v2.py','Ally_mortgage_v2.py','synchrony_deposits_new.py','citi_bank.py','citi_mortgage.py',
# 'consolidated_BOA.py','Bank_of_america_mortgage_v2.py','Consolidate_JPM_Data_Deposit_final.py','JPM_mortgage_v2.py',
# 'Us_Deposits.py','Us_Deposits_Mortgage.py','bankRate.py','bankRate_Mortgage.py',
# 'Deposits_account.py','MyBankTracker_Deposits.py','MyBankTracker_Mortgage.py','Nerdwallet_Bank_Deposits.py']
#
#
# log_config(logpath, "US_BANK_RUNStatus".format(), __doc__)
# for bank in Bank_Names:
#     logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
#     cmd = "python "+ bank
#     stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
#     if 0 == stdout.returncode:
#         logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
#     else:
#         logging.error('Got: Error for bank: {}\n'.format(bank))
#
# try:
#     consolidated_banks = ['Final_Consolidation_Deposits.py','Final_Consolidation_MORTGAGE.py']
#
#     log_config(logpath, "US_BANK_RUNStatus".format(), __doc__)
#     for bank in consolidated_banks:
#         logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
#         cmd = "python "+ bank
#         stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
#         if 0 == stdout.returncode:
#             logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
#         else:
#             logging.error('Got: Error for bank: {}\n'.format(bank))
# except Exception as e:
#     print(e)
#
#
# try:
#     aggregator_banks = ['Aggregator_US_DEPOSIT.py','Aggregator_US_Mortgage.py']
#
#     log_config(logpath, "US_BANK_RUNStatus".format(), __doc__)
#     for bank in aggregator_banks:
#         logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
#         cmd = "python "+ bank
#         stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
#         if 0 == stdout.returncode:
#             logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
#         else:
#             logging.error('Got: Error for bank: {}\n'.format(bank))
# except Exception as p:
#     print(p)
#
# try:
#     us_bank_and_agg = ['US_bank_agg.py']
#
#     log_config(logpath, "US_BANK_RUNStatus".format(), __doc__)
#     for bank in us_bank_and_agg:
#         logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
#         cmd = "python "+ bank
#         stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
#         if 0 == stdout.returncode:
#             logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
#         else:
#             logging.error('Got: Error for bank: {}\n'.format(bank))
# except Exception as c:
#     print(c)

try:
    consolidated_banks = ['validation_checker_deposit.py','validation_checker_mortgage.py']

    log_config(logpath, "US_BANK_RUNStatus".format(), __doc__)
    for bank in consolidated_banks:
        logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
        cmd = "python "+ bank
        stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
        if 0 == stdout.returncode:
            logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
        else:
            logging.error('Got: Error for bank: {}\n'.format(bank))
except Exception as e:
    print(e)


try:
    consolidated_banks = ['comparing_excel_deposits.py','comparing_excel_mortgages.py']

    log_config(logpath, "US_BANK_RUNStatus".format(), __doc__)
    for bank in consolidated_banks:
        logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
        cmd = "python " + bank
        stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
        if 0 == stdout.returncode:
            logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
        else:
            logging.error('Got: Error for bank: {}\n'.format(bank))
except Exception as e:
    print(e)

End_time = time.time()-start_time
print(End_time/60)