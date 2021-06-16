

# #alternative to preprocessing (ligher function)
# def clean_tweet(tweet):
#     '''
#     Utility function to clean the text in a Tweet by removing
#     links and special characters using regex re.
#     '''
#     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
#
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
# print(read_employee_info("@PMOIndia"))
#
# def add_quote(a):
#     return '"{0}"'.format(a)
# print(add_quote(5))
#
#
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

# def tweet_pattern_in_last_4months(tweet):
#     """helper function to return only tweets within last 4 months"""
#     if tweet.created_at > datetime.now() - timedelta(days=120):
#         senti = sentiment(preprocess(tweet.full_text))
#     return senti


# def update_twitter_linkedin_sentiment(twitter_id,linkedin_sentiment = False):
#     tweet_sentiment = tweet_user_updated(twitter_id,1)
#     linkedin_sentiment = False
#     logger.info(f"{tweet_sentiment} to be updated")
#     try:
#         cursor.execute("INSERT INTO Employee (tweet_sentiment,linkedin_sentiment) VALUES (%f, %s)",(tweet_sentiment,linkedin_sentiment))
#         conn.commit()
#         tweet_sentiment = tweet_user_updated(twitter_id)
#         logger.info(f"twitter sentiment for id = {twitter_id} ie {tweet_sentiment} updated.")
#     except Exception as error:
#         logger.error(f"{error}")
#         return 0
#     return 1
#
