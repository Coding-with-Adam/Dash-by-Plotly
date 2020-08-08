import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

df = px.data.gapminder()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

card_main = dbc.Card(
    [
        dbc.CardImg(src="/assets/ball_of_sun.jpg", top=True, bottom=False,
                    title="Image by Kevin Dinkel", alt='Learn Dash Bootstrap Card Component'),
        dbc.CardBody(
            [
                html.H4("Learn Dash with Charming Data", className="card-title"),
                html.H6("Lesson 1:", className="card-subtitle"),
                html.P(
                    "Choose the year you would like to see on the bubble chart.",
                    className="card-text",
                ),
                dcc.Dropdown(id='user_choice', options=[{'label': yr, "value": yr} for yr in df.year.unique()],
                             value=2007, clearable=False, style={"color": "#000000"}),
                # dbc.Button("Press me", color="primary"),
                # dbc.CardLink("GirlsWhoCode", href="https://girlswhocode.com/", target="_blank"),
            ]
        ),
    ],
    color="dark",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_question = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Question 1", className="card-title"),
            html.P("What was India's life expectancy in 1952?", className="card-text"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("A. 55 years"),
                    dbc.ListGroupItem("B. 37 years"),
                    dbc.ListGroupItem("C. 49 years"),
                ], flush=True)
        ]),
    ], color="warning",
)

card_graph = dbc.Card(
        dcc.Graph(id='my_bar', figure={}), body=True, color="secondary",
)


app.layout = html.Div([
    dbc.Row([dbc.Col(card_main, width=3),
             dbc.Col(card_question, width=3),
             dbc.Col(card_graph, width=5)], justify="around"),  # justify="start", "center", "end", "between", "around"

    # dbc.CardGroup([card_main, card_question, card_graph])   # attaches cards with equal width and height columns
    # dbc.CardDeck([card_main, card_question, card_graph])    # same as CardGroup but with gutter in between cards

    # dbc.CardColumns([                        # Cards organised into Masonry-like columns
    #         card_main,
    #         card_question,
    #         card_graph,
    #         card_question,
    #         card_question,
    # ])

])


@app.callback(
    Output("my_bar", "figure"),
    [Input("user_choice", "value")]
)
def update_graph(value):
    fig = px.scatter(df.query("year=={}".format(str(value))), x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", title=str(value),
                     hover_name="country", log_x=True, size_max=60).update_layout(showlegend=True, title_x=0.5)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
