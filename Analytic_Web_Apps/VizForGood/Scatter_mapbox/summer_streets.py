from dash import Dash, html, dcc, Input, Output, callback  # dash 2.0 or higher
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  # dash bootstrap 1.0 or higher

dfc = pd.read_csv(
    "https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/VizForGood/Scatter_mapbox/Volaby-Sunny_Street-detailed-stats%202019%20-%202021%20-%20V3.csv"
)
# dfp = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/VizForGood/Scatter_mapbox/Sunny%20Street%20-%20Patient%20data%203%20years.csv")

# Data Processing *********************************************************
# *************************************************************************
dfc["Activity"] = dfc["Activity"].replace(
    {
        "Hervey Bay Neighbourhood/ Community Centre ": "Hervey Bay Neighbourhood",
        "Maroochydore Neighbourhood Centre Community Event ": "Maroochydore Neighbourhood Centre",
    }
)

# create shift periods for the bottom map
dfc["Start Time"] = pd.to_datetime(dfc["Start Time"], format="%I:%M %p").dt.hour
dfc["shift_start"] = ""
dfc.loc[dfc["Start Time"] >= 19, "shift_start"] = "night"
dfc.loc[dfc["Start Time"] < 12, "shift_start"] = "morning"
dfc.loc[
    (dfc["Start Time"] >= 12) & (dfc["Start Time"] < 19), "shift_start"
] = "afternoon"
dfc_shift = dfc.groupby(["Latitude", "Longitude", "Activity", "shift_start"])[
    ["Medical Consults"]
].sum()
dfc_shift.reset_index(inplace=True)
# print(dfc_shift.head())

# calculate average shift time for bottom histogram graph
avg_shift_time = round(dfc["Length minutes"].mean())

# re-organize dataframe for the top map
dfc_gpd = dfc.groupby(["Latitude", "Longitude", "Activity"])[
    [
        "Medical Consults",
        "Nurse Practitioner Consults",
        "Nursing/Paramedic Consults",
        "Conversations about health education",
        "Allied Health",
        "Referrals (Formal and informal)",
        "Patient Conversations",
        "Service provider conversations",
        "Mental health",
        "Suicide prevention/planning",
        "Substance use",
        "Medication education",
        "Patients turned away",
        "Telehealth consults that happened at Clinic",
        "Length minutes",
    ]
].sum()
dfc_gpd.reset_index(inplace=True)


app = Dash(
    __name__, external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True
)

# Layout building *********************************************************
app.layout = dbc.Container(
    [
        dbc.Container(
            [
                html.H1(
                    "Sunny Streets Dashboard",
                    style={"textAlign": "center"},
                    className="display-3",
                )
            ],
            className="p-5 bg-light rounded-1 mt-3 mb-5",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("For Funders:"),
                        html.P(
                            "Change dropdown and button values to see how your contribution can impact our work."
                        ),
                        dcc.Dropdown(
                            id="bar-data",
                            clearable=False,
                            value="Activity",
                            options=[
                                {"label": "Activity Center", "value": "Activity"},
                                {"label": "Region", "value": "Program"},
                            ],
                        ),
                    ],
                    width=5,
                ),
                dbc.Col(
                    [html.P("")],
                    style={
                        "borderLeft": "6px solid red",
                        "height": "1100px",
                        "position": "absolute",
                        "left": "49.75%",
                    },
                ),
                dbc.Col(
                    [
                        html.H3("For Volunteers:"),
                        html.P(
                            "Use Maps for exploring services and shifts to choose a volunteer Activity Center best for you."
                        ),
                        dcc.Dropdown(
                            id="map1-conslt-data",
                            clearable=False,
                            value="Medical Consults",
                            options=[
                                {
                                    "label": "Medical Consults",
                                    "value": "Medical Consults",
                                },
                                {
                                    "label": "Patient Conversations",
                                    "value": "Patient Conversations",
                                },
                                {
                                    "label": "Referrals",
                                    "value": "Referrals (Formal and informal)",
                                },
                                {"label": "Substance use", "value": "Substance use"},
                            ],
                        ),
                    ],
                    width=5,
                ),
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col(id="bar-col", children=[], width=5),
                dbc.Col(id="map-conslt-col", children=[], width=5),
            ],
            justify="around",
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="hist-data",
                            clearable=False,
                            value="avg",
                            options=[
                                {"label": "Average shift time", "value": "avg"},
                                {"label": "Sum of shifts", "value": "sum"},
                            ],
                        ),
                        dcc.RadioItems(
                            id="checklist",
                            value="$10,000",
                            className="mt-1",
                            options=[
                                {"label": x, "value": x}
                                for x in ("$0k", "$10,000", "$25,000", "$50,000")
                            ],
                        ),
                        html.Div(
                            id="thediv",
                            children=dcc.Dropdown(
                                id="activity-data",
                                clearable=False,
                                value="Beddown Event Brisbane CBD",
                                options=[
                                    {"label": x, "value": x}
                                    for x in sorted(dfc.Activity.unique())
                                ],
                            ),
                        ),
                    ],
                    width=5,
                ),
                dbc.Col(width=5),
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col(id="hist-col", children=[], width=5),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="map2",
                            config={"displayModeBar": False},
                            figure=px.scatter_mapbox(
                                dfc_shift,
                                lat="Latitude",
                                lon="Longitude",
                                hover_data={
                                    "Activity": True,
                                    "Longitude": False,
                                    "Latitude": False,
                                },
                                color="shift_start",
                                zoom=6,
                                labels={"shift_start": "Shift Start Time"},
                            )
                            .update_layout(
                                mapbox_style="carto-darkmatter",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                            )
                            .update_traces(marker_size=20),
                        )
                    ],
                    width=5,
                ),
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/image3.jpg",
                            style={"maxHeight": "500px", "maxWidth": "200px"},
                        )
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.H5(
                            "We are also always on the lookout for donations of medical equipment and supplies. If you can help in this area please contact us at info@sunnystreet.org"
                        ),
                    ],
                    width=7,
                ),
            ],
            justify="center",
            className="mt-5 mb-2",
        ),
    ],
    fluid=True,
)


