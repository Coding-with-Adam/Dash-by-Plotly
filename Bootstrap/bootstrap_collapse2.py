import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State

import pandas as pd

# Data source: https://nextspaceflight.com/launches/past/?page=1 Data owner: "Agirlcoding" on Kaggle
df = pd.read_csv("Space_Corrected.csv")
# print(df.head())
df = df[df["Status Mission"] != "Prelaunch Failure"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div([
    dbc.Row([
        dbc.Button(
            f"Open {graph}",
            id=f"button-{graph}",
            className="mb-3",
            color="primary",
        ) for graph in ["pie", "hist", "strip"]
    ], justify="center"),
    dbc.Row([
        dbc.Col(dbc.Collapse(
            dcc.Graph(id="pie_chart", config={'displayModeBar': False},
                      figure=px.pie(df, names="Status Mission", values="Mission Cost").update_traces(showlegend=False)),
            id="collapse_pie", is_open=False), width=4),
        dbc.Col(dbc.Collapse(
            dcc.Graph(id="hist_chart", config={'displayModeBar': False},
                      figure=px.histogram(df, x="Mission Cost", range_x=[0,500])),
            id="collapse_hist", is_open=False), width=4),
        dbc.Col(dbc.Collapse(
            dcc.Graph(id="strip_chart", config={'displayModeBar': False},
                      figure=px.strip(df, x="Mission Cost", y="Status Mission", range_x=[0,220])),
            id="collapse_strip", is_open=False), width=4),
    ])
])


@app.callback(
    Output("collapse_pie", "is_open"),
    [Input("button-pie", "n_clicks")],
    [State("collapse_pie", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse_hist", "is_open"),
    [Input("button-hist", "n_clicks")],
    [State("collapse_hist", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse_strip", "is_open"),
    [Input("button-strip", "n_clicks")],
    [State("collapse_strip", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True, port=3000)
