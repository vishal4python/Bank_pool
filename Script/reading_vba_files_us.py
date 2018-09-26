 # Library to be imported
import os, sys
import win32com.client
from maks_lib import scripts

# Path and file name to be used for opening
path = scripts

# Change to our current directory where macro exists
os.chdir(path)

us_banks = ["Ally-2.xlsm","CapitalOne-2.xlsm","JPMorgan-2.xlsm","SunTrust-2.xlsm"]

# Run us_banks
for us_banks in us_banks:
    if os.path.exists(us_banks):
        xl=win32com.client.Dispatch("Excel.Application")
        xl.Workbooks.Open(path+str(us_banks), ReadOnly=1)
    del xl
