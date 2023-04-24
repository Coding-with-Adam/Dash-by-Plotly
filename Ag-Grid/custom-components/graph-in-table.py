import dash_ag_grid as dag              # pip install dash-ag-grid==2.0.0a5
from dash import Dash, html, dcc, Input, Output, State, no_update, Patch
import dash_bootstrap_components as dbc # pip install dash-bootstrap-custom-components
import pandas as pd                     # pip install pandas
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
# data from Nitin Datta on Kaggle:
# https://www.kaggle.com/datasets/nitindatta/finance-data?select=Finance_data.csv
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Ag-Grid/row-deletion/finance_survey.csv")
subset = df.groupby("Objective")[["Age","Money"]].mean().reset_index()
subset[["Age","Money"]] = subset[["Age","Money"]].round(0)
subset['Graphing'] = ''


for i, r in subset.iterrows():
    filterDf = df[df["Objective"] == r["Objective"]]
    # fig = px.histogram(filterDf, x='Source', y='Money')
    fig = px.scatter(filterDf, x='Age', y='Money', color='Gender', hover_data={'Money':True, 'Age':True, 'Gender':False})

    fig.update_layout(
        scattermode='group',
        scattergap=0.25,
        showlegend=False,
        yaxis_visible=False,
        yaxis_showticklabels=False,
        xaxis_visible=False,
        xaxis_showticklabels=False,
        margin=dict(l=0, r=0, t=0, b=0),
        template="plotly_dark",
    )
    subset.at[i, "Graphing"] = fig

columnDefs = [
    {
        "headerName": "Age",
        "field": "Age",
        "type": "rightAligned",
    },
    {
        "headerName": "Money",
        "field": "Money",
        "type": "rightAligned",
    },
    {
        "headerName": "Objective",
        "field": "Objective",
    },
    {
        "headerName": "Graphing",
        "field": "Graphing",
        "cellRenderer": "DCC_GraphClickData",
        "maxWidth": 900,
        "minWidth": 500,

    },
]


table = dag.AgGrid(
    id="portfolio-table",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=subset.to_dict('records'),
    columnSize="sizeToFit",
    dashGridOptions={"rowHeight": 120},
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




if __name__ == "__main__":
    app.run_server(debug=True)
