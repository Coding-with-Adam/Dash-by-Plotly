from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

df = px.data.tips()
days = df.day.unique()

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

day_dropdown = dcc.Dropdown(
    id="dropdown",
    options=[{"label": x, "value": x} for x in days],
    value=days[0],
    clearable=False,
    className="mt-3",
)

fake_dropdown = dbc.Select(
    id="fake-bootstrap-dropdown",
    options=[{"label": x, "value": x} for x in df.sex.unique()],
    value="",
    placeholder="Fake disconnected dropdown for tutorial purposes",
    className="bg-success mt-3"
)


app.layout = dbc.Container([
    html.Br(),
    html.Span("Utility Border", className="border"),  # border-top, border border-danger, border border-3, border rounded-circle
    html.Div("Utility Color", className="text-primary"),  # text-light, bg-success
    html.Div("Utility Opacity", className="opacity-25"),  # opacity-75
    html.Div("Utility Spacing", className="border m-2"),  # m-5, ms-2, my-4, p-3, pb-5
    html.Div("Utility Text : with nowrap", style={"width":15}, className="text-nowrap"),  # text-wrap, text-break, fs-3, text-decoration-line-through
    html.Div(["Utility Typography : you can use html.Mark to ", html.Mark("highlight"), " text"]),
    html.Div("Example of many classes combined",
             className="opacity-100 p-2 m-1 bg-primary text-light fw-bold rounded"),

    dbc.Row([
        dbc.Col(day_dropdown, width=6),
        dbc.Col(fake_dropdown, width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="bar-chart"), width=12)
    ]),
])


@app.callback(
    Output("bar-chart", "figure"), 
    [Input("dropdown", "value")])
def update_bar_chart(day):
    mask = df["day"] == day
    fig = px.bar(df[mask], x="sex", y="total_bill", 
                 color="smoker", barmode="group")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8002)
