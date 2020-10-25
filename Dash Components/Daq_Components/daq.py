import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.graph_objects as go
from random import randrange


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# *************************************************************************
app.layout = html.Div(
    id="dark-light-theme",
    children=[
        html.Div(
            [
                html.H1("Water Valve Pressure", style={"textAlign": "center"}),
                html.Div(
                    daq.Tank(
                        id="my-tank",
                        max=400,
                        value=197,
                        showCurrentValue=True,
                        units="gallons",
                        style={"margin-left": "50px"},
                    ),
                    className="three columns",
                ),
                html.Div(
                    daq.Gauge(
                        id="my-daq-gauge1", min=0, max=10, value=6, label="Valve 1"
                    ),
                    className="four columns",
                ),
                html.Div(
                    daq.Gauge(
                        id="my-daq-gauge2", min=0, max=10, value=9, label="Valve 2"
                    ),
                    className="four columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            html.Div(
                daq.ToggleSwitch(
                    id="my-toggle-switch", label="Liters | Gallons", value=True
                ),
                className="three columns",
            ),
            className="row",
        ),
        html.Div(
            dcc.Graph(id="my-graph", figure={}),
            className="row",
        ),
        dcc.Interval(id="timing", interval=1000, n_intervals=0),
    ],
)


# *************************************************************************
# must have Dash 1.16.0 or higher for this to work
@app.callback(
    Output("my-daq-gauge1", "value"),
    Output("my-daq-gauge2", "value"),
    Output("my-graph", "figure"),
    Input("timing", "n_intervals"),
)
def update_g(n_intervals):
    pressure_1 = randrange(10)  # mimics data pulled from live database
    pressure_2 = randrange(10)  # mimics data pulled from live database

    fig = go.Figure(
        [
            go.Bar(
                x=["valve 1", "valve 2"],
                y=[pressure_1, pressure_2],
            )
        ]
    )
    fig.update_layout(yaxis={"range": [0, 10]})

    return pressure_1, pressure_2, fig


@app.callback(
    Output("my-tank", "units"),
    Input("my-toggle-switch", "value"),
)
def update_g(toggle):
    if toggle:
        return "gallons"
    else:
        return "liters"


if __name__ == "__main__":
    app.run_server(debug=True, port=3030)
