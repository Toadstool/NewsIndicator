from nltk.tokenize import word_tokenize
import twitter
from twitter import Twitt
import pydic

class TwittProcessing:
    
    KeyWords= { 'PKNORLEN' : {
                    'search': ['pkn orlen','ropa'] ,
                    'ignore':['Małachowski','Kszczot','Lisek','Kubica','Dąbrowskiego']
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
                base = self.sjp.word_base(token)
                if len(base)>0:
                    normalized += base[0]+' '
                else:
                    normalized += base[0]+' '
            return normalized

    def download(self,companyCode,date):
        twitts = []
        if self.KeyWords[companyCode]:
            for keyWord in self.KeyWords[companyCode]['search']:
                tws = twitter.searchPremium(keyWord,date)                      
                for t in tws:                            
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)
                print(keyWord+ ' downloaded:'+str(len(tws))+', total:'+str(len(twitts)))
        else:
            for t in twitter.search(companyCode,date):
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)
        return twitts

    def indicator(self, companyCode,date):
        processed = []
        twitts = self.download(companyCode,date)
        for tw in twitts:
            if not self.ignore(companyCode,tw.text):
                processed.append(tw)
        return processed


if __name__ == '__main__':
   
    tw = TwittProcessing()
    results = tw.indicator('PKNORLEN','20190512')
    print(len(results)) 
    
        

