
#twitter_functions

# #alternative to preprocessing (ligher function)
# def clean_tweet(tweet):
#     '''
#     Utility function to clean the text in a Tweet by removing
#     links and special characters using regex re.
#     '''
#     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



# def tweet_user_sentiment_type(username):
#     """tweet sentiment type. useful for wordclouds"""
#     sentiment = tweet_user_updated(username,1)
#     return -1 if sentiment < 0 else 1



# def tweet_user_key_phrase(username,max_tweets):
#     tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(max_tweets)
#     if max_tweets == 1:
#         tweet = [
#             [key_phrase_extraction(preprocess(tweet.full_text)) if tweet.created_at > datetime.now() - timedelta(days=7) else 0] for
#             tweet in tweets]
#     return tweet[0][0]



# def tweet_user_NER(username,max_tweets):
#     tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended').items(max_tweets)
#     if max_tweets == 1:
#         tweet = [
#             [named_entity_extraction(preprocess(tweet.full_text)) if tweet.created_at > datetime.now() - timedelta(
#                 days=7) else 0] for
#             tweet in tweets]
#     return tweet[0][0]

#

# #For employee info, with default max_tweets


# def read_employee_info(twitter_id):
#     """Reading id, name, sentiment and sentiment pattern of employee from the table"""
#     cursor.execute("SELECT id,name,tweet_sentiment,twitter_sentiment_pattern from Employee WHERE twitter_id = %s;",(twitter_id,))
#     employee = cursor.fetchall()
#     # print(employee)
#     # ilog.info(f"The sentiments of the employees are {employee}")
#     conn.commit()
#     return employee
#

#
# def add_quote(a):
#     return '"{0}"'.format(a)
# print(add_quote(5))
#
#Normal tweet analysis without time constraint

# def tweet_user(username,max_tweets):
#     """Extracting user sentiment information from tweets"""
#     # Creation of query method using parameters
#     tweets = tweepy.Cursor(api.user_timeline,id=username,tweet_mode = 'extended').items(max_tweets)
#
#     tweets_list = [sentiment(preprocess(tweet.full_text)) for tweet in tweets]
#     if max_tweets == 1:
#         for tweet in tweets_list:
#             return float(tweet)
#     if max_tweets > 1:
#         sentiment_pattern = [0 if tweet < 0 else 1 for tweet in tweets_list]
#         return str(sentiment_pattern)

#tweet pattern within last 4 months

# def tweet_pattern_in_last_4months(tweet):
#     """helper function to return only tweets within last 4 months"""
#     if tweet.created_at > datetime.now() - timedelta(days=120):
#         senti = sentiment(preprocess(tweet.full_text))
#     return senti



### to get query result as json
#
def query_db(query,args=(), one=False):
    """returns table in a list of dicts"""
    # query = "SELECT * FROM Employee"
    cursor.execute(query, args)
    try:
        r = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"{e}")
    # cursor.connection.close()
    logger.info(f"{r} successful")
    return (r[0] if r else None) if one else r


######################################################Tweet NER#########################################################
#
# def update_tweet_NER(twitter_id):
#     """to add Named Entity Recognition values related to the tweet"""
#     try:
#         tweet_NER = (tweet_user_NER(twitter_id,1))
#     # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
#         print(tweet_NER)
#
#         sentiment = cursor.execute("""UPDATE Employee SET ner = %s WHERE twitter_id = %s """,(tweet_NER, twitter_id ))
#         logger.info(f"twitter NER for {twitter_id} updated successfully")
#     except Exception as error:
#         logger.error(f"{error}")
#         return print(error)
#     return 1
#
# # print(update_tweet_NER("@TheEconomist"))
#
# def update_tweet_ner_from_ids():
#     """updating and checking the update of NER for the user"""
#     s = "SELECT twitter_id FROM Employee"
#     cursor.execute(s)
#     twitter_ids = cursor.fetchall()
#     logger.info(f"{twitter_ids}")
#     conn.commit()
#     try:
#         list = [update_tweet_NER(id[0]) for id in twitter_ids]
#         print(list)
#         logger.info(f"list of updated twitter sentiments - {list}")
#         return list
#     except Exception as e:
#         print(e)
#         return 0

# print(update_tweet_ner_from_ids())

####################################Key_Phrase#####################################################################
# def update_tweet_key_phrase(twitter_id):
#     """To update Key phrase used in the tweet.Provides useful information about the tweet."""
#     try:
#         tweet_key_phrase = (tweet_user_key_phrase(twitter_id,1))
#         # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
#         print(tweet_key_phrase)
#
#         sentiment = cursor.execute("""UPDATE Employee SET key_phrase = %s WHERE twitter_id = %s """,(tweet_key_phrase, twitter_id,))
#         logger.info(f"twitter key phrase for {twitter_id} updated successfully")
#     except Exception as error:
#         logger.error(f"{error}")
#         return print(error)
#     return 1


# def update_tweet_key_phrase_from_ids():
#     """updating and checking the update of tweet key phrases for the user"""
#     s = "SELECT twitter_id FROM Employee"
#     cursor.execute(s)
#     twitter_ids = cursor.fetchall()
#     logger.info(f"{twitter_ids}")
#     conn.commit()
#     try:
#         list = [update_tweet_key_phrase(id[0]) for id in twitter_ids]
#         print(list)
#         logger.info(f"list of updated twitter key phrases - {list}")
#         return list
#     except Exception as e:
#         print(e)
#         return 0

# print(update_tweet_key_phrase_from_ids())