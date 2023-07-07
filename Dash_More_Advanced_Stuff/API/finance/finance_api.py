import pandas as pd
import plotly
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# "pip install alpha_vantage" (if you haven't done so)
from alpha_vantage.timeseries import TimeSeries

#-------------------------------------------------------------------------------
# Set up initial key and financial category

key = '7FEDJMHY3CM2KPEC' # Your API Key
# https://github.com/RomelTorres/alpha_vantage
# Chose your output format or default to JSON (python dict)
ts = TimeSeries(key, output_format='pandas') # 'pandas' or 'json' or 'csv'

#-------------------------------------------------------------------------------
# (only for example purposes) Pull data from API and prepare it for plotting on line chart

# Get the data, returns a tuple
# ttm_data is a pandas dataframe, ttm_meta_data is a dict
# https://github.com/RomelTorres/alpha_vantage/blob/develop/alpha_vantage/timeseries.py
ttm_data, ttm_meta_data = ts.get_intraday(symbol='TTM',interval='1min', outputsize='compact')
print(ttm_meta_data)

df = ttm_data.copy()
print(df.head())

df=df.transpose()
print(df.head())

df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
                 "4. close":"close","5. volume":"volume"},inplace=True)
df=df.reset_index().rename(columns={'index': 'indicator'})
print(df.head())

df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
df = df[df['indicator']!='volume']
print(df[:15])

#-------------------------------------------------------------------------------
# Building our Web app and update financial data automatically

# app = dash.Dash(__name__)
# 
# app.layout = html.Div([
#     dcc.Interval(
#                 id='my_interval',
#                 n_intervals=0,       # number of times the interval was activated
#                 interval=120*1000,   # update every 2 minutes
#     ),
#     dcc.Graph(id="world_finance"),   # empty graph to be populated by line chart
# ])
# 
# #-------------------------------------------------------------------------------
# @app.callback(
#     Output(component_id='world_finance', component_property='figure'),
#     [Input(component_id='my_interval', component_property='n_intervals')]
# )
# def update_graph(n):
#     """Pull financial data from Alpha Vantage and update graph every 2 minutes"""
# 
#     ttm_data, ttm_meta_data = ts.get_intraday(symbol='TTM',interval='1min',outputsize='compact')
#     df = ttm_data.copy()
#     df=df.transpose()
#     df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
#                      "4. close":"close","5. volume":"volume"},inplace=True)
#     df=df.reset_index().rename(columns={'index': 'indicator'})
#     df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
#     df = df[df['indicator']!='volume']
#     print(df[:15])
# 
#     line_chart = px.line(
#                     data_frame=df,
#                     x='date',
#                     y='rate',
#                     color='indicator',
#                     title="Stock: {}".format(ttm_meta_data['2. Symbol'])
#                  )
#     return (line_chart)
# 
# #-------------------------------------------------------------------------------
# if __name__ == '__main__':
#     app.run_server(debug=True)
