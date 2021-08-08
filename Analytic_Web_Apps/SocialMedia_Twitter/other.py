import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd
import twitter  # pip install python-twitter
from app import app, api


# layout of second (trends) tab ******************************************
other_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("More Twitter analysis to come...")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter', figure={})
        ], width=6),
        dbc.Col([
            dcc.Graph(id='scatter2', figure={})
        ], width=6)
    ])
])