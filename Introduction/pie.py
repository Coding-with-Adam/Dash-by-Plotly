import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px #(need to pip install plotly==4.4.1)

df = pd.read_csv("Urban_Park_Ranger_Animal_Condition_Response.csv")

# you need to include __name__ in your Dash constructor if
# you plan to use a custom CSS or JavaScript in your Dash apps
app = dash.Dash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        html.Label(['NYC Calls for Animal Rescue']),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                     {'label': 'Action Taken by Ranger', 'value': 'Final Ranger Action'},
                     {'label': 'Age', 'value': 'Age'},
                     {'label': 'Animal Health', 'value': 'Animal Condition'},
                     {'label': 'Borough', 'value': 'Borough'},
                     {'label': 'Species', 'value': 'Animal Class'},
                     {'label': 'Species Status', 'value': 'Species Status'}
            ],
            value='Animal Class',
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])

#---------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def update_graph(my_dropdown):
    dff = df

    piechart=px.pie(
            data_frame=dff,
            names=my_dropdown,
            hole=.3,
            )

    return (piechart)


if __name__ == '__main__':
    app.run_server(debug=True)
