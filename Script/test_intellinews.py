import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
keywords = ['Economy','Economics','politics','political','politically','Government+Policy',
            'Government+Policies','president','finance+minister','cabinet','economic+law',
            'economic+laws','bills','referendum','parliament','election','elections',
            'political+parties','GDP','growth','consumer+inflation','unemployment','CPI',
            'fuel+prices','oil+prices','house+prices','retail+sales','Central+bank',
            'interest+rates','monetary+policy','currency+fluctuations','international+investment',
            'Consumer+confidence','business+confidence','PMI','Trade+balance','budget+balance',
            'external+debt','imports','exports','Sanctions','trade+war','Tariffs','Trump',
            'Construction+output','industrial+output','industrial+production','jobless+growth',
            'Credit+rating','bond+market','job+market','labour+market','migration','EU+funds',
            'cohesion+funds','IMF','Moody’s','Fitch','Issue','issuance','bonds','syndicated+loan',
            'competitiveness','devaluation','depreciation','fiscal+deficit','primary+deficit',
            'surplus','tightening','financing+needs','maturity','ties','World+Bank','EBRD','IFC',
            'EIB','Debt','fiscal','revenue','expenditure','budget','bill','parliament']
Excel_Table = []
headers = ['Date','Region','Country','Date Published','Author','Keyword','Source','Headline','Description','URL']
for k in keywords:
    print('+++++++++++++++++++++++++++++++++++++++++++')
    print(k)
    response = requests.get('http://www.intellinews.com/search/?search_for='+str(k)).content
    jsoup = BeautifulSoup(response,'html.parser')
    for sections in jsoup.find_all('div',attrs={'class':'newsArticle mt10'}):
        # print(sections)
        title = sections.find('h2').text
        print(title)
        date = sections.find('span',attrs={'class':'date'}).text
        print(date)
        content = sections.find('p').text
        print(content.strip())
        href = sections.find('a')['href']
        print(str('http://www.intellinews.com')+str(href))