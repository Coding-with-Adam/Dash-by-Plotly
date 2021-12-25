import dash

dash.register_page(__name__, path="/")

from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import plotly.express as px
import pandas as pd


layout = html.Div(
    [
        html.P("Choose Day:"),
        html.Div(id="dropdown-container", children=[]),
        html.Div(id="bar-container", children=[]),
    ]
)

@callback(Output("dropdown-container", "children"), Input("stored-data", "data"))
def populate_dropdownvalues(data):
    dff = pd.DataFrame(data)
    return dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in dff.day.unique()],
        value=dff.day.unique()[0],
        clearable=False,
        style={"width": "50%"},
        persistence=True,
        persistence_type="session"
    ),


@callback(
    [Output("bar-container", "children"),
    Output("store-dropdown-value", "data")],
    [Input("dropdown", "value"),
     State("stored-data", "data")]
)
def graph_and_table(dropdown_day, data):
    dff = pd.DataFrame(data)
    dff = dff[dff["day"] == dropdown_day]
    fig = px.bar(dff, x="sex", y="total_bill", color="smoker", barmode="group")
    return dcc.Graph(figure=fig), dropdown_day

