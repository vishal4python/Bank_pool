import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import datetime
import time
import pandas as pd
keywords = ['Politics','public+finances','Debt']
start_time = time.time()
today = datetime.datetime.now()
Excel_Table = []
headers = ['Date','Region','Country','Date Published','Author','Keyword','Source','Headline','Description','URL']
date_today = ' '+today.strftime('%Y-%m-%d')
region = 'LATAM'
country = 'Costa Rica'
for k in keywords:
    response = requests.get('https://qcostarica.com/?s='+str(k)).content
    pages = BeautifulSoup(response, 'html.parser')
    pages = pages.find('div', attrs={'class': 'page-nav td-pb-padding-side'}).find('span', attrs={'class': 'pages'}).text
    pages = pages.split()[3]
    print(pages)

    for i in range(int(1) + int(pages))[1:]:
        response = requests.get('https://qcostarica.com/page/'+str(i)+'/?s='+str(k))
        print(k)
        print(str('page = ')+str(i))
        # print(response)
        jsoup = BeautifulSoup(response.content)
        for sections in jsoup.find_all('div',attrs={'class':'td_module_16 td_module_wrap td-animation-stack'}):
            title = sections.find('h3').find('a').text
            print(title)
            content = sections.find('div',attrs={'class':'td-excerpt'}).text
            print(content.strip())
            date = sections.find('time').text
            # print(date)
            href = sections.find('h3').find('a')['href']
            print(href)

            inputDate1 = date
            DateFormat1 = "%d %B %Y"
            outPutDateFormat = "%m/%d/%Y"
            date1 = datetime.datetime.strptime(inputDate1, DateFormat1)
            date = datetime.date.strftime(date1, outPutDateFormat)
            print(date)

            a = [date_today, region, country, date, None, k.replace('+',' '), 'qcostarica.com', title, content.strip(), href]
            # print(a)
            Excel_Table.append(a)


print(tabulate(Excel_Table))
df = pd.DataFrame(Excel_Table, columns=headers)
df.to_excel("Qcostarica_"+today.strftime('%Y_%m_%d')+".xlsx", index=False) #Moving data to csv File

print('Total Execution Time:',time.time()-start_time,' Seconds') #Display total time taken to Execute the program
