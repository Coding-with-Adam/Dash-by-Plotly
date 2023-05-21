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
# print(grid)
# grid.rowData[0]['Number of Solar Plants'] = 500

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
    prevent_initial_call=True
)
def display_cell_clicked_on(_, state_chosen, num):
    # print(np.where(df.State=='California')[0])

    update_grid_data = Patch()
    for x in [0,8,16]:
        update_grid_data[x]['Number of Solar Plants'] = num
    return update_grid_data


if __name__ == "__main__":
    app.run_server(debug=True)
