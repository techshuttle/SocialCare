import re
# from nltk.stem import WordNetLemmatizer
# Cleaning the tweets
# def clean_tweet(tweet):
#     # remove links
#     tweet = re.sub(r'http\S+', '', tweet)
#     # remove mentions
#     tweet = re.sub("@\w+", "", tweet)
#     # alphanumeric and hashtags
#     tweet = re.sub("[^a-zA-Z#]", " ", tweet)
#     # remove multiple spaces
#     tweet = re.sub("\s+", " ", tweet)
#     tweet = tweet.lower()
#     # Lemmatize
#     # lemmatizer = WordNetLemmatizer()
#     # sent = ' '.join([lemmatizer.lemmatize(w) for w in tweet.split() if len(lemmatizer.lemmatize(w)) > 3])
#     return tweet

def preprocess(tweet):
    '''
    Utility function to clean the text in a Tweet by removing
    links and special characters using regex re.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# print(preprocess("Hello!###^&**(&^ Wow!"))