# This Code was written by Ann Marie - a Plotly Forum Moderator
from dash import Dash, dcc, html, Input, Output, dash_table, no_update  # Dash version >= 2.0.0
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = px.data.gapminder()
df["id"] = df.index
# print(df.head(15))
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
            className="five columns"
        ),
        html.Div(id="output-graph", className="six columns"),
    ],
    className="row"
)


@app.callback(
    Output("output-graph", "children"), Input("table", "active_cell"),
)
def cell_clicked(active_cell):
    if active_cell is None:
        return no_update

    row = active_cell["row_id"]
    print(f"row id: {row}")

    country = df.at[row, "country"]
    print(country)

    col = active_cell["column_id"]
    print(f"column id: {col}")
    print("---------------------")

    y = col if col in ["pop", "gdpPercap"] else "lifeExp"

    fig = px.line(
        df[df["country"] == country], x="year", y=y, title=" ".join([country, y])
    )
    fig.update_layout(title={"font_size": 20},  title_x=0.5, margin=dict(t=190, r=15, l=5, b=5))
    fig.update_traces(line=dict(color=color[y]))

    return dcc.Graph(figure=fig)


if __name__ == "__main__":
    app.run_server(debug=True)
