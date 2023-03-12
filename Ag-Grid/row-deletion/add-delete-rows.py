import dash_ag_grid as dag              # pip install dash-ag-grid==2.0.0a2
from dash import Dash, html, dcc, Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
import pandas as pd                     # pip install pandas
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# data from Nitin Datta on Kaggle (modified by me):
# https://www.kaggle.com/datasets/nitindatta/finance-data?select=Finance_data.csv
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Ag-Grid/row-deletion/finance_survey.csv")
print(df.head())

columnDefs = [
    {
        "headerName": "Gender",  # Name of table displayed in app
        "field": "Gender",       # ID of table (needs to be the same as excel sheet column name)
        "rowDrag": True,         # only need to activate on the first row for all to be draggable
        "checkboxSelection": True,  # only need to activate on the first row
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
    "minWidth": 150,
}



table = dag.AgGrid(
    id="portfolio-table",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    rowDragManaged=True,
    rowSelection="multiple",
    dashGridOptions={"undoRedoCellEditing": True},
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
                                        html.Span(
                                            [
                                                dbc.Button(
                                                    id="delete-row-btn",
                                                    children="Delete row",
                                                    color="secondary",
                                                    size="md",
                                                    className='mt-3 me-1'
                                                ),
                                                dbc.Button(
                                                    id="add-row-btn",
                                                    children="Add row",
                                                    color="primary",
                                                    size="md",
                                                    className='mt-3'
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ],
                    width=7,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            id="pie-breakdown", className="card-text"
                                        )
                                    ]
                                ),
                            ],
                        )
                    ],
                    width=5,
                ),
            ],
            className="py-4",
        ),
    ],
)



# add or delete rows of table
@app.callback(
    Output("portfolio-table", "deleteSelectedRows"),
    Output("portfolio-table", "rowData"),
    Input("delete-row-btn", "n_clicks"),
    Input("add-row-btn", "n_clicks"),
    State("portfolio-table", "rowData"),
    prevent_initial_call=True,
)
def update_dash_table(n_dlt, n_add, data):
    if ctx.triggered_id == "add-row-btn":
        new_row = {
            "Gender": [""],
            "Age": [0],
            "Money": [0],
            "Stock_Market": [""],
            "Objective": [""],
            "Source": [""]
        }
        df_new_row = pd.DataFrame(new_row)
        updated_table = pd.concat([pd.DataFrame(data), df_new_row])
        return False, updated_table.to_dict("records")

    elif ctx.triggered_id == "delete-row-btn":
        return True, no_update


# Build the Pie Chart
@app.callback(
    Output("pie-breakdown", "children"),
    Input("portfolio-table", "cellValueChanged"),
    Input("portfolio-table", "rowData"),
)
def update_portfolio_stats(cell_change, data):
    dff = pd.DataFrame(data)
    return dcc.Graph(figure=px.pie(
        dff,
        values='Money',
        names='Source',
        hole=0.3,
        template="plotly_dark",
    ))


if __name__ == "__main__":
    app.run_server(debug=True)
