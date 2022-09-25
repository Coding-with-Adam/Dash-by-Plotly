from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import math

# Data source: https://www.ncei.noaa.gov/access/billions/time-series/US
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Dash%20Components/Slider/severe-storms.csv")

rangeslider_marks = {0:'$0', 5:'$5 billion', 10:'$10 billion', 15:'$15 billion', 20:'$20 billion',
                     25:'$25 billion', 30:'$30 billion', 35:'$35 billion', 40:'$40 billion'}

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Severe Storms Analysis in the USA", style={'textAlign': 'center'}),

        html.Label("Number of Severe Storms"),
        dcc.Slider(min=df['Severe Storm Count'].min(),
                   max=df['Severe Storm Count'].max(),
                   step=1,
                   value=13,
                   tooltip={"placement": "bottom", "always_visible": True},
                   updatemode='drag',
                   persistence=True,
                   persistence_type='session', # 'memory' or 'local'
                   id="my-slider"
        ),

        html.Label("Severe Storm Costs ($ Billions)"),
        dcc.RangeSlider(min=df['Severe Storm Costs (Billions)'].min(),
                        max=math.ceil(df['Severe Storm Costs (Billions)'].max()),
                        step=1,
                        marks=rangeslider_marks,
                        value=[0,10],
                        tooltip={"placement": "bottom", "always_visible": True},
                        updatemode='drag',
                        id="my-rangeslider"
        ),

        dcc.Graph(id='my-graph')
    ],
    style={"margin": 30}
)


@app.callback(
    Output('my-graph', 'figure'),
    Input('my-slider', 'value'),
    Input('my-rangeslider', 'value')
)
def update_graph(n_storms, dollar_range):
    bool_series = df['Severe Storm Count'].between(0, n_storms, inclusive='both')
    df_filtered = df[bool_series]
    fig = px.bar(data_frame=df_filtered,
                 x='Year',
                 y='Severe Storm Count',
                 range_y=[df['Severe Storm Count'].min(), df['Severe Storm Count'].max()],
                 range_x=[df['Year'].min()-1, df['Year'].max()+1])

    bool_series2 = df['Severe Storm Costs (Billions)'].between(dollar_range[0], dollar_range[1], inclusive='both')
    filtered_year = df[bool_series2]['Year'].values
    fig["data"][0]["marker"]["color"] = ["orange" if c in filtered_year else "blue" for c in fig["data"][0]["x"]]

    return fig


if __name__ == "__main__":
    app.run(debug=True)
