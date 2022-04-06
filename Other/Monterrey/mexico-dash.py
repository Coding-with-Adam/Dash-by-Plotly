from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv("airbnb.csv")  # https://www.kaggle.com/datasets/tsarina/mexico-city-airbnb?select=listings1.csv
# print(type(df.price.min()))
# exit()
df.price = df.price.astype(int)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([dcc.Markdown('# Análisis de Airbnb de México DF')], width=10)
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            night_slider := dcc.Slider(1, 30, 1, value=1)
        ], width=4),
        dbc.Col([
            price_slider := dcc.RangeSlider(min=df.price.min(), max=df.price.max(), value=[0,10000], step=1000,
                                            marks={'0':'0', '10000':'10000', '20000':'20000', '30000':'30000', '40000':'40000', '50000':'50000'},
                                            tooltip={"placement": "bottom", "always_visible": True})
        ], width=4),
        dbc.Col([

        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            sg := dcc.Graph()], width=12)
    ]),
])

@app.callback(
    Output(sg, component_property='figure'),
    Input(night_slider, 'value'),
    Input(price_slider, 'value')
)
def update_graph(nights_value, prices_value):
    print(nights_value)
    print(prices_value)
    dff = df[df.minimum_nights >= nights_value]
    dff = dff[(dff.price > prices_value[0]) & (dff.price < prices_value[1])]
    print(len(dff))

    fig = px.scatter_mapbox(data_frame=dff, lat='latitude', lon='longitude', color='price',
                            range_color=[0, 1000], zoom=11,
                            hover_data={'latitude': False, 'longitude': False, 'room_type': True,
                                        'minimum_nights': True})
    fig.update_layout(mapbox_style='pen-street-map', margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


if __name__=='__main__':
    app.run_server(debug=True)
