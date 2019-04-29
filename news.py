
import tweepy
import config
import json

def getContext():
    auth = tweepy.OAuthHandler(config.Config.APP_NAME, config.Config.SECRET_KEY)
    return tweepy.API(auth) 

def search(query):
    api = getContext()
    results = api.search(query)

    return list(map(lambda x:{ 'date': x.created_at,'text': x.text,'user': x.user.name },results)) 

if __name__ == '__main__':
    results = search('PKOBP')
    for r in results:
        print(r)
        print("\n")
    

    