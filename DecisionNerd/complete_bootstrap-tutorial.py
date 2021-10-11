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

# set time window
start = datetime.datetime(2020,1,1)
end = datetime.datetime(2020,12,31)
