from dash import Dash, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd


df = pd.read_csv("country trade register.csv")


app = Dash()
app.layout = [
    dcc.RadioItems(["Supplier", "Recipient"], value="Supplier", id="radio-btn"),
    dcc.RangeSlider(
        min=df["Delivery year"].min(),
        max=df["Delivery year"].max(),
        step=1,
        value=[df["Delivery year"].min(), df["Delivery year"].max() - 13],
        id="years",
        marks={
            2000: "2000",
            2002: "02",
            2004: "04",
            2006: "06",
            2008: "08",
            2010: "2010",
            2012: "12",
            2014: "14",
            2016: "16",
            2018: "18",
            2020: "20",
            2022: "22",
            2023: "2023",
        },
    ),
    dcc.Graph(id="my-graph"),
]


@callback(
    Output("my-graph", "figure"),
    Input("radio-btn", "value"),
    Input("years", "value"),
)
def update_graph(selected_value, selected_years):
    # print(selected_years)
    # [2000,2023]
    if selected_years[0] == selected_years[1]:
        dff = df[df["Delivery year"] == selected_years[0]]
    else:
        dff = df[
            df["Delivery year"].isin(range(selected_years[0], selected_years[1] + 1))
        ]
        # print(dff['Delivery year'].unique())
    if selected_value == "Supplier":
        fig = px.treemap(
            dff,
            path=[px.Constant("all"), selected_value, "Recipient", "Armament category"],
            values="Numbers delivered",
            title=f"Suppliers of Armaments from {selected_years[0]} to {selected_years[1]}",
            height=650,
        )
    else:
        fig = px.treemap(
            dff,
            path=[px.Constant("all"), selected_value, "Supplier", "Armament category"],
            values="Numbers delivered",
            title=f"Recipients of Armaments from {selected_years[0]} to {selected_years[1]}",
            height=650,
        )

    fig.update_layout(margin=dict(l=10, r=10, t=30, b=30))
    return fig


@callback(Input("my-graph", "clickData"))
def country_info(clicked):
    print(f"Label is: {clicked['points'][0]['label']}")
    print(f"Value is: {clicked['points'][0]['value']}")
    print(f"Parent is: {clicked['points'][0]['parent']}")


if __name__ == "__main__":
    app.run_server(debug=False)
