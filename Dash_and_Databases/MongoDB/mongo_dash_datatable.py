import dash     # need Dash version 1.21.0 or higher
from dash import dcc, html, Input, Output, State
import dash_table

import pandas as pd
import plotly.express as px
import pymongo
from pymongo import MongoClient
from bson import ObjectId




# Connect to local server
client = MongoClient("mongodb://127.0.0.1:27017/")
# Create database called animals
mydb = client["animals"]
# Create Collection (table) called shelterA
collection = mydb.shelterA


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Choose database
database_dropdown = dbc.Row(
    [
        dbc.Label("Database", html_for="database-row", width=2),
        dbc.Col(
            dcc.Dropdown(database_names, None, id='database-dropdown'),
            width=10,
        ),
    ],
    className="mb-3",
)
# Choose collection (table)
collection_dropdown = dbc.Row(
    [
        dbc.Label("Collection (table)", html_for="collection-row", width=2),
        dbc.Col(
            dcc.Dropdown(collection_names, None, id='collection-dropdown'),
            width=10,
        ),
    ],
    className="mb-3",
)

app.layout = html.Div([

    dbc.Form([database_dropdown, collection_dropdown]),
    html.Div(id=id(__name__,"placeholder")),

    html.Div(id='mongo-datatable', children=[]),

    # activated once/week or when page refreshed
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),

    html.Button("Save to Mongo Database", id="save-it"),
    html.Button('Add Row', id='adding-rows-btn', n_clicks=0),

    html.Div(id="show-graphs", children=[]),
    html.Div(id="placeholder")

])

# rf.   [Cascading dropdowns](https://community.plotly.com/t/cascading-dropdowns/48635) and
#       [dash-three-cascading-dropdowns.py](https://github.com/plotly/dash-recipes/blob/master/dash-three-cascading-dropdowns.py)
@callback(
    Output('collection-dropdown', 'children'), # TODO: Learn from links how to update available choices
    Input('database-dropdown', 'value')
)
def select_database(value):
    # return f'You have selected database {value}'
    # TODO: update choices for collections (tables)

    return


def database_collection_by_names(database_name, collection_name):
    if not database_name:
        print(f'Unable to access database "{database_name}"')
        return None
    # Create database called f'{database_name}'
    database = client[database_name]
    if not collection_name:
        print(f'Unable to access collection "{collection_name}"')
        return None
    # Create Collection (table) called f'{collection_name}'
    collection = database[collection_name]
    print(f'selected collection "{collection_name}" of database "{database_name}"')
    return collection

# Display Datatable with data from Mongo database *************************
@app.callback(Output('mongo-datatable', 'children'),
          [
            Input('database-dropdown', 'value'),
            Input('collection-dropdown', 'value'),
            Input(id(__name__,"interval_db"), 'n_intervals'),
          ])
def populate_datatable(database_name, collection_name, n_intervals):
    print(n_intervals)
    collection = database_collection_by_names(database_name, collection_name)
    if collection==None:
        return None
    # FIXME: ValueError: Value of 'x' is not the name of a column in 'data_frame'. Expected one of [] but received: age
    #        Empty DataFrame
    #        Columns: []
    #        Index: []
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    #Drop the _id column generated automatically by Mongo
    df = df.iloc[:, 1:]
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='my-table',
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
@app.callback(
    Output('my-table', 'data'),
    [Input('adding-rows-btn', 'n_clicks')],
    [State('my-table', 'data'),
     State('my-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the Mongo database ***************************
@app.callback(
    Output("placeholder", "children"),
    Input("save-it", "n_clicks"),
    State("my-table", "data"),
    prevent_initial_call=True
)
def save_data(n_clicks, data):
    dff = pd.DataFrame(data)
    collection.delete_many({})
    collection.insert_many(dff.to_dict('records'))
    return ""


# Create graphs from DataTable data ***************************************
@app.callback(
    Output('show-graphs', 'children'),
    Input('my-table', 'data')
)
def add_row(data):
    df_grpah = pd.DataFrame(data)
    fig_hist1 = px.histogram(df_grpah, x='age',color="animal")
    fig_hist2 = px.histogram(df_grpah, x="neutered")
    return [
        html.Div(children=[dcc.Graph(figure=fig_hist1)], className="six columns"),
        html.Div(children=[dcc.Graph(figure=fig_hist2)], className="six columns")
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
