# import libraries
import datetime
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader as pdr    # https://pandas-datareader.readthedocs.io/

# # set time window
# start = datetime.datetime(2020,1,1)
# end = datetime.datetime(2020,12,31)

# # load data from pandas_datareader
# df = pdr.data.DataReader(['AMZN', 'GOOGL', 'FB', 'PFE', 'BNTX', 'MRNA'],
#                          'stooq', start=start, end=end)
# df = df.stack().reset_index()
# print(df[:15])

# df.to_csv("mystocks.csv", index=False)

# load saved data
df = pd.read_csv("mystocks.csv")

# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.SIMPLEX],
                metadata=[
                    {
                        'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'
                    }
                ])

# Layout for app https://hackerthemes.com/bootstrap-cheatsheet/
# ------------------------------
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("DecisionNerd's Stock Market")
        )
    ]),
    dbc.Row([
        
    ]),
    dbc.Row([
        
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8181)