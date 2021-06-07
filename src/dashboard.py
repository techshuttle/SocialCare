import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from db_utils import read_name_sentiment_add_pattern
df = read_name_sentiment_add_pattern()

employees = df['name'].to_list()
tweet = ["Latest Tweet",2,3,4,5,6,7,8,9,10,11,12,13,14,"15th"]
df["sentiment_binary"] = df["sentiment"].apply(lambda x: "negative" if x < 0 else "positive")
day_sentiment_counts = df['sentiment_binary'].value_counts()
data_heatmap = df['sentiment_pattern'].apply(eval).to_list()

app = dash.Dash(__name__)

#Import and clean data (importing csv into pandas)

# pie chart
day_sentiment_counts = df['sentiment_binary'].value_counts()
print(day_sentiment_counts)
fig_pie = px.pie(names = day_sentiment_counts.index,values = day_sentiment_counts.values,color = day_sentiment_counts.index, hole = 0.5)
fig_pie.update_traces(textinfo="label + percent",insidetextfont =dict(color = "white") )
fig_pie.update_layout(legend= {"itemclick":False})
# fig_pie.show()

#bar graph
fig_bar = px.bar(
    data_frame= df,
    x = 'name',
    y = 'sentiment',
    opacity= 0.9,
    orientation="v",
    barmode= 'relative',
)
#title = "Updated Tweet Sentiment"
# pio.show(fig_bar)

#heatmap
fig_heatmap = px.imshow(data_heatmap,
                color_continuous_scale=px.colors.sequential.Cividis_r,
                title = "15 tweet sentiment pattern",
                labels = dict(x = "Tweet index", y = "Names"),
                x= tweet,
                y = employees)
fig_heatmap.update_xaxes(side= "top")

app.layout = html.Div(children=[
    #
    html.Div([
        html.H1(children="Pattern of last 15 tweets"),

        html.Div(children= """
        The pattern will tell us about the positive and negative sentiments.
        """),

        dcc.Graph(
            id = 'graph1',
            figure = fig_heatmap
        )
    ]),

#New division for all elements in the new 'row' of the page
    html.Div([
        html.H1(children="Today's sentiments"),
        html.Div(children="""
        Polarity of the sentiment
        """),

        dcc.Graph(
            id = 'graph2',
            figure = fig_bar
        ),
        ]),

    html.Div([
        html.H1(children="Pie Chart"),
        html.Div(children="""
        Insights on tweets with positive and negative sentiment
        """),

        dcc.Graph(
            id = 'graph3',
            figure = fig_pie
            ),
        ]),
    ])


# print(df[:5])
#
# data = df['sentiment_pattern'].apply(eval).to_list()
# # fig = px.density_heatmap(df, x = data ,y = "name")
# # fig.show()
# #
# # trace = go.Heatmap(
# #     x =
# # )
# # print(df_1)
#
# #_____________________________________________________________________________________________
# #App layout - dash components, graphs, checkbox and any html we need.
# # H1 = Title, dcc.Dropdown have parameters for dropdown ie
# #
# # app.layout = html.Div([
# #     html.H1("Web Application with Dashboards with Dash", style = {'text-align':'center'}),
# #
# #     dcc.Dropdown(id = "slct_year",
# #                  options = [
# #                      {"label":"2015", "value":2015},
# #                      {"label":"2016", "value":2016},
# #                      {"label":"2017", "value":2017},
# #                      {"label":"2018", "value":2018}],
# #                  multi = False,
# #                  value = 2015,
# #                  style = {'width':"40%"}),
# #
# #     html.Div(id = 'output_container', children= []),
# #     html.Br(),
# #
# #     dcc.Graph(id = 'my_bee_map', figure = {})])
# # #___________________________________________________________________________________
# # #Connect the Plotly graphs with Dash Components
# #
# # @app.callback(
# #     [Output(component_id='output_container',component_property='children'),
# #      Output(component_id='my_bee_map', component_property='figure')],
# #     [Input(component_id='slct_year',component_property='value')]
# #     )
# #
# # def update_graph(option_slctd):
# #     print(option_slctd)
# #     print(type(option_slctd))
# #
# #     container = "The year chosen by the user was: {}".format(option_slctd)
# #
# #     dff = df.copy()
# #     dff = dff[[" == option_slctd]
# #     dff = dff[dff["Affected by"] == "Varroa-mites"]
# #
# #     #Plotly Express
# #     # fig = px.choropleth(
# #     #     data_frame = dff,
# #     #     locationmode= 'USA-states',
# #     #     locations='state_code',
# #     #     scope="usa",
# #     #     color='Pct of Colonies Impacted',
# #     #     hover_data=['State','Pct of Colonies Impacted'],
# #     #     color_continuous_scale=px.colors.sequential.YlOrRd,
# #     #     labels={'Pct of Colonies Impacted':'% of Bee Colonies'},
# #     #     template='plotly_dark'
# #     # )
# #
# #     fig = px.bar(
# #         data_frame = dff,
# #         x = 'State',
# #         y= 'Pct of Colonies Impacted',
# #         hover_data= ['State','Pct of Colonies Impacted'],
# #         labels= {'Pct of Colonies Impacted':'% of Bee Colonies'},
# #         template= 'plotly_dark'
# #     )
# #
# #     # #Plotly Graph Objects (GO)
# #     # fig = go.Figure(
# #     #     data=[go.Choropleth(
# #     #         locationmode='USA-states',
# #     #         locations= dff['state_code'],
# #     #         z = dff["Pct of Colonies Impacted"].astype(float),
# #     #         colorscale= 'Reds',
# #     #
# #     #     )]
# #     # )
# #     # #
# #     # fig.update_layout(
# #     #     title_text = "bees Affected by Mites in the USA",
# #     #     title_xanchor= "center",
# #     #     title_font = dict(size=24),
# #     #     title_x= 0.5,
# #     #     geo=dict(scope='usa'),
# #     # )
# #
# #     return container, fig
# #
# #
# #
# #
# #
if __name__ == "__main__":
    app.run_server(debug=True)