

#alternative to preprocessing (ligher function)
def clean_tweet(tweet):
    '''
    Utility function to clean the text in a Tweet by removing
    links and special characters using regex re.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


#For employee info, with default max_tweets
def read_employee_info(twitter_id):
    """Reading id, name, sentiment and sentiment pattern of employee from the table"""
    cursor.execute("SELECT id,name,tweet_sentiment,twitter_sentiment_pattern from Employee WHERE twitter_id = %s;",(twitter_id,))
    employee = cursor.fetchall()
    # print(employee)
    # ilog.info(f"The sentiments of the employees are {employee}")
    conn.commit()
    return employee

print(read_employee_info("@PMOIndia"))

