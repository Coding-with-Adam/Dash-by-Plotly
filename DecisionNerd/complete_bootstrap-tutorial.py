# import libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader as pdr    # https://pandas-datareader.readthedocs.io/
import datetime

# set time window
start = datetime.datetime(2021,1,1)
end = datetime.now()
