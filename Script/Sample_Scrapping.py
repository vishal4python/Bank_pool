#!/usr/bin/env python
"""
Purpose     : Extract data for different rates of available account types in SBI

        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Moody's Analytics    ##27th FEB,2017       ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date              Version     Author      Description
        27th Feb,2017     v 0.1       Deepak      extract_data()
"""


import datetime
import logging
from maks_lib import logpath,output_path,input_path
from maks_lib import log_config

print(logpath,output_path,input_path)


if __name__== "__main__":
    print("Please wait while we execute the code and generate the Log file for you...")
    log_config(logpath,log_file_name = "SBI", change_log=__doc__)
    ######Add log for all your Events##########
    msg = "Opening the website {}".format("www.sbi.co.in")
    logging.info(msg)
