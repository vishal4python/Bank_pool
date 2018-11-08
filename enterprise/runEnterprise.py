"""
Purpose     : Extract data from comparefirst
        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Moody's Analytics    ##11th July, 2018     ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date              Version     Author      Description
        11th July, 2018   v 1.0       Vishal      Data Extraction
"""

import os
import re
import time
import logging
from datetime import datetime
import concurrent.futures
import pandas as pd
from tabulate import tabulate
from enterprise_car import get_eneterpricecar_data
from log_file import function_logger, write_doc

# Retrieve a single page and report the URL and contents
def load_row(row, car_data):
    get_eneterpricecar_data(row, car_data)
    print(row)



if __name__ == '__main__':
    print(os.getcwd().rsplit('\\', 1)[0]+'\\output\\')
    output_path = os.getcwd().rsplit('\\', 1)[0]+'\\output\\'+datetime.today().strftime('%d-%m-%Y')+'\\enterpriseCarData.xlsx'
    for filename in os.listdir(os.getcwd()):
        if re.match("log_file_\d.*\.log", filename):
            os.remove(os.getcwd() + '\\' + filename)
        elif re.match(".*\.png", filename):
            os.remove(os.getcwd() + '\\' + filename)
    write_doc(doc=__doc__)
    f_logger = function_logger(logging.DEBUG, logging.ERROR)
    f_logger.info('Program Execution Started Time' + str(datetime.now().time()))

    car_data_headers = ['Date', 'pickup_date', 'return_date','Location', 'Airport name','selected_location', 'Location Code',
                    'className', 'vehicleName', 'payNowAmount', 'payNowAmountUnit',
                'payNowTotalAmount','payNowTotalUnit','payLaterAmount','payLaterAmountUnit','payLaterTotalAmount','payLaterTotalUnit','sitename']
    start_time = time.time()
    DF = pd.read_excel('enterprise_car_locations.xlsx')
    print(DF.to_dict(orient='records'))
    mainRows = subRows = total_records = DF.to_dict(orient='records')
    car_data = dict()
    check = 1
    while True:
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(load_row,  row, car_data): row for row in subRows}
            for future in concurrent.futures.as_completed(future_to_url):
                car_loc = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (car_loc, exc))
                else:
                    print(car_loc, 'is Done')
                    f_logger.info('{}is Done'.format(car_loc))

        subRows = []
        for r in mainRows:
            if r['Code'] not in car_data:
                subRows.append(r)

        if len(mainRows) == len(car_data):
            break
        elif check == 2:
            break
        elif len(subRows) == 1:
            break

        check += 1
        f_logger.info('Round {} completed'.format(check))

    if len(subRows)!=0:
        print('After 3 Checking still missed rows')
        f_logger.info('Missed data {}'.format([r['Code'] for r in subRows]))
        f_logger.info('Total Locations = {} and missed location'.format((len(mainRows), (len(mainRows)-len(car_data)))))
        print(subRows)
    else:
        f_logger.info('All rows are executed successfully.')
        f_logger.info('Total Locations = {}'.format(len(car_data)))
        print('All rows are executed successfully.')
    fina_data = []
    print('Total Found Airports = ', len(car_data))
    for key, item in car_data.items():
        print(key)
        fina_data.extend(item)

    df = pd.DataFrame(fina_data, columns=car_data_headers)
    df.to_excel(output_path, index=False)
    f_logger.info('File Name : {}'.format(output_path))
    f_logger.info('Total Execution Time is {} Min'.format((time.time()-start_time)/60))
    print('Total Execution Time is ',(time.time()-start_time)/60)
