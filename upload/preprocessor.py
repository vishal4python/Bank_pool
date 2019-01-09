# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 15:20:49 2018

@author: mullzoh
"""
import os
import pandas as pd
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordNERTagger

st = StanfordNERTagger(r'C:\Users\mullzoh\Desktop\Balthasar\Code\stanford-ner\english.all.3class.distsim.crf.ser',
                       r'C:\Users\mullzoh\Desktop\Balthasar\Code\stanford-ner\stanford-ner-2017-06-09\stanford-ner.jar')

javapath = r"C:\Program Files (x86)\Java\jre1.8.0_181\bin\java.exe"
os.environ['JAVAHOME'] = javapath

def mergefile():
    todaydate = datetime.now().strftime("%m-%d-%Y")
    df = pd.DataFrame()
    path = r'C:\Users\mullzoh\Desktop\NewsArticleScript\reuters\newsArticleData\\' + todaydate + '\\'
    files = os.listdir(path)
    for f in files:
        data = pd.read_excel(path+f)
        df = df.append(data)
        print (len(df))
    return (df)
    
    
    
def removeduplicate(df):
    df = df.drop_duplicates('Headline')
    return df
    
def delete_file_folder(complete_filename):
    os.remove(complete_filename)
    
#mdf = mergefile()
#print (len(mdf))
#ddf = removeduplicate(mdf)
#ddf.to_excel(r"C:\Users\mullzoh\Desktop\Balthasar\Input\test.xlsx")
#print (len(ddf))
#filename = r"C:\Users\mullzoh\Desktop\Balthasar\Input\test.xlsx"
#delete_file_folder(filename)

def get_NER(text):
    for sent in nltk.sent_tokenize(text):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = st.tag(tokens)
        
        for tag in tags:
            if tag[1] in ["PERSON", "LOCATION", "ORGANIZATION"]:
                print(tag)



text= """
Sensex rises, Infosys leads gains on buyback plan
Chandini Monnappa
2 MIN READ

(Reuters) - Indian shares traded higher on Wednesday tracking gains in broader Asia, as risk appetite improved on hopes of a positive outcome of the U.S.-China trade talks, while domestic investors remained optimistic about a strong results season starting this week.

Brokers trade at their computer terminals at a stock brokerage firm in Mumbai, August 25, 2015. REUTERS/Shailesh Andrade/Files
Stocks across the globe have witnessed a rally this week after jitters about a global economic slowdown were pacified by a rating cut by China, strong U.S. jobs data, and a dovish tone by the Federal Reserve.

“Markets are tracking global cues, there are expectations of better Q3 numbers and risk appetite has generally been better,” said Anand James, chief market strategist at Geojit Financial Services.

“The global rally is helping sentiment, there is strength across sectors, we have not made big moves, but there is some sense of positivity.”

SPONSORED

The broader NSE Nifty was up 0.33 percent at 10,837.40 as of 0557 GMT, while the benchmark BSE Sensex was 0.47 percent higher at 36,148.72.

Gains on the Nifty were driven by IT stocks, with shares of Infosys Ltd rising as much as 2.95 percent, their highest since Dec. 17 after it said it will consider a share buyback and a special dividend on Friday.

“Any buyback or the kind of incentives has to be seen with business prospects the companies are seeing, it is not a major driver of the index but obviously has lent a positive bias to the market.” James said.

Infosys is set to report its December quarter results on Jan. 11.

Shares of Indusind Bank Ltd were up as much as 1.35 percent ahead of quarterly results announcement.

Yes Bank Ltd shares were trading down as much as 1.2 percent. The lender is scheduled to hold a board meeting later in the day and is expected to make final recommendations to the central bank for naming a new chief executive officer.
"""
get_NER(text)