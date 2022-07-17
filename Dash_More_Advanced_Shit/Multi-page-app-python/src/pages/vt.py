import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


dash.register_page(__name__,
                   name = 'Vermont',
                   layout = dbc.Row([
                       dbc.Col([
                           dcc.Markdown(["# Information on Vermont.\n"
                                         "#### Interesting climate change data:"
                           ])
                       ], width=12)
                   ])
)
