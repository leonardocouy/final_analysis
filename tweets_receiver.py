import tweepy
from pymongo import MongoClient
from decouple import config
from tweepy import Stream
from tweepy import StreamListener
from tweepy.streaming import json

CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')

client = MongoClient('localhost', 27017)
db = client.final


class TweetStreamListener(StreamListener):

    def on_data(self, data):

        tweet = json.loads(data)


        try:
            db.tweets.insert(tweet)
        except KeyError:
            pass

if __name__ == '__main__':
    listener = TweetStreamListener()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)
    stream.filter(track=['CRUxFLA', 'Flamengo', 'Cruzeiro', 'Copa do Brasil'], async=True)
