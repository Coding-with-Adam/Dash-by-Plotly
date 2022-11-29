
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP])


card_sales = dbc.Card(
    dbc.CardBody(
        [
            html.H1([html.I(className="bi bi-currency-dollar me-2"), "Sales"], className="text-nowrap"),
            html.H3("$106.7M"),
            html.Div(
                [
                    html.I("5.8%", className="bi bi-caret-up-fill text-success"),
                    " vs LY",
                ]
            ),
        ], className="border-start border-success border-5"
    ),
    className="text-center m-4"
)


card_profit = dbc.Card(
    dbc.CardBody(
        [
            html.H1([html.I(className="bi bi-bank me-2"), "Profit"], className="text-nowrap"),
            html.H3("$8.3M",),
            html.Div(
                [
                    html.I("12.3%", className="bi bi-caret-down-fill text-danger"),
                    " vs LY",
                ]
            ),
        ], className="border-start border-danger border-5"
    ),
    className="text-center m-4",
)


card_orders = dbc.Card(
    dbc.CardBody(
        [
            html.H1([html.I(className="bi bi-cart me-2"), "Orders"], className="text-nowrap"),
            html.H3("91.4K"),
            html.Div(
                [
                    html.I("10.3%", className="bi bi-caret-up-fill text-success"),
                    " vs LY",
                ]
            ),
        ], className="border-start border-success border-5"
    ),
    className="text-center m-4",
)

app.layout = dbc.Container(
    dbc.Row(
        [dbc.Col(card_sales), dbc.Col(card_profit), dbc.Col(card_orders)],
    ),
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
