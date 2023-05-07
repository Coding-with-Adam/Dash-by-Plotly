from dash import Dash, html, dcc, Input, Output
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

df = px.data.tips()

app = Dash(__name__)

col_defs = []
for i in df.columns:
    if i=="tip" or i=="total_bill" or i=="size":
        col_defs.append({"field": i, "filter": "agNumberColumnFilter"})
    else:
        col_defs.append({"field": i})

table = dag.AgGrid(
    id="my-table",
    rowData=df.to_dict("records"),
    columnDefs=col_defs,
    defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":115},
    columnSize="sizeToFit",
    dashGridOptions={"pagination": True, "paginationPageSize":10},
    className="ag-theme-alpine",
)

graph = dcc.Graph(id="my-graph", figure={})
graph2 = dcc.Graph(id="my-graph2", figure={})

app.layout = html.Div([graph, table, graph2])


@app.callback(Output("my-graph", "figure"), Input("my-table", "virtualRowData"))
def display_cell_clicked_on(vdata):
    if vdata:
        dff = pd.DataFrame(vdata)
        return px.histogram(dff, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=df.columns)
    else:
        return px.histogram(df, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=df.columns)


@app.callback(Output("my-graph2", "figure"), Input("my-table", "cellClicked"))
def display_cell_clicked_on(cdata):
    if cdata:
        cell_row = int(cdata['rowId'])
        new_color = ["pink" if x==cell_row else "blue" for x in range(0,len(df))]
        new_size = [30 if x==cell_row else 10 for x in range(0,len(df))]

        fig = px.scatter(df, x="total_bill", y="tip")
        fig['data'][0]['marker']['color'] = new_color
        fig['data'][0]['marker']['size'] = new_size
        return fig

    else:
        return px.scatter(df, x="total_bill", y="tip")


if __name__ == "__main__":
    app.run_server(debug=True)
