import altair as alt                                                  # pip install altair
from dash import Dash, Input, Output, callback, dcc, html, no_update  # pip install dash
from vega_datasets import data                                        # pip install vega_datasets
import dash_vega_components as dvc                                    # pip install dash_vega_components
import plotly.express as px

app = Dash()

app.layout = html.Div(
    [
        html.H1("Altair Chart"),
        dcc.Dropdown(options=["All", "USA", "Europe", "Japan"], value="All", id="origin-dropdown"),
        dvc.Vega(id="altair-chart", opt={"renderer": "svg", "actions": False}, spec={}),
    ]
)


@callback(
    Output(component_id="altair-chart", component_property="spec"),
    Input(component_id="origin-dropdown", component_property="value")
)
def display_altair_chart(origin):
    source = data.cars()
    # print(source.head())

    if origin != "All":
        source = source[source["Origin"] == origin]

    chart = (
        alt.Chart(source)
        .mark_circle(size=60)
        .encode(
            x="Horsepower",
            y="Miles_per_Gallon",
            color=alt.Color("Origin").scale(domain=["Europe", "Japan", "USA"]),
            tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
        )
        .interactive()
    )

    # source2 = px.data.medals_long()
    # # print(source2)
    # chart2 = alt.Chart(source2).mark_bar().encode(
    #     x='nation',
    #     y='count',
    #     color=alt.condition(
    #         alt.datum.count > 14,    # If the year is bigger than 14 this test returns True,
    #         alt.value('orange'),     # which sets the bar orange.
    #         alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    #     )
    # ).properties(width=400)

    return chart.to_dict() #chart.to_dict



if __name__ == "__main__":
    app.run(debug=True)
