from nltk.tokenize import word_tokenize
import twitter
from twitter import Twitt
import pydic

class TwittProcessing:
    
    KeyWords= { 'PKNORLEN' : {
                    'search': ['pkn orlen','ropa'] ,
                    'ignore':['bieg','sponsor','Małachowski','Wyciszkiewicz','Kszczot','Lisek','Kubica','Dąbrowskiego','RobertKubicaKlub','WilliamsRacing','Williams','AkademiiInwestowania'],
                    'sentiment':{
                        'kuluary':-1,
                        'lepsza':1,
                        'lepszy':1
                        }
                    },
                'GRUPAAZOTY':{
                    'search': ['azoty'],
                    'ignore':['sponsor'],
                    'sentiment':{
                        'kuluary':-1,
                        'lepsza':1 
                        }
                },
                'CDPROJEKT':{
                    'search': ['CD Projekt'],
                    'ignore':['sponsor'],
                    'sentiment':{
                        'kuluary':-1,
                        'lepsza':1 
                        }
                },
            }

    def __init__(self):
        self.sjp= pydic.PyDic('sjp_clean.txt')

    def ignore(self,companyCode,text):
        ignore = False
        for i in self.KeyWords[companyCode]['ignore']:
            if i in text:
                ignore = True
        return ignore

    def normalization(self,text):
        if text and len(text)>0:
            tokenize =  word_tokenize(text)
            normalized= ''
            for token in tokenize:
                base = self.sjp.a_word_base(token)
                if len(base)>0:
                    normalized =normalized+ base[0]+' '
                else:
                    normalized =normalized+ token+' '
            return normalized

    def download(self,companyCode,date):
        twitts = []
        if self.KeyWords[companyCode]:
            for keyWord in self.KeyWords[companyCode]['search']:
                tws = twitter.searchPremium(keyWord,date)                      
                for t in tws:                            
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)                
        else:
            for t in twitter.search(companyCode,date):
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)
        return twitts

    def indicator(self, companyCode,date):
        
        twitts = self.download(companyCode,date)
        for tw in twitts:
            tw.sentiment = 0
            tw.sentimentKeys = []
            tw.text = self.normalization(tw.text)
            tw.ignore = self.ignore(companyCode,tw.text)
            #print(tw.text)
            if not tw.ignore:
                for k in self.KeyWords[companyCode]['sentiment'].keys():
                    if tw.text.find(k)!=-1:
                        tw.sentiment = tw.sentiment + self.KeyWords[companyCode]['sentiment'][k]                                             
                        tw.sentimentKeys.append(k)                        
                        #print(tw.text)
                        #print(k)
                        #print(str(self.KeyWords[companyCode]['sentiment'][k]))   
        return twitts

if __name__ == '__main__':
   
    tw = TwittProcessing()
    results = tw.indicator('PKNORLEN','20190512')
    print(len(results)) 
    for r in results:
        if len(r.sentimentKeys)>0 or r.sentiment!=0 :
            print(str(r.sentiment) +' '+str(r.sentimentKeys))
