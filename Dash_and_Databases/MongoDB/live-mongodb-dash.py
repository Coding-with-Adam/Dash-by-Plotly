# Mongodb Set up guide: https://docs.google.com/document/d/1EdvOK5_1D4ya94-N0RU5t9Rm_e2YurhU/edit?usp=sharing&ouid=118003078876393636228&rtpof=true&sd=true
import dash                                                     # pip install dash  (2.1 or higher)
from dash import html, dcc, Input, Output, State, dash_table
import pandas as pd                                             # pip install pandas
import plotly.express as px
import pymongo                                                  # pip install "pymongo[srv]"
from bson.objectid import ObjectId

# Connect to server on the cloud
client = pymongo.MongoClient(
    "mongodb+srv://adam3:mypassword@cluster0.t9aqb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# test the connection
# db = client.test
# print(db)
# exit()

# Go into the database I created
db = client["xindustry"]
# Go into one of my database's collection (table)
collection = db["production"]

# Example of how to create a document (row)
# record = {
#     "employee": "Mike",
#     "department": "engineering",
#     "product": "PC",
#     "part": "motherboard",
#     "quantity": "12",
#     "day": "Saturday"
# }
# # Insert document (row) into the database's collection (table)
# collection.insert_one(record)
# testing = collection.find_one()
# print(testing)
# exit()

# Define Layout of App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('Web Application connected to a Live Database', style={'textAlign': 'center'}),
    # interval activated once/week or when page refreshed
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div(id='mongo-datatable', children=[]),

    html.Div([
        html.Div(id='pie-graph', className='five columns'),
        html.Div(id='hist-graph', className='six columns'),
    ], className='row'),
    dcc.Store(id='changed-cell')
])


# Display Datatable with data from Mongo database
@app.callback(Output('mongo-datatable', component_property='children'),
              Input('interval_db', component_property='n_intervals')
              )
def populate_datatable(n_intervals):
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    # Convert id from ObjectId to string so it can be read by DataTable
    df['_id'] = df['_id'].astype(str)
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='our-table',
            data=df.to_dict('records'),
            columns=[{'id': p, 'name': p, 'editable': False} if p == '_id'
                     else {'id': p, 'name': p, 'editable': True}
                     for p in df],
        ),
    ]


# store the row id and column id of the cell that was updated
app.clientside_callback(
    """
    function (input,oldinput) {
        if (oldinput != null) {
            if(JSON.stringify(input) != JSON.stringify(oldinput)) {
                for (i in Object.keys(input)) {
                    newArray = Object.values(input[i])
                    oldArray = Object.values(oldinput[i])
                    if (JSON.stringify(newArray) != JSON.stringify(oldArray)) {
                        entNew = Object.entries(input[i])
                        entOld = Object.entries(oldinput[i])
                        for (const j in entNew) {
                            if (entNew[j][1] != entOld[j][1]) {
                                changeRef = [i, entNew[j][0]] 
                                break        
                            }
                        }
                    }
                }
            }
            return changeRef
        }
    }    
    """,
    Output('changed-cell', 'data'),
    Input('our-table', 'data'),
    State('our-table', 'data_previous')
)


# Update MongoDB and create the graphs
@app.callback(
    Output("pie-graph", "children"),
    Output("hist-graph", "children"),
    Input("changed-cell", "data"),
    Input("our-table", "data"),
)
def update_d(cc, tabledata):
    if cc is None:
        # Build the Plots
        pie_fig = px.pie(tabledata, values='quantity', names='day')
        hist_fig = px.histogram(tabledata, x='department', y='quantity')
    else:
        print(f'changed cell: {cc}')
        print(f'Current DataTable: {tabledata}')
        x = int(cc[0])

        # update the external MongoDB
        row_id = tabledata[x]['_id']
        col_id = cc[1]
        new_cell_data = tabledata[x][col_id]
        collection.update_one({'_id': ObjectId(row_id)},
                              {"$set": {col_id: new_cell_data}})
        # Operations guide - https://docs.mongodb.com/manual/crud/#update-operations

        pie_fig = px.pie(tabledata, values='quantity', names='day')
        hist_fig = px.histogram(tabledata, x='department', y='quantity')

    return dcc.Graph(figure=pie_fig), dcc.Graph(figure=hist_fig)


if __name__ == '__main__':
    app.run_server(debug=False)
