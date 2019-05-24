
import tweepy
import config
import json
import datetime
import os
import sys
import jsonpickle
from tweepy.binder import bind_api
from tweepy.api import API
from tweepy.parsers import ModelParser
from tweepy.models import ResultSet, ModelFactory, Status



class Twitt():   
   
    id=0
    date=None
    text = ''
    user = ''
    lang = ''
    user_power = 0
    twitt_power= 0
    power = 0
    sentiment= 0
    sentimentKeys = []
    ignore = False    

    def __init__(self,id,date,text,user,user_power,lang,twitt_power):
        self.id = id
        self.date = date
        self.text = text
        self.user = user
        self.lang = lang
        self.user_power = user_power    
        self.twitt_power = twitt_power
        self.power = twitt_power + user_power
        self.sentiment =0
        self.sentimentKeys = []
        self.ignore = False
        
class PremiumSearchResults(ResultSet):
    next = None

    @classmethod
    def parse(cls, api, json):
                
        results = PremiumSearchResults()
        for k, v in json.items():
            if k == 'requestParameters':
                    metadata = v
            if k == 'next':
                    results.next = v

        results.refresh_url = metadata.get('refresh_url')
        results.completed_in = metadata.get('completed_in')
        results.query = metadata.get('query')
        results.count = metadata.get('count')
        results.next_results = metadata.get('next_results')

        status_model = getattr(api.parser.model_factory, 'status') if api else Status

        for status in json['results']:
            s= status_model.parse(api, status)
            for k, v in status.items():
                if k == 'extended_tweet':                   
                    s.text = v['full_text']                               
            results.append(s)
        return results

class PremiumModelFactory(ModelFactory):
    premium_search_results = PremiumSearchResults

class EAPI(API):
    def __init__(self,auth_handler):
        super().__init__(auth_handler,parser  = ModelParser(model_factory = PremiumModelFactory())) 
    @property
    def search30DEV(self):
        return bind_api(
                api= self,
                path='/tweets/search/30day/DEV.json',
                method='GET',
                payload_type='premium_search_results',
                allowed_param=['query', 'lang', 'locale', 'since_id', 'geocode',
                           'max_id', 'since', 'until', 'result_type',
                           'count', 'include_entities', 'from',
                           'to', 'source','tweet_mode']                
            )


def searchPremium(query,date):

    today = datetime.date.today()    
    if date==None:
           date =today.strftime("%Y%m%d")
    filePath = 'data/Twitter_SearchPremium_'+query+'_'+date +'.json'
    if os.path.isfile(filePath):        
        with open(filePath) as json_file:  
            return jsonpickle.loads(json_file.read())
    
    print('twitter download '+query)  
    auth = tweepy.OAuthHandler(config.Config.APP_NAME, config.Config.SECRET_KEY)
    api = EAPI(auth)
    
    
    query = query+ ' lang:pl'
    fromDate = (today - datetime.timedelta(days=7)).strftime("%Y%m%d")+'0000'      
    results = api.search30DEV(query,fromDate= fromDate)
    try:
        data =  list(map(lambda x: Twitt(x.id,x.created_at,x.text,x.user.name,                                 
                                    x.user.followers_count 
                                    + x.user.friends_count
                                    + x.user.listed_count
                                    + x.user.favourites_count,
                                    x.user.lang,
                                    x.retweet_count+ x.favorite_count)
                    ,results)) 
        while results.next:       
            print(results.next)
            print(str(results[0].created_at)) 
            results = api.search30DEV(query,fromDate= fromDate,next =results.next)
            data.extend(list(map(lambda x: Twitt(x.id,x.created_at,x.text,x.user.name,                                 
                                    x.user.followers_count 
                                    + x.user.friends_count
                                    + x.user.listed_count
                                    + x.user.favourites_count,
                                    x.user.lang,
                                    x.retweet_count+ x.favorite_count)
                    ,results)))
    except:
         print(sys.exc_info()[0],"occured.")
    
    with open(filePath, 'w+') as outfile: 
        outfile.write(jsonpickle.dumps(data))
    return data

def search(query,date):

    today = datetime.date.today()    
    if date==None:
        date =today.strftime("%Y%m%d")
    filePath = 'data/Twitter_Search_'+query+'_'+date +'.json'
    if os.path.isfile(filePath):        
        with open(filePath) as json_file:  
            return jsonpickle.loads(json_file.read())

    print('twitter download '+query)
    auth = tweepy.OAuthHandler(config.Config.APP_NAME, config.Config.SECRET_KEY)
    api = EAPI(auth)
    fromDate = (today - datetime.timedelta(days=6)).strftime("%Y%m%d")+'0000'        
    results = api.search(query,lang='pl',tweet_mode='extended',fromDate=fromDate)

    data=  list(map(lambda x: Twitt(x.id,x.created_at,x.full_text,x.user.name,                                 
                                    x.user.followers_count 
                                    + x.user.friends_count
                                    + x.user.listed_count
                                    + x.user.favourites_count,
                                    x.user.lang,
                                    x.retweet_count+ x.favorite_count)
                    ,results)) 
    with open(filePath, 'w+') as outfile: 
        outfile.write(jsonpickle.dumps(data))
    return data

if __name__ == '__main__':
    results = search('pkn orlen','20190512')
    for r in results:
        print(r.id)
        #print(r.text)
    print('len: ',str(len(results)))    
    
    