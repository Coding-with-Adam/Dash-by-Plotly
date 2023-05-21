from dash import Dash, dcc, html, Input, Output, State, Patch
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

# Getting our data
df = pd.read_csv("MarketSales.csv")
# df = pd.read_csv("MarketSales1.csv")

# print("find index of item id #324")
# print(np.where(df['ID']==324))

# Print figure to understand how to use Patch
# fig = px.scatter(df, x='LINENET', y='PRICE')
# print(fig)
# # print('price of item id #324 on index 12 is:')
# print(fig['data'][0]['y'][12])
# exit()


# App layout
app.layout = html.Div([
    html.Div("Our goal is to update only the Price of one data point without transferring the whole figure and its data from the server to the browser."),
    dcc.RadioItems(['LINENET','LINENETTOTAL'], 'LINENET',  id='x-axis'),
    html.Button(id="button", children="update Price of one data point"),
    dcc.Graph(id="graph-update-example", figure={}),
])

@app.callback(
    Output("graph-update-example", "figure"),
    Input("x-axis", "value"),
)
def update_markers(x_axis_col):
    fig = px.scatter(df, x=x_axis_col, y='PRICE')
    return fig

@app.callback(
    Output("graph-update-example", "figure", allow_duplicate=True),
    Input("button", "n_clicks"),
    prevent_initial_call=True
)
def update_markers(n_click):
    patched_figure = Patch()
    patched_figure['data'][0]['y'][12] = 500+n_click*100
    return patched_figure


if __name__ == '__main__':
    app.run_server(debug=True)
