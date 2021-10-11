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
print(df[:15])