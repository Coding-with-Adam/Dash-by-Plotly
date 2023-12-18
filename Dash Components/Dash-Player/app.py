from dash import Dash, dcc, html, Input, Output, State, callback
import dash_player  # pip install dash-player

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    style={"width": "48%", "padding": "0px"},
                    children=[
                        dash_player.DashPlayer(
                            id="player",
                            url="https://youtu.be/wmQ6_GZ0zSk",
                            controls=True,
                            width="100%",
                            height="250px",
                        ),
                        dcc.Checklist(
                            id="bool-props-radio",
                            options=[
                                {"label": val.capitalize(), "value": val}
                                for val in [
                                    "playing",
                                    "loop",
                                    "controls",
                                    "muted",
                                ]
                            ],
                            value=["controls"],
                            inline=True,
                            style={"margin": "20px 0px"},
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="seekto-number-input",
                                    type="number",
                                    placeholder="seekTo value",
                                    style={"width": "calc(100% - 115px)"},
                                ),
                                html.Button(
                                    "seekTo",
                                    id="seekto-number-btn",
                                    style={"width": "105px"},
                                ),
                            ],
                            style={"margin": "20px 0px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    id="current-time-div",
                                    style={"margin": "10px 0px"},
                                ),
                                html.Div(
                                    id="seconds-loaded-div",
                                    style={"margin": "10px 0px"},
                                ),
                                html.Div(
                                    id="duration-div",
                                    style={"margin": "10px 0px"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                            },
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%", "padding": "10px"},
                    children=[
                        html.P("Volume:", style={"marginTop": "30px"}),
                        dcc.Slider(
                            id="volume-slider",
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            updatemode="drag",
                            marks={0: "0%", 0.5: "50%", 1: "100%"},
                        ),
                        html.P("Playback Rate:", style={"marginTop": "25px"}),
                        dcc.Slider(
                            id="playback-rate-slider",
                            min=0,
                            max=2,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) + "x" for i in [0, 0.5, 1, 1.5, 2]},
                            value=1,
                        ),
                        html.P(
                            "Update Interval for Current Time:",
                            style={"marginTop": "30px"},
                        ),
                        dcc.Slider(
                            id="intervalCurrentTime-slider",
                            min=0,
                            max=1000,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) for i in [0, 250, 500, 750, 1000]},
                            value=250,
                        ),
                    ],
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
            },
        ),
    ]
)


@callback(
    Output("player", "playing"),
    Output("player", "loop"),
    Output("player", "controls"),
    Output("player", "muted"),
    Input("bool-props-radio", "value"),
)
def update_bool_props(values):
    print(values)
    playing = "playing" in values
    loop = "loop" in values
    controls = "controls" in values
    muted = "muted" in values
    print(muted)
    return playing, loop, controls, muted


@callback(
    Output("player", "seekTo"),
    Input("seekto-number-btn", "n_clicks"),
    State("seekto-number-input", "value"),
)
def set_prop_seekTo(n_clicks, seekto):
    return seekto


@callback(
    Output("current-time-div", "children"),
    Input("player", "currentTime"),
)
def display_currentTime(currentTime):
    return f"Current Time: {currentTime}"


@callback(
    Output("seconds-loaded-div", "children"),
    Input("player", "secondsLoaded"),
)
def display_secondsLoaded(secondsLoaded):
    return f"Second Loaded: {secondsLoaded}"


@callback(
    Output("duration-div", "children"),
    Input("player", "duration"),
)
def display_duration(duration):
    return f"Duration: {duration}"


@callback(
    Output("player", "volume"),
    Input("volume-slider", "value"),
)
def set_volume(value):
    return value


@callback(
    Output("player", "playbackRate"),
    Input("playback-rate-slider", "value"),
)
def set_playbackRate(value):
    return value


@callback(
    Output("player", "intervalCurrentTime"),
    Input("intervalCurrentTime-slider", "value"),
)
def set_intervalCurrentTime(value):
    return value


if __name__ == "__main__":
    app.run(debug=True)
