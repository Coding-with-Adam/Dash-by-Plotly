# import the libraries----------------------------------------------------
import plotly.express as px
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

# read, clean, and filter the data----------------------------------------
# data source: https://mappingpoliceviolence.org/aboutthedata
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/DPhi%20Presentation/MPVDataset.csv")

df = df[df["Victim's race"].isin(["White", "Black", "Hispanic", "Asian"])]
df["Victim's age"] = pd.to_numeric(df["Victim's age"], errors='coerce')

# app layout--------------------------------------------------------------
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(id='gender', multi=False, clearable=False,
                     options=[{'label': x, 'value': x} for x in
                              sorted(df["Victim's gender"].unique())],
                     value="Male")
    ], style={'width': '50%'}),

    html.Div([
        dcc.Graph(id='my-barplot', figure={})
    ])
    ,
    html.Div(id='content-container', children='')
])


# Callback - app interactivity section------------------------------------
@app.callback(
    Output(component_id='my-barplot', component_property='figure'),
    # Output(component_id='content-container', component_property='children'),
    Input(component_id='gender', component_property='value'),
)
def update_graph(gender_chosen):
    print(gender_chosen)
    # build the graph
    dff = df[df["Victim's gender"] == gender_chosen]
    dff = dff.groupby(["Victim's race", "Geography"])[
        ["Victim's age"]].mean()
    dff = dff.reset_index()
    fig = px.bar(
        data_frame=dff,
        x="Victim's race",
        y="Victim's age",
        color="Geography",
        barmode="group"
    )
    return fig  # gender_chosen


if __name__=='__main__':
    app.run_server(debug=True, port=8002)
