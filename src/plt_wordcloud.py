import matplotlib.pyplot as plt
# from src.db_utils import read_name_tweet_ner_key_phrase
from wordcloud import WordCloud, STOPWORDS


from src.text_preprocess import preprocess
# df = read_name_tweet_ner_key_phrase()
# # print(df.isnull().sum())
# df=df.fillna("no tweet today")
#
# from src.db_utils import read_tweet_features_on_sentiment_type as df_divide
# df_positive,df_negative = df_divide()


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
