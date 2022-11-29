# Video: [Introduction to MongoDB with Plotly Dash](https://www.youtube.com/watch?v=2pWwSm6X24o)

import dash     # need Dash version 1.21.0 or higher
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_table

import pandas as pd
import plotly.express as px
import pymongo
from pymongo import MongoClient     # pip install pymongo
from bson import ObjectId           # pip install bson
					   
# [Examples of multi-page apps with Dash Pages](https://community.plotly.com/t/examples-of-multi-page-apps-with-dash-pages/66489/8):
# from .utils import id
def id(name, localid):
    return f"{name.replace('.', '-').replace(' ', '-').replace('_', '-').replace('.py', '').replace('/', '')}-{localid}"


dash.register_page(__name__, path="/mongo-dash-datatable")


# Connect to local server
client = MongoClient("mongodb://127.0.0.1:27017/")
# Create database called animals
mydb = client["animals"]
# Create Collection (table) called shelterA
collection = mydb.shelterA


# app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

layout = html.Div([

    html.Div(id=id(__name__,"datatable-div"), children=[ # To be filled in
        # populate_datatable(n_itvl):
        #   return [ dash_table.DataTable(id=id(__name__,"datatable"), columns=[...], data=df.to_dict('records'), ...) ]
    ]),

    # activated once/week or when page refreshed
    dcc.Interval(id=id(__name__,"interval_db"), interval=86400000 * 7, n_intervals=0),

    html.Button("Save to Mongo Database", id=id(__name__,"save-it")),
    html.Button('Add Row', id=id(__name__,"adding-rows-btn"), n_clicks=0),

    html.Div(id=id(__name__,"show-graphs"), children=[]),
    html.Div(id=id(__name__,"placeholder"))

])

# Display Datatable with data from Mongo database *************************
@callback(Output(id(__name__,"datatable-div"), 'children'),
              [Input(id(__name__,"interval_db"), 'n_intervals')])
def populate_datatable(n_intervals):
    print(n_intervals)
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    #Drop the _id column generated automatically by Mongo
    df = df.iloc[:, 1:]
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='my-table', # id(__name__,"datatable") # FIXME: ID not found in layout
            columns=[{
                'name': x,
                'id': x,
            } for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_current=0,  # page number that user is on
            page_size=6,  # number of rows visible per page
            style_cell={'textAlign': 'left', 'minWidth': '100px',
                        'width': '100px', 'maxWidth': '100px'},
        )
    ]


# Add new rows to DataTable ***********************************************
@callback(
    Output('my-table', # id(__name__,"datatable")   # FIXME: ID not found in layout
           'data'),
    [Input(id(__name__,"adding-rows-btn"), 'n_clicks')],
    [State('my-table', # id(__name__,"datatable")   # FIXME: ID not found in layout
           'data'),
     State('my-table', # id(__name__,"datatable")   # FIXME: ID not found in layout
           'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the Mongo database ***************************
@callback(
    Output(id(__name__,"placeholder"), "children"), # FIXME: ID not found in layout
    Input(id(__name__,"save-it"), "n_clicks"),      # FIXME: ID not found in layout
    State('my-table', # id(__name__,"datatable")    # FIXME: ID not found in layout
          "data"),
    prevent_initial_call=True
)
def save_data(n_clicks, data):
    dff = pd.DataFrame(data)
    collection.delete_many({})
    collection.insert_many(dff.to_dict('records'))
    return ""


# Create graphs from DataTable data ***************************************
@callback(
    Output(id(__name__,"show-graphs"), 'children'), # FIXME: ID not found in layout
    Input('my-table', # id(__name__,"datatable")   # FIXME: ID not found in layout
          'data')
)
def add_row(data):
    df_grpah = pd.DataFrame(data)
    fig_hist1 = px.histogram(df_grpah, x='age',color="animal")
    fig_hist2 = px.histogram(df_grpah, x="neutered")
    return [
        html.Div(children=[dcc.Graph(figure=fig_hist1)], className="six columns"),
        html.Div(children=[dcc.Graph(figure=fig_hist2)], className="six columns")
    ]

