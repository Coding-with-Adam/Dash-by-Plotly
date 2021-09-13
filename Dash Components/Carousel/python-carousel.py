from dash import Dash, Input, Output, html, dcc, callback # need version dash 2.0.0 or higher
# import plotly.express as px
# import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Our Cool Analytics Dashboard", style={"textAlign":"center"})
        ],width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Carousel(
                items=[
                    {"key": "1", "src": "/assets/Chapulin1.jpg", "caption":"My cat captions", "img_style":{"max-height":"500px"}},
                    {"key": "2", "src": "/assets/Chapulin2.jpg", "header":"My cat header", "img_style":{"max-height":"500px"}},
                    {"key": "3", "src": "/assets/Chapulin3.jpg", "img_style":{"max-height":"500px"}},
                ],
                controls=True,
                indicators=True,
                interval=2000,
                ride="carousel",
#                 className="carousel-fade"
            )
        ], width=8)
    ], justify="center"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H2("All my graphs and charts below", style={"textAlign":"center"}),
            dcc.Graph(figure={})
        ],width=12)    
    ])

])


if __name__ == '__main__':
    app.run_server(debug=False, port=8000)
