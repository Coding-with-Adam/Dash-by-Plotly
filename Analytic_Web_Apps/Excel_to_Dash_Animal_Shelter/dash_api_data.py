import dash                     # pip install dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px     # pip install plotly==5.2.2

import pandas as pd             # pip install pandas
from sodapy import Socrata      # pip install sodapy
# Data: https://www.dallasopendata.com/Services/Animals-Inventory/qgg6-h4bd
# Socrata API Python wrapper repository: https://github.com/xmunoz/sodapy

# Connect to Socrata API
socrata_domain = 'www.dallasopendata.com'
socrata_dataset_identifier = 'qgg6-h4bd'
client = Socrata(socrata_domain, app_token="wikVcRNlqjQupRZ6oiKQoF1g8")

# pull the data from Socrata API
results = client.get(socrata_dataset_identifier)
# Convert data into a pandas dataframe
df = pd.DataFrame(results)

df["intake_time"] = pd.to_datetime(df["intake_time"])
df["intake_time"] = df["intake_time"].dt.hour
df["animal_stay_days"] = df["animal_stay_days"].astype(int)
print(df.head())
exit()

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
#                 suppress_callback_exceptions=True)
#
# app.layout = html.Div([
#     html.H1("Analytics Dashboard of Dallas Animal Shelter (Dash Plotly)", style={"textAlign":"center"}),
#     html.Hr(),
#     html.P("Choose animal of interest:"),
#     html.Div(html.Div(id="drpdn-div", children=[], className="two columns"),className="row"),
#
#     dcc.Interval(id="timer", interval=1000*7, n_intervals=0),
#     dcc.Store(id="stored", data={}),
#
#     html.Div(id="output-div", children=[]),
# ])
#
#
# @app.callback(Output("stored", "data"),
#               Output("drpdn-div", "children"),
#               Input("timer","n_intervals")
# )
# def get_drpdn_and_df(n):
#     results = client.get(socrata_dataset_identifier)
#     # Convert data into a pandas dataframe
#     df = pd.DataFrame(results)
#     df["intake_time"] = pd.to_datetime(df["intake_time"])
#     df["intake_time"] = df["intake_time"].dt.hour
#     df["animal_stay_days"] = df["animal_stay_days"].astype(int)
#     # print(df.iloc[:, :4].head())
#
#     return df.to_dict('records'), dcc.Dropdown(id='animal-type',
#                                                clearable=False,
#                                                value="DOG",
#                                                options=[{'label': x, 'value': x} for x in
#                                                         df["animal_type"].unique()])
#
#
# @app.callback(Output("output-div", "children"),
#               Input("animal-type", "value"),
#               Input("stored", "data"),
# )
# def make_bars(animal_chosen, data):
#     df = pd.DataFrame(data)
#
#     # HISTOGRAM
#     df_hist = df[df["animal_type"]==animal_chosen]
#     fig_hist = px.histogram(df_hist, x="animal_breed")
#     fig_hist.update_xaxes(categoryorder="total descending")
#
#     # STRIP CHART
#     fig_strip = px.strip(df_hist, x="animal_stay_days", y="intake_type")
#
#     # SUNBURST
#     df_sburst = df.dropna(subset=['chip_status'])
#     df_sburst = df_sburst[df_sburst["intake_type"].isin(["STRAY", "FOSTER", "OWNER SURRENDER"])]
#     fig_sunburst = px.sunburst(df_sburst, path=["animal_type", "intake_type", "chip_status"])
#
#     # Empirical Cumulative Distribution
#     df_ecdf = df[df["animal_type"].isin(["DOG","CAT"])]
#     fig_ecdf = px.ecdf(df_ecdf, x="animal_stay_days", color="animal_type")
#
#     # LINE CHART
#     df_line = df.sort_values(by=["intake_time"], ascending=True)
#     df_line = df_line.groupby(
#         ["intake_time", "animal_type"]).size().reset_index(name="count")
#     fig_line = px.line(df_line, x="intake_time", y="count",
#                        color="animal_type", markers=True)
#
#     return [
#         html.Div([
#             html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
#             html.Div([dcc.Graph(figure=fig_strip)], className="six columns"),
#         ], className="row"),
#         html.H2("All Animals", style={"textAlign":"center"}),
#         html.Hr(),
#         html.Div([
#             html.Div([dcc.Graph(figure=fig_sunburst)], className="six columns"),
#             html.Div([dcc.Graph(figure=fig_ecdf)], className="six columns"),
#         ], className="row"),
#         html.Div([
#             html.Div([dcc.Graph(figure=fig_line)], className="twelve columns"),
#         ], className="row"),
#     ]


if __name__ == '__main__':
    app.run_server(debug=True)
