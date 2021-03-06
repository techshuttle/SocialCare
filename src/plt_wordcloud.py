import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from src.text_preprocess import preprocess


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
    wc = WordCloud(background_color="white",stopwords=stopwords,random_state = 2016).generate(" ".join([i for i in tweets.str.upper()]))
    plt.imshow(wc)
    plt.axis("off")
    plt.title(title)
    wc_img = wc.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer,'png')
        img2 = base64.b64encode(buffer.getvalue()).decode()
    return img2

#wordclouds



# Reference - https://www.kaggle.com/jagangupta/wordcloud-of-tweets
