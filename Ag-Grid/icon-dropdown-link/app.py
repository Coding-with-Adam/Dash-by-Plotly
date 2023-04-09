import dash_ag_grid as dag              # pip install dash-ag-grid==2.0.0a5
from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
import pandas as pd                     # pip install pandas
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
# data from Nitin Datta on Kaggle:
# https://www.kaggle.com/datasets/nitindatta/finance-data?select=Finance_data.csv
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Ag-Grid/row-deletion/finance_survey.csv")


# add image to Stock_market column
danger = f"![dangerous market]({app.get_asset_url('prohibited.png')})"
safety =  f"![safe market]({app.get_asset_url('safe.png')})"
market_icons = []
for x in df.Stock_Market:
    if x == 'No':
        market_icons.append(f"{danger}")
    else:
        market_icons.append(f"{safety}")

df.Stock_Market = market_icons


# add link to Source column
linked_source = []
for x in df.Source:
    if x == 'Newspapers':
        linked_source.append(f'[{x}](https://www.lefigaro.fr/)')
    elif x == 'Television':
        linked_source.append(f'[{x}](https://www.nationalgeographic.com/tv/)')
    else:
        linked_source.append(f'[{x}](https://www.google.com/)')

df.Source = linked_source


columnDefs = [
    {
        "headerName": "Gender",  # Name of table displayed in app
        "field": "Gender",       # ID of table (needs to be the same as excel sheet column name)
        "checkboxSelection": True,
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {
            "values": ["Female", "Male"],  # dropdown per Column
        },                                 # for dropdown per row see: https://dashaggrid.pythonanywhere.com/components/row-menu
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
        "cellRenderer": "markdown"  # needed for inserting image
    },
    {
        "headerName": "Objective",
        "field": "Objective",
    },
    {
        "headerName": "Source",
        "field": "Source",
        "cellRenderer": "markdown"  # needed for inserting image
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
        html.Div("AG Grid: Icons, Dropdown, Link", className="h3 p-2 text-white bg-secondary"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        table
                    ], width={"size": 10, "offset": 1},
                ),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
