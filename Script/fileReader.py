import pandas as pd
import math
import requests
import random
import traceback
from selenium import webdriver
from datetime import datetime
import statistics
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# driver = webdriver.Firefox()
import re
from bs4 import BeautifulSoup
from searchFunctions import getBlogDivs, blogData, getMetaDataContent,getApplication_ld_json, getContentInsideTag
ex = pd.ExcelFile('keywordsAndUrls.xlsx')
print(ex.sheet_names)
df_urls = ex.parse('urls')
df_urls = df_urls.to_dict('records')
TableHeaders = ["Date", "Region", "Country", "Date Published", "Author", "Headline","Keyword", "Source","Summary", "URL"]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}
todaydate = datetime.now().strftime("%m-%d-%Y")
finaldata = []
kewords = ['Politics', 'Public finances', 'Debt']
for record in df_urls:
    print(record['url'])

    for keyword in kewords[:1]:
        try:
            resp = requests.get(record['url'], headers=headers).content
            divs = getBlogDivs(resp, topDiv=record['topdiv'], subTag=record['subtag'], subClass=record['subclass'])
            data = blogData(divs)
            print(len(data))
            for div in data:
                print(div)
                try:
                    Country = record['Country']
                    Region = record['Region']
                    source = record['url']#re.search('\..*\.', record['url']).group(0).strip('.')
                    articleHeading = div['Heading']
                    Author = None
                    publishedDate = div['Date']
                    finalContent = div['Content']
                    if div['Url'][0] == '/':
                        url = record['weburl']+div['Url']
                    else:
                        url = div['Url']
                    webUrl = url
                    contentList = []
                    subContent = requests.get(url, headers=headers).content

                    jsonData = getApplication_ld_json(subContent, ['description', 'author', 'published'])
                    if Author is None:
                        if jsonData.get('author'):
                            Author = jsonData.get('author') if len(jsonData.get('author')) < 30 else None
                    if publishedDate is None:
                        publishedDate = jsonData.get('published')
                    if jsonData.get('description'):
                        if len(jsonData.get('description')) >= 100:
                            contentList.append(jsonData.get('description'))

                    metaData = getMetaDataContent(subContent, ['description', 'author', 'published'])
                    if Author is None:
                        if metaData.get('author'):
                            Author = metaData.get('author') if len(metaData.get('author')) < 30 else None
                    if publishedDate is None:
                        publishedDate = metaData.get('published')
                    if metaData.get('description'):
                        if len(metaData.get('description')) >= 100:
                            contentList.append(metaData.get('description'))


                    pContent = getContentInsideTag(subContent)
                    if pContent is not None:
                        contentList.append(pContent)

                    if len(contentList) != 0 and finalContent is None:
                        finalContent = random.choice(contentList)

                    a = [todaydate, Region, Country, publishedDate, Author if Author is not None else "N/A", articleHeading, keyword, source, finalContent, webUrl]
                    finaldata.append(a)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
        except Exception as e:
            print(e)
            traceback.print_exc()
df = pd.DataFrame(finaldata, columns=TableHeaders)
df.to_excel('eeee.xlsx', index=False)