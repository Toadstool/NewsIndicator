
import tweepy
import config
import json

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
        


def getContext():
    auth = tweepy.OAuthHandler(config.Config.APP_NAME, config.Config.SECRET_KEY)
    return tweepy.API(auth) 

def search(query):
    api = getContext()
    results = api.search(query,lang='pl',tweet_mode='extended')
    #for x in results:
    #    file_object = open('test/x.id', 'w')
    #    json.dump(x._json, file_object)

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
    
    