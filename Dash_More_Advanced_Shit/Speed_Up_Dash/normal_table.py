from dash import Dash, html, dcc,Input, Output, State, Patch
import dash_ag_grid as dag
import pandas as pd
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")
df = pd.concat([df]*3, ignore_index=True)


app = Dash(__name__)

grid =  dag.AgGrid(
    id="quickstart-grid",
    rowData=df.to_dict("records"),
    columnDefs=[{"field": i} for i in df.columns],
    columnSize="sizeToFit",
)

app.layout = html.Div([
    html.Button('Get Data', id='my-button'),
    html.Div('Select State to update number of Solar Plants'),
    dcc.Dropdown(sorted(df.State.unique()), 'California', id='select-state'),
    dcc.Input(type='number', id='quantity'),
    grid
])


@app.callback(
    Output("quickstart-grid", "rowData"),
    Input("my-button", "n_clicks"),
    State("select-state", "value"),
    State("quantity", "value"),
    State("quickstart-grid", "rowData"),
    prevent_initial_call=True
)
def display_cell_clicked_on(_, state_chosen, num, data):
    for x in [0, 8, 16]:
        data[x]['Number of Solar Plants'] = num
    return data


if __name__ == "__main__":
    app.run_server(debug=True, port=8004)
