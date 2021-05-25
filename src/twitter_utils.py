import tweepy
import config
import pandas as pd
import sys
import numpy as np
import re
from nltk.stem import WordNetLemmatizer
import time

from expertai.nlapi.cloud.client import ExpertAiClient
client = ExpertAiClient()

# from dotenv import load_dotenv
# load_dotenv()

import os
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


def tweet_user(username):
    """Extracting user information"""
    max_tweets = 1
    # Creation of query method using parameters
    tweets = tweepy.Cursor(api.user_timeline,id=username,tweet_mode = 'extended').items(max_tweets)
    # https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy
    # while True:
    #     try:
    #         new_tweet = tweets.next()
    #         #Insert into db
    #     except tweepy.TweepError:
    #         time.sleep(60 * 15)
    #         continue
    #     except StopIteration:
    #         break
    # tweets_list = [[sentiment(preprocess(tweet.full_text))] for tweet in tweets]
    # for tweet in tweets:
    #     return tweet

    tweets = [sentiment(preprocess(tweet.full_text)) for tweet in tweets]
    # return tweets
    for tweet in tweets:
        return float(tweet)

api = twitter_api()


if __name__ == '__main__':
    api = twitter_api()
    users = ['@rajatpaliwal319']
    for user in users:
        tweet_user(user)
        print(type(tweet_user(user)))

