import requests
from bs4 import BeautifulSoup
import datetime
import time
import pandas as pd
from tabulate import tabulate

keywords = ['Politics','Public+finances','Debt']
start_time = time.time()
today = datetime.datetime.now()
Excel_Table = []
headers = ['Date','Region','Country','Date Published','Author','Keyword','Source','Headline','Description','URL']
date_today = ' '+today.strftime('%Y-%m-%d')
region = 'LATAM'
country = 'Dominican Republic'
for k in keywords:
    response = requests.get('https://dominicantoday.com/?s='+str(k)).content
    pages = BeautifulSoup(response, 'html.parser')
    pages = pages.find('div', attrs={'class': 'pagination'}).find_all('a')[-1]['href']
    pages = pages.split('/')
    pages = pages[4]
    print(k)
    print(pages)
    for i in range(int(1) + int(pages))[1:]:

        response = requests.get('https://dominicantoday.com/page/'+str(i)+'/?s='+str(k))
        print(k)
        print(str('page = ')+str(i))
        # print(response)
        jsoup = BeautifulSoup(response.content)
        for sections in jsoup.find('ul',attrs={'id':'SearchResultsList'}).find_all('li'):
            title = sections.find('h2').find('a').text
            print(title)
            date = sections.find('span', attrs={'class': 'fecha'}).text
            # print(date)
            href = sections.find('h2').find('a')['href']
            print(href)
            p = sections.find('p',attrs={'class':'categoria'})
            if p is not None:
                p.decompose()
            h2 = sections.find('h2')
            if h2 is not None:
                h2.decompose()
            content = sections.find('p')

            if content is None:
                content = sections
            content = content.text.replace('\r\n','')
            print(content)
            date = date.split('|')[0]
            print(date)
            inputDate1 = date
            DateFormat1 = "%B %d, %Y "
            outPutDateFormat = "%m/%d/%Y"
            date1 = datetime.datetime.strptime(inputDate1, DateFormat1)
            date = datetime.date.strftime(date1, outPutDateFormat)
            print(date)


            a = [date_today,region,country, date,None,k.replace('+',' '),'dominicantoday.com',title,content.strip(),href]
            # print(a)
            Excel_Table.append(a)

print(tabulate(Excel_Table))
df = pd.DataFrame(Excel_Table, columns=headers)
df.to_excel("Domicantoday_"+today.strftime('%Y_%m_%d')+".xlsx", index=False) #Moving data to csv File

print('Total Execution Time:',time.time()-start_time,' Seconds') #Display total time taken to Execute the program
