import os
# from tweepy import API,Cursor,OAuthHandler,Stream
import tweepy
import config
import pandas as pd
import sys
import numpy as np
# import re
import time
from datetime import datetime,timedelta
# start_time = datetime.now()

from src.expertai_utils import sentiment
from src.expertai_utils import resource_concept_score_analysis as rcsa
from src.text_preprocess import preprocess


"""authentication function"""

def twitter_api():
    """to utilize twitter api using the key and token from twitter developer account"""
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


def user_tweet_today(username):
    """to extract the latest tweet from a user timeline"""
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(1)
    tweet = [[preprocess(tweet.full_text) if tweet.created_at > datetime.now()- timedelta(days=7) else 0] for tweet in tweets]
    return tweet[0][0]


def tweet_user_updated(username,max_tweets):
    """returns latest tweets( not older than yesterday) or tweet pattern for no. of tweets given in max_tweets"""
    start = time.time()
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(max_tweets)
    if max_tweets == 1:
        tweet = [[sentiment(preprocess(tweet.full_text)) if tweet.created_at > datetime.now() - timedelta(days= 7) else 0] for tweet in tweets]
        end = time.time()
        # print("for 1 tweet", end - start)
        return float(tweet[0][0])
    if max_tweets > 1:
        #returns tweet pattern upto last 4 months
        tweets_list = [sentiment(preprocess(tweet.full_text)) for tweet in tweets]
        sentiment_pattern = [-1 if tweet < 0 else 1 for tweet in tweets_list]
        end = time.time()
        print(f"for {max_tweets} tweets: ",end - start)
        return str(sentiment_pattern)



def tweet_user_RCSA(username,max_tweets):
    """Resource Concept Score Analysis """
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(max_tweets)
    if max_tweets == 1:
        tweet = [
            [rcsa(preprocess(tweet.full_text)) if tweet.created_at > datetime.now() - timedelta(
                days=7) else 0] for
            tweet in tweets]
    return tweet[0][0]

api = twitter_api()

