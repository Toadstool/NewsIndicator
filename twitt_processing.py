from nltk.tokenize import word_tokenize
import twitter
import pydic

class TwittProcessing:
    
    KeyWords= { 'PKNORLEN' : {
                    'search': ['pkn orlen','ropa','paliwo'] ,
                    'ignore':['Piotr Małachowski','Adam Kszczot','Piotr Lisek','Adam Kszczot','Kubica','Mazurka Dąbrowskiego']
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

    def download(self,companyCode):
        twitts = []
        if self.KeyWords[companyCode]:
            for keyWord in self.KeyWords[companyCode]['search']:
                tws = twitter.search(keyWord)                      
                for t in tws:                    
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)
                print(keyWord+ ' downloaded:'+str(len(tws))+', total:'+str(len(twitts)))
        else:
            for t in twitter.search(companyCode):
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)
        return twitts


    def indicator(self, companyCode):
        processed = []
        twitts = self.download(companyCode)
        for tw in twitts:
            if self.ignore(companyCode,twitts.text):
                processed.append(tw)
        return processed


if __name__ == '__main__':
   
    tw = TwittProcessing()
    results = tw.download('PKNORLEN')
    print(len(results)) 
        

