from dash import Dash, html, dcc, Input, Output  # pip install dash
import dash_ag_grid as dag  # pip install dash-ag-grid
import pandas as pd  # pip install pandas
import plotly.express as px

df = px.data.tips()

table = dag.AgGrid(
    id="my-table",
    rowData=df.to_dict("records"),                                                          # **need it
    columnDefs=[{"field": i} for i in df.columns],                                          # **need it
    defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":115},
    columnSize="sizeToFit",
    dashGridOptions={"pagination": True, "paginationPageSize":10},
    className="ag-theme-alpine",  # https://dashaggrid.pythonanywhere.com/layout/themes
)
graph = dcc.Graph(id="my-graph", figure={})


app = Dash(__name__)
app.layout = html.Div([graph, table])


@app.callback(Output("my-graph", "figure"), Input("my-table", "virtualRowData"))
def display_cell_clicked_on(vdata):
    if vdata:
        dff = pd.DataFrame(vdata)
        return px.histogram(dff, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=df.columns)
    else:
        return px.histogram(df, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=df.columns)


if __name__ == "__main__":
    app.run_server(debug=True)
