import dash_ag_grid as dag              # pip install dash-ag-grid==2.0.0a5
from dash import Dash, html, dcc, Input, Output, State, no_update, Patch  # pip install dash==2.9.3
import dash_bootstrap_components as dbc # pip install dash-bootstrap-custom-components
import pandas as pd                     # pip install pandas
import plotly.express as px
import json

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
# data from Nitin Datta on Kaggle:
# https://www.kaggle.com/datasets/nitindatta/finance-data?select=Finance_data.csv
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Ag-Grid/row-deletion/finance_survey.csv")
df['Invest'] = 'sell'

columnDefs = [
    {
        "headerName": "Gender",  # Name of table displayed in app
        "field": "Gender",       # ID of table (needs to be the same as excel sheet column name)
        "checkboxSelection": True,
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
    {
        "headerName": "Invest",
        "field": "Invest",
        "cellRenderer": "Button",
        "cellRendererParams": {"className": "btn btn-info"},
    },
]

defaultColDef = {
    "filter": True,
    "floatingFilter": True,
    "resizable": True,
    "sortable": True,
    "editable": True,
    "minWidth": 125,
}



table = dag.AgGrid(
    id="portfolio-table",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=df.to_dict('records'),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions={"undoRedoCellEditing": True, "rowSelection":"multiple"},
)


app.layout = dbc.Container(
    [
        html.Div("Investments Survey", className="h3 p-2 text-white bg-secondary"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        table,
                                    ]
                                ),
                            ],
                        )
                    ], width={"size": 10, "offset": 1},
                ),
            ],
            className="py-4",
        ),
    ],
)

@app.callback(
    Output("portfolio-table", "rowData"),
    Input("portfolio-table", "cellRendererData"),
)
def showChange(n):
    if n:
        print(n)
        row_id_sold = int(n['rowId'])
        patched_table = Patch()
        patched_table[row_id_sold]['Money'] = 0
        return patched_table
    else:
        return no_update



if __name__ == "__main__":
    app.run_server(debug=True)
