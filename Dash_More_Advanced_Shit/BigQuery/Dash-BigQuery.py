import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from datetime import date

import plotly.express as px
import pandas as pd
from google.oauth2 import service_account  # pip install google-auth
import pandas_gbq  # pip install pandas-gbq

credentials = service_account.Credentials.from_service_account_file('C:/Users/13474/heroku/My_Dash/Youtube/Connect_Dash_to_Databases/BigQuery/assets\My First Project-6e03fa235eb0.json')
project_id = 'singular-winter-308201'  # make sure to change this with your own project ID

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("New York City and its Beautiful Trees", style={'textAlign':'center'}),
    html.Div(id='graph-content'),
    html.Div(
        dcc.Input(id='tree-diameter', placeholder="Insert number for diameter",
                  value=30, type='number'),
    ),
    html.Div(
        dcc.DatePickerRange(id='date-point',
                            min_date_allowed=date(2015, 3, 1),
                            max_date_allowed=date(2016, 4, 29),
                            start_date=date(2015, 3, 1),
                            end_date=date(2015, 12, 29)
                            ),
    ),
    html.Button(id='enter', children=['Submit'])
])


@app.callback(
    Output('graph-content', 'children'),
    [Input('enter','n_clicks')],
    [State('tree-diameter', 'value'),
    State('date-point', 'start_date'),
    State('date-point', 'end_date')]
)
def create_graph(n, treediameter, startdate, enddate):
    print(treediameter)
    print(startdate)
    print(enddate)
    # I recommend running the SQL in Good Cloud to make sure it works
    # before running it here in your Dash App.
    df_sql = f"""SELECT
    created_at,
    boroname,
    tree_dbh as diameter,
    spc_common as type
    FROM `bigquery-public-data.new_york_trees.tree_census_2015`
    WHERE created_at < '{enddate}'
    AND created_at > '{startdate}'
    AND tree_dbh > {treediameter}
    ORDER BY created_at DESC
    LIMIT 1000
    """

    df = pd.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    print(len(df))
    #df.to_csv("first_sample.csv")
    dff = df.groupby('boroname')[['diameter']].mean()
    dff.reset_index(inplace=True)
    print(dff.head(10))

    fig = px.bar(dff, x='boroname', y='diameter')
    return dcc.Graph(figure=fig)



if __name__=='__main__':
    app.run_server(debug=False)
