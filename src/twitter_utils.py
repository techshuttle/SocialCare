import os
import tweepy
import config
import pandas as pd
import sys
import numpy as np
# import re
import time

from datetime import datetime,timedelta
from expertai_utils import sentiment, key_phrase_extraction, named_entity_extraction
from text_preprocess import preprocess


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

# def tweet_pattern_in_last_4months(tweet):
#     """helper function to return only tweets within last 4 months"""
#     if tweet.created_at > datetime.now() - timedelta(days=120):
#         senti = sentiment(preprocess(tweet.full_text))
#     return senti


def tweet_user_updated(username,max_tweets):
    """returns latest tweets( not older than yesterday) or tweet pattern for no. of tweets given in max_tweets"""
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(max_tweets)
    if max_tweets == 1:
        tweet = [[sentiment(preprocess(tweet.full_text)) if tweet.created_at > datetime.now() - timedelta(days= 7) else 0] for tweet in tweets]
        return float(tweet[0][0])
    if max_tweets > 1:
        #returns tweet pattern upto last 4 months
        tweets_list = [sentiment(preprocess(tweet.full_text)) for tweet in tweets]
        sentiment_pattern = [-1 if tweet < 0 else 1 for tweet in tweets_list]
        return str(sentiment_pattern)

def tweet_user_key_phrase(username,max_tweets):
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(max_tweets)
    if max_tweets == 1:
        tweet = [
            [key_phrase_extraction(preprocess(tweet.full_text)) if tweet.created_at > datetime.now() - timedelta(days=7) else 0] for
            tweet in tweets]
    return tweet[0][0]

def tweet_user_NER(username,max_tweets):
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(max_tweets)
    if max_tweets == 1:
        tweet = [
            [named_entity_extraction(preprocess(tweet.full_text)) if tweet.created_at > datetime.now() - timedelta(
                days=7) else 0] for
            tweet in tweets]
    return tweet[0][0]


# functions added on June 9,2021

api = twitter_api()

if __name__ == '__main__':
    name = "@ArianaGrande"
    a = tweet_user_updated(name ,10)
    b = tweet_user_key_phrase(name,1)
    c = tweet_user_NER(name,1)
#     a = tweet_user("@rajatpaliwal319", 1)
#     print(c)
