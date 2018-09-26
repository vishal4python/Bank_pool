from bs4 import BeautifulSoup
from extruct.jsonld import JsonLdExtractor
import traceback
from html import unescape
import statistics
import re
import math
import json

def getMetaDataContent(content, keywords):
    metaData = dict()
    jsoup = BeautifulSoup(content)
    metas = jsoup.find_all('meta')
    for keyword in keywords:
        try:
            big = 0
            for meta in metas:
                for key, value in meta.attrs.items():
                    try:
                        # print(key, value)
                        if keyword in value:
                            content = meta.attrs['content']
                            if content:
                                if len(content)>big:
                                    big = len(content)
                                    metaData[keyword] = content
                    except:
                        pass
        except Exception as e:
            print(e)
            return []
    return metaData


def getApplication_ld_json(content, keywords):
    jsonData = dict()
    try:
        jsoup = BeautifulSoup(content)
        apjson = jsoup.find('script', attrs={'type':'application/ld+json'})

        if apjson is not None:
            for keyword in keywords:
                for key, value in json.loads(apjson.text.replace(": '", ': "').replace("',", '",')).items():
                    if keyword in key:
                        if isinstance(value, str):
                            jsonData[keyword] = value
                        elif isinstance(value, dict):
                            jsonData[keyword] = value.get('name')

        return jsonData
    except:
        return jsonData

def getContentInsideTag(content):
    try:
        removeTags = ['a', 'script', 'style']
        jsoup = BeautifulSoup(content)
        # Fitering Data and getting Content from page source
        jsoup = jsoup.find('body')
        for remTag in removeTags:
            for div in jsoup.find_all(remTag):
                div.decompose()
        pContent = []
        for p in jsoup.find_all('p'):

            # print('-'.center(100, '-'))
            p = unescape(p.text).replace('\n', '')
            # print(p)
            specialCharacters = re.findall('[^a-zA-Z0-9,\.\'\" ]', p)
            # print(specialCharacters)
            if len(specialCharacters) != 0:
                a = [len(specialCharacters), len(p), p]
                if len(p) >= 100 and len(specialCharacters)<10:
                    pContent.append(a)

        pContent = sorted(pContent, key=lambda x:x[0], reverse=True)
        try:
            pContent = pContent[len(pContent[len(pContent)//2])//2]
        except:
            if len(pContent) != 0:
                pContent = pContent[0]

        return pContent[2]

        # for k in pContent:
        #     print(k)

    except:
        return None




def getBlogDivs(response, topDiv=math.nan, subTag=math.nan, subClass=math.nan):

    jsoup = BeautifulSoup(response)
    if isinstance(topDiv,str):
        div = jsoup.find(re.compile('div|dl|ul'), attrs={'class':topDiv})
        if isinstance(subTag,str) and isinstance(subClass,str):
            divs = div.find_all(subTag, attrs={'class':subClass})
        elif isinstance(subTag,str):
            divs = div.find_all(subTag)
    elif isinstance(subTag,str) and isinstance(subClass,str):
        divs = jsoup.find_all(subTag, attrs={'class': subClass})

    if len(divs) != 0:
        return divs
    else:
        return []


def blogData(tagsList):

    tagsData = []
    for r in tagsList:
        try:
            tag = dict()

            h = r.find(re.compile('(h2|h3|h4|h5|h6)'))

            anchor = [[len(a.text), a['href'], a.text] for a in r.find_all('a')]
            anchor = sorted(anchor, key = lambda x: int(x[0]),reverse=True)
            tag['Heading'] = h.text.strip() if h is not None else anchor[0][2].strip()
            tag['Url'] = anchor[0][1]

            ptags = [[len(p.text), p.text] for p in r.find_all('p')]
            ptags = sorted(ptags, key=lambda x: int(x[0]), reverse=True)
            content = ptags[0][1].replace('\r\n','').strip() if len(ptags) !=0 else None

            tag['Content'] = (content if len(content) >= 100 else None) if content else None
            text = r.text
            date = re.search('[a-zA-Z\.]* \d?\d, \d{4}|\d{4}[-\.]\d\d[-\.]\d\d|\d\d?[-\.]\d\d?[-\.]\d{4}|[a-zA-Z]* \d\d?, [a-zA-Z]* \d{4}', text)
            date = date.group(0) if date is not None else None
            tag['Date'] = date
            tagsData.append(tag)
        except:
            traceback.print_exc()

    if len(tagsData) != 0:
        return tagsData
    else:
        return []


