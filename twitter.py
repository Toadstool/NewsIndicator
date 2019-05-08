
import tweepy
import config
import json
import datetime
from tweepy.binder import bind_api
from tweepy.api import API
from tweepy.parsers import ModelParser
from tweepy.models import ResultSet, ModelFactory, Status


class Twitt:
    id=0
    date=None
    text = ''
    user = ''
    lang = ''
    user_power = 0
    twitt_power= 0
    power = 0
    

    def __init__(self,id,date,text,user,user_power,lang,twitt_power):
        self.id = id
        self.date = date
        self.text = text
        self.user = user
        self.lang = lang
        self.user_power = user_power    
        self.twitt_power = twitt_power
        self.power = twitt_power + user_power
        
class PremiumSearchResults(ResultSet):
    next = None

    @classmethod
    def parse(cls, api, json):
        
        metadata = json['requestParameters']
        results = PremiumSearchResults()
        results.next = json['next']
        results.refresh_url = metadata.get('refresh_url')
        results.completed_in = metadata.get('completed_in')
        results.query = metadata.get('query')
        results.count = metadata.get('count')
        results.next_results = metadata.get('next_results')

        status_model = getattr(api.parser.model_factory, 'status') if api else Status

        for status in json['results']:
            s= status_model.parse(api, status)
            for k, v in status.items():
                if k == 'retweeted_status':
                    for k1, v1 in v.items():
                        if k1 == 'extended_tweet':
                            s.text = v1['full_text']
                    
           
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


def search(query):
    auth = tweepy.OAuthHandler(config.Config.APP_NAME, config.Config.SECRET_KEY)
    api = EAPI(auth)
    
    today = datetime.date.today()
    fromDate = (today + datetime.timedelta(days=-today.weekday(), weeks=1)).strftime("%Y%d%m")+'0000'
    print(fromDate)
    #results = api.search30DEV(query)
    results = api.search(query,lang='pl',tweet_mode='extended',fromDate=fromDate)

    return list(map(lambda x: Twitt(x.id,x.created_at,x.full_text,x.user.name,                                 
                                    x.user.followers_count 
                                    + x.user.friends_count
                                    + x.user.listed_count
                                    + x.user.favourites_count,
                                    x.user.lang,
                                    x.retweet_count+ x.favorite_count)
                    ,results)) 

if __name__ == '__main__':
    results = search('pkn orlen')
    print(str(len(results)))
    
    