from nltk.tokenize import word_tokenize
import twitter
import pydic

def processing(sjp,text):
    if text and len(text)>0:
        tokenize =  word_tokenize(text)
        base_token = []
        for token in tokenize:
            base = sjp.word_base(token)
            if len(base)>0:
                base_token.append(base[0])
            else:
                base_token.append(token)
        return base_token

if __name__ == '__main__':
    results = twitter.search('PKOBP')
    sjp = pydic.PyDic('sjp_clean.txt')
    
    for r in results:      
        print(r['text']) 
        print(processing(sjp,r['text']))
        

