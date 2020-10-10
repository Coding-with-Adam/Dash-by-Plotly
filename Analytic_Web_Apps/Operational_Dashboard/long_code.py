import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

df = pd.read_csv('politics.csv')

# radioItem list for the layout
radio_list = [
    html.Div([
        html.Label('AZ-11: ', style={'display':'inline', 'fontSize':15}),
        dcc.RadioItems(
            id='radiolist-AZ',
            options=[
                {"label": "Dem", "value": "democrat"},
                {"label": "Rep", "value": "republican"},
                {"label": "NA", "value": "unsure"},
            ],
            value='unsure',
            inputStyle={'margin-left': '10px'},
            labelStyle={'display': 'inline-block'},
            style={'display':'inline'}
        ),
    ], style={'textAlign':'end'}),

    html.Div([
        html.Label('FL-29: ', style={'display':'inline'}),
        dcc.RadioItems(
            id='radiolist-FL',
            options=[
                {"label": "Dem", "value": "democrat"},
                {"label": "Rep", "value": "republican"},
                {"label": "NA", "value": "unsure"},
            ],
            value='unsure',
            inputStyle={'margin-left': '10px'},
            labelStyle={'display': 'inline-block'},
            style={'display':'inline'}
        ),
    ], style={'textAlign':'end'})
]

# Input list for the callback
input_list = [
    Input(component_id='radiolist-AZ', component_property='value'),
    Input(component_id='radiolist-FL', component_property='value'),
    Input(component_id='radiolist-GA', component_property='value')
]

# update dataframe according to chosen radioItem
dff.loc[dff.state == 'AZ', 'party'] = 'democrat' or 'republican' or 'unsure'
dff.loc[dff.state == 'FL', 'party'] = 'democrat' or 'republican' or 'unsure'
dff.loc[dff.state == 'GA', 'party'] = 'democrat' or 'republican' or 'unsure'
