import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_daq as daq


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# *************************************************************************
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Room Temperature"),
                html.Div(
                    daq.Knob(
                        id="my-knob",
                        label="Set Temperature",
                        min=30,
                        max=100,
                        value=40,
                        scale={"start": 40, "labelInterval": 10, "interval": 10},
                        color={
                            "gradient": True,
                            "ranges": {"blue": [30, 75], "red": [75, 100]},
                        },
                    ),
                    className="two columns",
                ),
                html.Div(
                    daq.Thermometer(id="my-thermometer", min=30, max=99, value=40),
                    className="three columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    daq.LEDDisplay(id="my-leddisplay", value="40", color="#39FF14"),
                    className="four columns",
                ),
                html.Div(
                    daq.ColorPicker(
                        id="my-colorpicker",
                        label="Choose display color",
                        value={"hex": "#39FF14"},
                    ),
                    className="three columns",
                ),
            ],
            className="row",
        ),
    ]
)


# *************************************************************************
# must have Dash 1.16.0 or higher for this to work
@app.callback(
    Output("my-thermometer", "value"),
    Output("my-leddisplay", "value"),
    Output("my-leddisplay", "color"),
    Input("my-knob", "value"),
    Input("my-colorpicker", "value"),
)
def update(knob_value, color_chosen):
    return knob_value, knob_value, color_chosen["hex"]


if __name__ == "__main__":
    app.run_server(port=3040, debug=True)
