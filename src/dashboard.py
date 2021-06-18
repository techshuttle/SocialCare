import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud,STOPWORDS
from src.plt_wordcloud import wordcloud_by_tweets

from src.db_utils import read_name_sentiment_add_pattern
df = read_name_sentiment_add_pattern()

from src.db_utils import read_name_tweet_ner_key_phrase
df_tweets = read_name_tweet_ner_key_phrase()
# df_tweets=df_tweets.fillna("no tweet today")
STOPWORDS = ["https", "co", "RT","S","LA","T","ALWAYS"] + list(STOPWORDS)

import matplotlib.pyplot as plt
#wordcloud
word_cloud = wordcloud_by_tweets(df_tweets['tweet'],"Sentiment")
word_cloud


#heatmap
# fig_heatmap = px.imshow(data_heatmap,
#                 color_continuous_scale=px.colors.sequential.Emrld,
#                 title = "15 tweet sentiment pattern",
#                 labels = dict(x = "Tweet index", y = "Names"),
#                 x= tweet,
#                 y = employees)
# fig_heatmap.update_xaxes(side= "top")



#for pie chart
try:
    df["sentiment_binary"] = df["tweet_sentiment"].apply(lambda x: "negative" if x < 0 else "positive")
    day_sentiment_counts = df['sentiment_binary'].value_counts()

    # # pie chart
    fig_pie = px.pie(names = day_sentiment_counts.index,values = day_sentiment_counts.values,color = day_sentiment_counts.index, hole = 0.5)
    fig_pie.update_traces(textinfo="label + percent",insidetextfont =dict(color = "white") )
    fig_pie.update_layout(legend= {"itemclick":False})
except Exception as e:
    print("please add data")
#bar graph
fig_bar = px.bar(
    data_frame= df,
    x = 'name',
    y = 'tweet_sentiment',
    opacity= 0.9,
    orientation="v",
    barmode= 'relative',
    title="Updated Tweet Sentiment"
)


app = dash.Dash(__name__)


def create_dash_application(flask_app):
    dash_app = dash.Dash(
        server=flask_app,name="Dashboard",
        url_base_pathname='/dash/')

    dash_app.layout = html.Div(children=[
        #
        html.Div([
            html.H1(children="Pattern of last 15 tweets"),

            html.Div(children="""
            The pattern will tell us about the positive and negative sentiments.
            """),

            dcc.Graph(
                id='graph1',
                figure=fig_bar
            )
        ]),

        # New division for all elements in the new 'row' of the page
        html.Div([
            html.H1(children="Today's sentiments"),
            html.Div(children="""
            Polarity of the sentiment
            """),

            dcc.Graph(
                id='graph2',
                figure=fig_bar
            ),
        ]),

        html.Div([
            html.H1(children="Pie Chart"),
            html.Div(children="""
            Insights on tweets with positive and negative sentiment
            """),

            dcc.Graph(
                id='graph3',
                figure=fig_pie
            ),
        ]),
        html.Div([
            html.H1(children="WordCloud"),
            html.Div(
                children=[html.Img(src="data:image/png;base64," + word_cloud, style={'height': '60%', 'width': '60%'})])
        ])
        ])



    return dash_app