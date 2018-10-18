from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import twitter_credentials
from textblob import TextBlob 

class TweetData():
    def __init__(self, text, screen_name, created_at, followers_count):
        self.text = text
        self.screen_name = screen_name
        self.created_at = created_at
        self.followers_count = followers_count

def collect_data(tweets_data_path):
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweets_data.append(json.loads(line))
        except:
            continue
    return tweets_data

def collect_tweets(tweets_data):
    tweets = []
    for tweet in tweets_data:
        data = TweetData(tweet['text'], tweet['user']['screen_name'], 
            tweet['created_at'], tweet['user']['followers_count'])
        tweets.append(data)
        #print (data.polarity)
    return tweets

if __name__ == '__main__':

    tweets_data_path = 'tweets.json' 
    tweets = collect_tweets(collect_data(tweets_data_path))

    #print (len(tweets_data))
