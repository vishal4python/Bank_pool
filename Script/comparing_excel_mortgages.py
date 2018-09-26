#-*- coding:utf-8 -*-
import os
from maks_lib import US
import re

old_file = US+"US_FINAL_Mortgage_Data_2018_09_21.csv" #Please enter the path of Old file
new_file = US+"US_FINAL_Mortgage_Data_2018_09_25.csv"#Please enter the path of New file
outputFile = US+"Mortgage_comparision_US.csv" #Please enter the path of output file


table_rows = ''
old_data_date = ''
old_data = []
new_data_date = ''
new_data = []
table_found = False
with open(old_file, 'r') as t1, open(new_file, 'r') as t2:
    for k in t1.readlines():
        # print(k)
        if not table_found:
            table_rows = k
            table_found = True
        print(k)
        if ',' in k:
            old_data_date = k[:k.index(',')]
            k = re.sub(r'[^\x00-\x7F]', '', k[k.index(',') + 1:])
            old_data.append(k)
    for l in t2.readlines():
        if ',' in l:
            new_data_date = l[:l.index(',')]
            l = re.sub(r'[^\x00-\x7F]','',l[l.index(',')+1:])
            new_data.append(l)

# print(table_rows)
with open(outputFile, 'w') as outFile:
    outFile.write(table_rows)
    for line in new_data:
        if line not in old_data:
            print(line)
            outFile.write(new_data_date+','+line)