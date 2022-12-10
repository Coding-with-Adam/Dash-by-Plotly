# Video: [Introduction to MongoDB with Plotly Dash](https://www.youtube.com/watch?v=2pWwSm6X24o)

import dash     # need Dash version 1.21.0 or higher
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_table
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, callback             # , ctx # "ctx" is not accessed (Pylance)
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px
from bson import ObjectId           # pip install bson
import pymongo                      # pip install pymongo
from pymongo import MongoClient
# from .utils import id
						   
# [Examples of multi-page apps with Dash Pages](https://community.plotly.com/t/examples-of-multi-page-apps-with-dash-pages/66489/8):
# from .utils import id
def id(name, localid):
    # return f"{name.replace('.', '-').replace(' ', '-').replace('_', '-').replace('.py', '').replace('/', '')}-{localid}"
	return localid

# dash.register_page(__name__, path="/mongo-databases")

# Connect to local server
client = MongoClient("mongodb://127.0.0.1:27017/")

# List collections available per database
all_options = {
    _: client[_].list_collection_names()
    for _ in [db["name"] for db in client.list_databases()]
}
print(f'{all_options=}')

# app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

layout = html.Div([
    dbc.Form(
        [
            dbc.Row(
                [
                    dbc.Label("Database", html_for="database-row", width=2),
                    dcc.Dropdown(
                        id=id(__name__,'database-dropdown'),
                        options=[{'label': k, 'value': k} for k in all_options.keys()]
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Label("Collection (table)", html_for="collection-row", width=2),
                    dcc.Dropdown(id=id(__name__,'collection-dropdown')),
                ],
                className="mb-3",
            ),
        ]
    ),

    html.Hr(),
    html.Div(id=id(__name__,"datatable-div"), children=[ # To be filled in
        # populate_datatable(n_itvl):
        #   return [ dash_table.DataTable(id=id(__name__,"datatable"), columns=[...], data=df.to_dict('records'), ...) ]
    ]),
    html.Hr(),

    # activated once/week or when page refreshed
    dcc.Interval(id=id(__name__,"interval_db"), interval=86400000 * 7, n_intervals=0),

    html.Button("Save to Mongo Database", id=id(__name__,"save-it")),
    html.Button('Add Row', id=id(__name__,"adding-rows-btn"), n_clicks=0),

    # html.Div(id=id(__name__,"show-graphs"), children=[]),
    html.Div(id=id(__name__,"placeholder"))

])

# rf.   [dash-three-cascading-dropdowns.py](https://github.com/plotly/dash-recipes/blob/master/dash-three-cascading-dropdowns.py)

@callback(
    dash.dependencies.Output(id(__name__,'collection-dropdown'), 'options'),
    [dash.dependencies.Input(id(__name__,'database-dropdown'), 'value')])
def set_collection_options(selected_database):
    if selected_database==None:
        return []
    return [{'label': i, 'value': i} for i in all_options[selected_database]]


@callback(
    dash.dependencies.Output(id(__name__,'collection-dropdown'), 'value'),
    [dash.dependencies.Input(id(__name__,'collection-dropdown'), 'options')])
def set_collection_value(available_options):
    if len(available_options)==0:
        return None
    return available_options[0]['value']


def database_collection_by_names(database_name, collection_name):
    if not database_name:
        print(f'Unable to access database "{database_name}"')
        return None
    # Create database called f'{database_name}'
    database = client[database_name]
    if not collection_name:
        print(f'Unable to access collection "{collection_name}"')
        return None
    # Create Collection (in NoSql rather than RDBMS' tables) called f'{collection_name}'
    collection = database[collection_name]
    print(f'selected collection "{collection_name}" of database "{database_name}"')
    return collection

# Display Datatable with data from Mongo database *************************
@callback(Output(id(__name__,"datatable-div"), 'children'),
          [
            Input(id(__name__,"database-dropdown"), 'value'),
            Input(id(__name__,"collection-dropdown"), 'value'),
            Input(id(__name__,"interval_db"), 'n_intervals'),
          ])
def populate_datatable(database_name, collection_name, n_intervals):
    print(n_intervals)
    collection = database_collection_by_names(database_name, collection_name)
    if collection==None:
        print("collection==None")
        return None
    results = list(collection.find())
    if len(results)==0:
        print("Empty Cursor")
        return []
    
    # Convert the Collection (in NoSql rather than RDBMS' tables) date to a pandas DataFrame
    df = pd.DataFrame(results)
    #Drop the _id column generated automatically by Mongo
    df = df.iloc[:, 1:]
    print(df.head(20))

    return [
        dash_table.DataTable(
            id=id(__name__,"datatable"),
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
    Output(id(__name__,"datatable"), 'data'),
    [Input(id(__name__,"adding-rows-btn"), 'n_clicks')],
    [State(id(__name__,"datatable"), 'data'),
     State(id(__name__,"datatable"), 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the Mongo database ***************************
@callback(
    Output(id(__name__,"placeholder"), "children"),
    [
        Input(id(__name__,"save-it"), "n_clicks"),
        Input(id(__name__,"database-dropdown"), 'value'),
        Input(id(__name__,"collection-dropdown"), 'value'),
    ],
    State(id(__name__,"datatable"), "data"),
    prevent_initial_call=True
)
def save_data(n_clicks, database_name, collection_name, data):
    collection = database_collection_by_names(database_name, collection_name)
    if collection==None:
        print("collection==None")
        return None
    results = list(collection.find())
    if len(results)==0:
        print("Empty Cursor")
        return []
    dff = pd.DataFrame(data)
    collection.delete_many({})
    collection.insert_many(dff.to_dict('records'))
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
