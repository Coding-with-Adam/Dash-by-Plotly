import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.express as px
import pymongo
from pymongo import MongoClient


# Connect to local server
client = MongoClient("mongodb://127.0.0.1:27017/")
# Create database called animals
mydb = client["animals"]
# Create Collection (table) called shelterA
collection = mydb.shelterA
# Convert the Collection (table) date to a pandas DataFrame
df = pd.DataFrame(list(collection.find()))
print(df.head(9))
inputlist = df.iloc[:, 1:]

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Updating Existing Data in Local Mongo Server"),
    dcc.Dropdown(id='owner-chosen', multi=False, style={'width':"50%"},
                 options=[{'label': x, 'value': x} for x in df.owner.unique()]),

    dcc.Dropdown(id="categories", multi=False, style={'width':"50%"}, clearable=False,
                 options=[{'label': x, 'value': x} for x in df.columns]),
    dcc.Input(id="input-value", type="text", placeholder="input updated info"),
    html.Button("Save to Local Mongo Server",id='save-to-mongodb'),

    html.Hr(),
    html.P(),
    html.H1("Inserting new Documents (rows) in Local Mongo Server"),

    html.Div(children=[dcc.Input(id="input-{}".format(x), placeholder="insert {}".format(x))
                       for x in inputlist.columns]),
    html.Button("Insert New Document(row)", id='save-new-row'),

    html.Div(id='hidden-content'),
])


# Update existing rows
@app.callback(
    Output("hidden-content", "children"),
    Input("save-to-mongodb","n_clicks"),
    State("owner-chosen", "value"),
    State("categories", "value"),
    State("input-value", "value"),
    prevent_initial_call=True
)
def update_mongodb(n, own_v, categ_v, input_v):
    collection.update_one({"owner": own_v}, {"$set": {categ_v: input_v}})
    return ""


# Insert new Documents (rows)
@app.callback(
    Output("save-new-row", "style"),
    Input("save-new-row","n_clicks"),
    State("input-owner", "value"),
    State("input-animal", "value"),
    State("input-breed", "value"),
    State("input-health", "value"),
    State("input-age", "value"),
    State("input-neutered", "value"),
    prevent_initial_call=True
)
def new_mongodb_row(n, own_v, anim_v, breed_v, health_v, age, netrd_v):
    for i in (own_v, anim_v, breed_v, health_v, age, netrd_v):
        if i is None or len(i)==0:
            return {'background-color': 'white'}
    else:
        collection.insert_one(
            {
                "owner": own_v,
                "animal": anim_v,
                "breed": breed_v,
                "age": age,
                "health": health_v,
                "neutered": netrd_v
            }
        )
        return {'background-color': 'yellow'}


if __name__ == '__main__':
    app.run_server(debug=True)
