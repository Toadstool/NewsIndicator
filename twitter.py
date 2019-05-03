
import tweepy
import config
import json

class Twitt:
    id=0
    date=None
    text = ''
    user = ''
    user_power = 0
    lang = ''
    power = 0

    def __init__(self,id,date,text,user,user_power,lang,power):
        self.id = id
        self.date = date
        self.text = text
        self.user = user
        self.user_power = user_power
        self.lang = lang
        self.power = power

def getContext():
    auth = tweepy.OAuthHandler(config.Config.APP_NAME, config.Config.SECRET_KEY)
    return tweepy.API(auth) 

def search(query):
    api = getContext()
    results = api.search(query,tweet_mode='extended')
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
    results = search('PKOBP')
    for r in results:       
        print(r.text)
        print("\n")
    
    