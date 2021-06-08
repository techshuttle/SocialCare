import os
import tweepy
import config
import pandas as pd
import sys
import numpy as np
import re
import time
from nltk.stem import WordNetLemmatizer
from datetime import datetime,timedelta

from expertai.nlapi.cloud.client import ExpertAiClient
client = ExpertAiClient()

# from dotenv import load_dotenv
# load_dotenv()


os.environ["EAI_USERNAME"] = config.expertai_mail
os.environ["EAI_PASSWORD"] =config.expertai_password



"""authentication function"""

def twitter_api():
    try:
        consumer_key = config.consumer_key
        consumer_secret = config.consumer_secret
        access_token = config.access_token
        access_secret = config.access_secret

    except KeyError:
        sys.stderr.write("TWITTER_* envirnoment variable not set\n")
        sys.exit(1)
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth,wait_on_rate_limit= True)
    return api

def sentiment(text):
    """returns overall sentiment"""
    output = client.specific_resource_analysis(body = {"document":{"text": text}},
                                               params = {'language': 'en','resource': 'sentiment'})
    return output.sentiment.overall

# Cleaning the tweets
def preprocess(tweet):
    # remove links
    tweet = re.sub(r'http\S+', '', tweet)
    # remove mentions
    tweet = re.sub("@\w+", "", tweet)
    # alphanumeric and hashtags
    tweet = re.sub("[^a-zA-Z#]", " ", tweet)
    # remove multiple spaces
    tweet = re.sub("\s+", " ", tweet)
    tweet = tweet.lower()
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    sent = ' '.join([lemmatizer.lemmatize(w) for w in tweet.split() if len(lemmatizer.lemmatize(w)) > 3])

    return sent


def tweet_pattern_in_last_4months(tweet):
    """helper function to return only tweets within last 4 months"""
    if tweet.created_at > datetime.now() - timedelta(days=120):
        senti = sentiment(preprocess(tweet.full_text))
    return senti

def tweet_user(username,max_tweets):
    """Extracting user information"""
    # Creation of query method using parameters
    tweets = tweepy.Cursor(api.user_timeline,id=username,tweet_mode = 'extended').items(max_tweets)

    tweets_list = [sentiment(preprocess(tweet.full_text)) for tweet in tweets]
    if max_tweets == 1:
        for tweet in tweets_list:
            return float(tweet)
    if max_tweets > 1:
        sentiment_pattern = [0 if tweet < 0 else 1 for tweet in tweets_list]
        return str(sentiment_pattern)

def tweet_user_updated(username,max_tweets):
    """returns latest tweets( not older than yesterday) or tweet pattern for no. of tweets given in max_tweets"""
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(max_tweets)
    if max_tweets == 1:
        # (datetime.datetime.now() - tweet.created_at).days < 1
        tweet = [[sentiment(preprocess(tweet.full_text)) if tweet.created_at > datetime.now() - timedelta(days= 1) else 0] for tweet in tweets]
        return float(tweet[0][0])
    if max_tweets > 1:
        #returns tweet pattern upto last 4 months
        tweets_list = [tweet_pattern_in_last_4months(tweet) for tweet in tweets]
        sentiment_pattern = [-1 if tweet < 0 else 1 for tweet in tweets_list]
        return str(sentiment_pattern)

api = twitter_api()

if __name__ == '__main__':
    a = tweet_user_updated("@PMOIndia",15)
#     a = tweet_user("@rajatpaliwal319", 1)
    print(a)
