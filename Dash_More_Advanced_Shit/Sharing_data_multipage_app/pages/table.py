import dash

dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd


layout = html.Div(
    [
        html.Div(id="table-container", children=[]),
    ]
)

@callback(Output("table-container", "children"),
          [Input("stored-data", "data"),
           Input("dropdown-value", "data")]
          )
def populate_checklist(data, day):
    dff = pd.DataFrame(data)
    dff = dff[dff["day"] == day]
    my_table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in dff.columns],
                    data=dff.to_dict('records'),
                )
    return my_table