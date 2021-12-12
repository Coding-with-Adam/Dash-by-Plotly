import dash
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

df = px.data.tips()
days = df.day.unique()

layout = html.Div(
    [
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in days],
            value=days[0],
            clearable=False,
            style={"width": "50%"}
        ),
        dcc.Graph(id="bar-chart"),
    ]
)


@callback(Output("bar-chart", "figure"), Input("dropdown", "value"))
def update_bar_chart(day):
    mask = df["day"] == day
    fig = px.bar(df[mask], x="sex", y="total_bill", color="smoker", barmode="group")
    return fig
