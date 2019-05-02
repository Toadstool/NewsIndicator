
import tweepy
import config
import json


def getContext():
    auth = tweepy.OAuthHandler(config.Config.APP_NAME, config.Config.SECRET_KEY)
    return tweepy.API(auth) 

def search(query):
    api = getContext()
    results = api.search(query,tweet_mode='extended')
    #for x in results:
    #    file_object = open('test/x.id', 'w')
    #    json.dump(x._json, file_object)

    return list(map(lambda x:{ 'id': x.id,
                                'date': x.created_at,
                                'text': x.full_text,
                                'user': x.user.name,                                 
                                'user_power': x.user.followers_count 
                                             + x.user.friends_count
                                             + x.user.listed_count
                                             + x.user.favourites_count,
                                'lang':x.user.lang,
                                 'power': x.retweet_count
                                         + x.favorite_count
                            },results)) 

if __name__ == '__main__':
    results = search('PKOBP')
    for r in results:       
        print(r['text'])
        print("\n")
    
    