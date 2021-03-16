import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd

# global dataframe saved on the server
df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Callbacks/Client-side-callback/opsales1.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(
        id='clientside-content', children="Soon data will be here."
    ),
    dcc.Store(
        id='clientside-store-data', data={}
    ),
    dcc.Interval(
        id='serverside-interval',
        interval=2000,
        n_intervals=1
    ),
    dcc.Interval(
        id='clientside-interval',
        n_intervals=1,
        interval=25
    ),
])

# Serverside callback
@app.callback(
    Output('clientside-content', 'children'),
    Input('serverside-interval', 'n_intervals'),
)
def update_data(n_intervals):
    data = df.iloc[n_intervals]['Sales per customer']
    return data


# Clientside callback
# @app.callback(
#     Output('clientside-store-data', 'data'),
#     Input('serverside-interval', 'n_intervals'),
# )
# def update_store_data(n_intervals):
#     last_row = n_intervals*100
#     stored_data = df.iloc[0:last_row]
#     return stored_data.to_dict('records')
#
#
# app.clientside_callback(
#     """
#     function(n_intervals, data) {
#         if(data[n_intervals] === undefined) {
#             return '';
#         }
#         return data[n_intervals]['Sales per customer'];
#     }
#     """,
#     Output('clientside-content', 'children'),
#     Input('clientside-interval','n_intervals'),
#     State('clientside-store-data', 'data'),
# )


if __name__ == '__main__':
    app.run_server(debug=True, port=5559)

    
    
# https://youtu.be/wHUzUHTPfo0
