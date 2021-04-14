import dash                              # pip install dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
from datetime import date


# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='/assets/linkedin-logo2.png')
            ],className='mb-2'),
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=8),
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=2),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
], fluid=True)



if __name__=='__main__':
    app.run_server(debug=False)
