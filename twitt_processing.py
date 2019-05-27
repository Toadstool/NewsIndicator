from nltk.tokenize import word_tokenize
import twitter
from twitter import Twitt
import pydic
import datetime

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
                'CCC':{
                    'search': ['CCC SA'],
                    'ignore':['sponsor'],
                    'sentiment':{
                        'kuluary':-1,
                        'lepsza':1 
                        }
                },
                'DINOPL':{
                    'search': ['Dino Polska'],
                    'ignore':['sponsor'],
                    'sentiment':{
                        'kuluary':-1,
                        'lepsza':1 
                        }
                },
                'LPP':{
                    'search': ['LPP','Reserved', 'House', 'Cropp', 'Mohito'],
                    'ignore':['sponsor'],
                    'sentiment':{
                        'kuluary':-1,
                        'lepsza':1 
                        }
                },
                'MBANK':{
                    'search': ['MBANK'],
                    'ignore':['sponsor'],
                    'sentiment':{
                        'kuluary':-1,
                        'lepsza':1 
                        }
                },
                'WPROST_TOP3':{
                    'search': ['Jarosław Kaczyński','Mateusz Morawiecki','Donald Tusk']
                }
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

    def download(self,companyCode,dateFrom,dateTo):
        twitts = []
        if self.KeyWords[companyCode]:
            for keyWord in self.KeyWords[companyCode]['search']:
                tws = twitter.searchPremium(keyWord,dateTo)                      
                for t in tws:                            
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)                
        else:
            for t in twitter.search(companyCode,dateTo):
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)     
        df = datetime.datetime.strptime(dateFrom,"%Y%m%d")    
        return list(filter(lambda x: x.date>=df, twitts))

    def indicator(self, companyCode,dateFrom,dateTo):
        
        twitts = self.download(companyCode,dateFrom,dateTo)
        for tw in twitts:
            tw.sentiment = 0
            tw.sentimentKeys = []
            tw.tokens = self.normalization(tw.text)
            tw.ignore = self.ignore(companyCode,tw.tokens)            
            if not tw.ignore:
                for k in self.KeyWords[companyCode]['sentiment'].keys():
                    if tw.tokens.find(k)!=-1:
                        tw.sentiment = tw.sentiment + self.KeyWords[companyCode]['sentiment'][k]                                             
                        tw.sentimentKeys.append(k)                                                  
        return twitts

if __name__ == '__main__':
   
    tw = TwittProcessing()
    results = tw.indicator('PKNORLEN','20190512')
    print(len(results)) 
    for r in results:
        if len(r.sentimentKeys)>0 or r.sentiment!=0 :
            print(str(r.sentiment) +' '+str(r.sentimentKeys))
