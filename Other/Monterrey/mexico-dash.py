from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# https://www.kaggle.com/datasets/tsarina/mexico-city-airbnb?select=listings1.csv
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Monterrey/airbnb.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# night_slider = dcc.Slider(1, 30, 1, value=1)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([dcc.Markdown('# Análisis de Airbnb de México DF', style={'textAlign': 'center'})], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('#### Select minimum Nights'),
            night_slider := dcc.Slider(1, 30, 1, value=1)
        ], width=6),
        dbc.Col([
            dcc.Markdown('#### Select price range'),
            price_slider := dcc.RangeSlider(min=df.price.min(), max=df.price.max(), value=[0, 10000], step=1000,
                                            marks={'0': '0', '10000': '10000', '20000': '20000', '30000': '30000',
                                                   '40000': '40000', '50000': '50000'},
                                            tooltip={"placement": "bottom", "always_visible": True})
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            sg := html.Div()
        ], width=12)
    ])
])


@app.callback(
    Output(sg, component_property='children'),
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
                            range_color=[0, 1000], zoom=11, color_continuous_scale=px.colors.sequential.Sunset,
                            hover_data={'latitude': False, 'longitude': False, 'room_type': True,
                                        'minimum_nights': True})
    fig.update_layout(mapbox_style='open-street-map')

    # 1. add room_type dropdown to the layout and callback function
    # 2. return a dbc.Alert() if dff is empty (o sea, if len(dff)==0)

    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run_server(debug=True)
