import matplotlib.pyplot as plt
from src.db_utils import read_name_tweet_ner_key_phrase
from wordcloud import WordCloud, STOPWORDS


from src.text_preprocess import preprocess
df = read_name_tweet_ner_key_phrase()
# print(df.isnull().sum())
df=df.fillna("no tweet today")

from src.db_utils import read_tweet_features_on_sentiment_type as df_divide
df_positive,df_negative = df_divide()
# print(df_negative[["tweet","sentiment_type"]])

# print(modified_df.isnull().sum())

# df['tweet'] = df['tweet'].str.upper()

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def wordcloud_by_tweets(tweets,title):
    stopwords = set(STOPWORDS)
    stopwords.add("https")
    stopwords.add("S")
    stopwords.add("END")
    stopwords.add("NEW")
    stopwords.add("ed")
    stopwords.add("RT")
    stopwords.add("THANK")
    stopwords.add("AMP")

    stopwords.add("lakh")
    wc = WordCloud(background_color="white",stopwords=stopwords,random_state = 2016).generate(" ".join([i for i in df['tweet'].str.upper()]))
    plt.imshow(wc)
    plt.axis("off")
    plt.title(title)
    wc_img = wc.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer,'png')
        img2 = base64.b64encode(buffer.getvalue()).decode()
    return img2

#wordclouds

# wordcloud_by_tweets(df,"overall")
# wordcloud_by_tweets(df_positive,"positive")
# wordcloud_by_tweets(df_negative,"negative")
# plt.show()

# Reference - https://www.kaggle.com/jagangupta/wordcloud-of-tweets
import re
#
# tweet_tok.enizer = TweetTokenizer()
#
# text = df["tweet"].to_list()
# try:
#     tweet_tokens = []
#     for sent in text:
#         print(tweet_tokenizer.tokenize(sent))
#         tweet_tokens.append(tweet_tokenizer.tokenize(sent))
#     print(type(tweet_tokens))
# except Exception as e:
#     print(e)



# wordcloud = WordCloud().generate(str(text))
#
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()
# print(wordcloud)

# raw_string = ''.join(tweets)
# print(raw_string)
# tweets = [t for t in tweets]
# print(tweets)
# tweets = [t.lower() for t in tweets]
#
# tweets = [t for t in tweets if t not in STOPWORDS]
# print(tweets)
# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
#
# mask = np.array(Image.open('Logo-Twitter.jpg'))
#
# wc = WordCloud(background_color = "white", max_words = 200,
#                )
# clean_string = ','.join(tweets)
# wc.generate(clean_string)
#
# #Image
#
# f = plt.figure(figsize = (50,50))
# f.add_subplot(1,2,1)
# plt.imshow(mask,cmap=plt.cm.grey,interpolation= 'bilinear')
# plt.title("original Sketch",size = 40)
# plt.axis("off")
#
# f.add_subplot(1,2,2)
# plt.imshow(wc,interpolation="bilinear")
# plt.title("Twitter Generated Cloud",size = 40)
# plt.axis("off")
# plt.show()