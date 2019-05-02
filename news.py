
import tweepy
import config
import json
import nltk
from nltk.tokenize import word_tokenize

def getContext():
    auth = tweepy.OAuthHandler(config.Config.APP_NAME, config.Config.SECRET_KEY)
    return tweepy.API(auth) 

def search(query):
    api = getContext()
    results = api.search(query,tweet_mode='extended')

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
        print(word_tokenize(r['text']))
        print("\n")
    
    