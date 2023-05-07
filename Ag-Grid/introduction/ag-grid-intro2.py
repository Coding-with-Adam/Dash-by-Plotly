from dash import Dash, html, dcc, Input, Output
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

df = px.data.tips()

# create a number-based filter for columns with integer data
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
graph2 = dcc.Graph(id="my-graph2", figure={})


app = Dash(__name__)
app.layout = html.Div([graph2, table])


@app.callback(Output('my-graph2', 'figure'), Input('my-table', 'cellClicked'))
def display_cell_clicked_on(cdata):
    if cdata:
        print(cdata)
        cell_row = int(cdata['rowId'])
        new_color = ["yellow" if x==cell_row else "blue" for x in range(0,len(df))]
        new_size = [30 if x==cell_row else 10 for x in range(0,len(df))]

        fig = px.scatter(df, x="total_bill", y="tip")
        fig['data'][0]['marker']['color'] = new_color
        fig['data'][0]['marker']['size'] = new_size
        return fig

    else:
        return px.scatter(df, x="total_bill", y="tip")


if __name__ == "__main__":
    app.run_server(debug=False, port=8045)
