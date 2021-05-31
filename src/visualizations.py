import matplotlib.pyplot as plt
#pie chart
"""df with name, id, sentiment.
use pie chart."""
from db_utils import read_name_sentiment
df = read_name_sentiment()
df["sentiment_binary"] = df["sentiment"].apply(lambda x: 0 if x < 0 else 1)



def pie_chart():
    fig = plt.figure(figsize = (10,7))
    plt.pie(df["sentiment_binary"].value_counts(), labels = ["Positive","Negative"])
    plt.show()

print(pie_chart())



# import plotly.express as px
# import pandas as pd
# fig = px.bar(df,x = "name", y = "sentiment_binary", title = "graph" )
# fig.show()


data = df['sentiment'].apply(lambda x: int(x))
data_list = data.to_list()




def show_sentiment_today():
    import matplotlib.pyplot as plt;
    plt.rcdefaults()
    import numpy as np

    objects = df['name'].to_list()
    y_pos = np.arange(len(objects))
    performance = df["sentiment"].apply(lambda x: int(x)).to_list()[:6]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Polarity')
    plt.title('Tweet Sentiments Today')
    plt.show()



def show_sentiment_today_fancy():
    import matplotlib.pyplot as plt
    plt.rcdefaults()
    import numpy as np

    objects = df['name'].to_list()
    y_pos = np.arange(len(objects))
    performance = df["sentiment"].apply(lambda x: int(x)).to_list()[:6]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    # Get the axes object
    ax = plt.gca()
    # remove the existing ticklabels
    ax.set_xticklabels([])
    # remove the extra tick on the negative bar
    ax.set_xticks([idx for (idx, x) in enumerate(performance) if x > 0])
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # placing each of the x-axis labels individually
    label_offset = 0.5
    for language, (x_position, y_position) in zip(objects, enumerate(performance)):
        if y_position > 0:
            label_y = -label_offset
        else:
            label_y = y_position - label_offset
        ax.text(x_position, label_y, language, ha="center", va="top")
    # Placing the x-axis label, note the transformation into `Axes` co-ordinates
    # previously data co-ordinates for the x ticklabels
    ax.text(0.5, -0.05, "Usage", ha="center", va="top", transform=ax.transAxes)

    plt.show()

# show_sentiment_today_fancy()