# top left bar graph ******************************************************
@callback(Output("bar-col", "children"), Input("bar-data", "value"))
def create_bar_graph(data_column):
    bar_grpah = dcc.Graph(
        figure=px.bar(
            dfc, x=data_column, y="Patients turned away", hover_data=["Activity Date"]
        ).update_xaxes(categoryorder="total descending")
    )
    return bar_grpah


# top right map ***********************************************************
@callback(Output("map-conslt-col", "children"), Input("map1-conslt-data", "value"))
def create_map(data_column):
    map1 = dcc.Graph(
        config={"displayModeBar": False},
        figure=px.scatter_mapbox(
            dfc_gpd,
            lat="Latitude",
            lon="Longitude",
            size="Length minutes",
            hover_data={"Activity": True, "Longitude": False, "Latitude": False},
            size_max=40,
            color=data_column,
            color_continuous_scale=px.colors.sequential.Bluered,
            zoom=6,
        ).update_layout(
            mapbox_style="stamen-terrain", margin={"r": 0, "t": 0, "l": 0, "b": 0}
        ),
    )

    return map1


# hide and unhide Div with dropdown ***************************************
@callback(
    Output("thediv", "style"),
    Input("hist-data", "value"),
)
def hidden_div(value):
    if value == "avg":
        return {"visibility": "hidden"}
    return {"visibility": "visible"}


# bottom left histogram graph *********************************************
@callback(
    Output("hist-col", "children"),
    Input("checklist", "value"),
    Input("activity-data", "value"),
    Input("hist-data", "value"),
)
def create_dashboard4(che_value, act_value, hist_data):
    if che_value == "$10,000":
        new_y = 160
        increment = 1.4
    if che_value == "$25,000":
        new_y = 200
        increment = 2
    if che_value == "$50,000":
        new_y = 250
        increment = 4

    if hist_data == "avg":
        if che_value == "$0k":
            hist_grpah = dcc.Graph(
                figure=px.histogram(
                    dfc,
                    x="Activity",
                    y="Length minutes",
                    histfunc=hist_data,
                    labels={"Length minutes": "Shift time"},
                )
                .update_xaxes(categoryorder="total descending")
                .add_hline(
                    y=120,
                    line_dash="dot",
                    annotation_text=f"Average shift time is {avg_shift_time}",
                    line_color="black",
                )
            )
            return hist_grpah
        elif che_value != "0k":
            hist_grpah = dcc.Graph(
                figure=px.histogram(
                    dfc,
                    x="Activity",
                    y="Length minutes",
                    histfunc=hist_data,
                    labels={"Length minutes": "Shift time"},
                )
                .update_xaxes(categoryorder="total descending")
                .add_hline(
                    y=120,
                    line_dash="dot",
                    annotation_text=f"Average shift time is {avg_shift_time}",
                    line_color="black",
                )
                .add_hline(
                    y=new_y,
                    line_dash="dot",
                    line_color="green",
                    annotation_text=f"{che_value} contribution will increase average shift time to {new_y} minutes",
                )
            )
            return hist_grpah

    if hist_data == "sum":
        df = dfc.copy()
        df["colors"] = "blue"
        df.loc[df.Activity == act_value, "colors"] = "red"

        if che_value == "$0k":
            hist_graph = dcc.Graph(
                figure=px.histogram(
                    df,
                    x="Activity",
                    y="Length minutes",
                    color="colors",
                    histfunc=hist_data,
                    labels={"Length minutes": "Shift time"},
                )
                .update_xaxes(categoryorder="category ascending")
                .update_layout(showlegend=False)
            )
            return hist_graph

        elif che_value != "$0k":
            df.loc[df.Activity == act_value, "Length minutes"] = df.loc[
                df.Activity == act_value, "Length minutes"
            ].apply(lambda x: x * increment)
            hist_graph = dcc.Graph(
                figure=px.histogram(
                    df,
                    x="Activity",
                    y="Length minutes",
                    color="colors",
                    histfunc=hist_data,
                    labels={"Length minutes": "Shift time"},
                )
                .update_xaxes(categoryorder="category ascending")
                .update_layout(showlegend=False)
            )
            return hist_graph


if __name__ == "__main__":
    app.run_server(debug=True, port=8001)
