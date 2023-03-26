import dash_ag_grid as dag              # pip install dash-ag-grid==2.0.0a4
from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
import pandas as pd                     # pip install pandas
import plotly.express as px
import os

# canada_finance data from Nitin Datta on Kaggle (modified by me):
# https://www.kaggle.com/datasets/nitindatta/finance-data?select=Finance_data.csv

datasets = [files for path, subdirectory, files in os.walk("\\Users\\adams\\PycharmProjects\\YouTube\\Ag Grid\\save-table\\data")]
print(datasets[0])

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


columnDefs = [
    {
        "headerName": "Gender",  # Name of table displayed in app
        "field": "Gender",       # ID of table (needs to be the same as excel sheet column name)
    },
    {
        "headerName": "Age",
        "field": "Age",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
    },
    {
        "headerName": "Money",
        "field": "Money",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
    },
    {
        "headerName": "Stock_Market",
        "field": "Stock_Market",
    },
    {
        "headerName": "Objective",
        "field": "Objective",
    },
    {
        "headerName": "Source",
        "field": "Source",
    },
]

defaultColDef = {
    "filter": True,
    "floatingFilter": True,
    "resizable": True,
    "sortable": True,
    "editable": True,
    "minWidth": 100,
}



table = dag.AgGrid(
    id="portfolio-table",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=None,
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions={"undoRedoCellEditing": True, "selectedRows": "multiple"},
)


app.layout = dbc.Container(
    [
        html.Div("Investments Survey", className="h3 p-2 text-white bg-secondary", id='not-important'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    dcc.Dropdown(
                                        id='retrieve-dataset',
                                        options=datasets[0],
                                        value=datasets[0][0],
                                        placeholder='Select dataset',
                                        clearable=False,
                                        style={'color':'black'}
                                    ), style={"width": "18rem"},
                                ),
                                dbc.CardBody(
                                    [
                                        table,
                                        dbc.Row([
                                           dbc.Col([
                                               dbc.Input(
                                                   id="save-name",
                                                   placeholder="Save as...",
                                                   type="text",
                                                   value=None,
                                                   className='mt-2'
                                               ),
                                           ], width=6),
                                            dbc.Col([
                                                dbc.Button(
                                                    id="save-btn",
                                                    children="Save Table",
                                                    color="primary",
                                                    size="md",
                                                    className='mt-2'
                                                ),
                                            ], width=3)
                                        ]),
                                    ]
                                ),
                            ],
                        )
                    ],
                    width=12,
                ),
            ],
            className="py-4",
        ),
        dbc.Row(
            dbc.Alert(children=None,
                      color="success",
                      id='alerting',
                      is_open=False,
                      duration=2000,
                      className='ms-4',
                      style={'width':'18rem'}
            ),
        )
    ],
)

# retrieve dataset to display in table
@app.callback(
    Output("portfolio-table", "rowData"),
    Input("retrieve-dataset", "value"),
)
def update_portfolio_stats(dataset_selected):
    # print(dataset_selected)
    dff = pd.read_csv(f'data\\{dataset_selected}')
    return dff.to_dict('records')


# save your data
@app.callback(
    Output("alerting", "is_open"),
    Output("alerting", "children"),
    Output("alerting", "color"),
    Input("save-btn", "n_clicks"),
    State("save-name", "value"),
    State("portfolio-table", "rowData"),
prevent_initial_call=True
)
def update_portfolio_stats(n, name, data):
    print(type(name))
    if name is None or len(name)==0:
        return True, "No name provided", "danger"
    else:
        dff = pd.DataFrame(data)
        dff.to_csv(f'data\\{name}.csv', index=False)
        return True, "Data Saved! Well done!", "success"



if __name__ == "__main__":
    app.run_server(debug=True)
