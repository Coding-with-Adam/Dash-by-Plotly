import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])  # https://bootswatch.com/default/

app.layout = html.Div([
    html.Div(html.H6("Product: a beautiful Pizza reheated after a day in the fridge, for $99"), style={"text-align":"center"}),
    html.Hr(),
    dbc.CardHeader(
            dbc.Button(
                "Why should I buy reheated pizza for $99?",
                color="link",
                id="button-question-1",
            )
    ),
    dbc.Collapse(
        dbc.CardBody("Because it's a lot better than a hotdog."),
        id="collapse-question-1", is_open=False
    ),

    dbc.CardHeader(
            dbc.Button(
                "Does it have extra cheese?",
                color="link",
                id="button-question-2",
            )
    ),
    dbc.Collapse(
        dbc.CardBody("Yes, and it is made from the goats of Antarctica, which keeps the cheese cold and fresh."),
        id="collapse-question-2", is_open=False
    ),
])


@app.callback(
    Output("collapse-question-1", "is_open"),
    [Input("button-question-1", "n_clicks")],
    [State("collapse-question-1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-question-2", "is_open"),
    [Input("button-question-2", "n_clicks")],
    [State("collapse-question-2", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True, port=2000)
