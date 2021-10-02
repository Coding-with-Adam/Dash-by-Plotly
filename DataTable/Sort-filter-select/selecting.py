# This Code was written by Ann Marie
from dash import Dash, dcc, html, Input, Output, dash_table, no_update  # Dash version >= 2.0.0
import plotly.express as px

app = Dash(__name__)

df = px.data.gapminder()
df["id"] = df.index
dff = df[df.year == 2007]
columns = ["country", "continent", "lifeExp", "pop", "gdpPercap"]
color = {"lifeExp": "#636EFA", "pop": "#EF553B", "gdpPercap": "#00CC96"}
initial_active_cell = {"row": 0, "column": 0, "column_id": "country", "row_id": 0}

app.layout = html.Div(
    [
        html.Div(
            [
                html.H3("2007 Gap Minder", style={"textAlign":"center"}),
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": c, "id": c} for c in columns],
                    data=dff.to_dict("records"),
                    page_size=10,
                    sort_action="native",
                    active_cell=initial_active_cell,
                ),
            ],
            style={"margin": 50},
        ),
        html.Div(id="output-graph"),
    ]
)


@app.callback(
    Output("output-graph", "children"), Input("table", "active_cell"),
)
def cell_clicked(active_cell):
    if active_cell is None:
        return no_update

    row = active_cell["row_id"]
    col = active_cell["column_id"]
    country = df.at[row, "country"]
    y = col if col in ["pop", "gdpPercap"] else "lifeExp"

    fig = px.line(
        df[df["country"] == country], x="year", y=y, title=" ".join([country, y])
    )
    fig.update_layout(title={"font_size": 20})
    fig.update_traces(line=dict(color=color[y]))

    return dcc.Graph(figure=fig)


if __name__ == "__main__":
    app.run_server(debug=True)