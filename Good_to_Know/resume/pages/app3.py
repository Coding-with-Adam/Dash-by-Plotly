import dash
from dash import html
import dash_bootstrap_components as dbc
from .side_bar import sidebar

dash.register_page(__name__)

def layout():
    return html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    html.H3('App 3 - the best of all the apps', style={'textAlign':'center'}),
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
])
