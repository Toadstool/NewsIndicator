from nltk.tokenize import word_tokenize
import twitter
import pydic

class TwittProcessing:
    
    KeyWords= { 'PKNORLEN' : ['PKN ORLEN','ropa'] }

    def __init__(self):
        self.sjp= pydic.PyDic('sjp_clean.txt')

    def normalization(self,text):
        if text and len(text)>0:
            tokenize =  word_tokenize(text)
            base_token = []
            for token in tokenize:
                base = self.sjp.word_base(token)
                if len(base)>0:
                    base_token.append(base[0])
                else:
                    base_token.append(token)
            return base_token

    def download(self,companyCode):
        twitts = []
        if self.KeyWords[companyCode]:
            for keyWord in self.KeyWords[companyCode]:
                for t in twitter.search(keyWord):
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)
        else:
            for t in twitter.search(companyCode):
                    if len(list(filter(lambda x: x.id==t.id, twitts)))<=0: 
                        twitts.append(t)
        return twitts

if __name__ == '__main__':
   
    tw = TwittProcessing()
    results = tw.download('PKNORLEN')
    for r in results:      
        print(r.text) 
        print(tw.normalization(r.text))
        

