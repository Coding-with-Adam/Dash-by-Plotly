import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.BOOTSTRAP])

coins = ["bitcoin", "ethereum", "binancecoin", "ripple"]
interval = 6000  # update frequency - adjust to keep within free tier
api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"


def get_data():
    try:
        response = requests.get(api_url, timeout=1)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)


def make_card(coin):
    change = coin["price_change_percentage_24h"]
    price = coin["current_price"]
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"
    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.Img(src=coin["image"], height=35, className="me-1"),
                        coin["name"],
                    ]
                ),
                html.H4(f"${price:,}"),
                html.H5(
                    [f"{round(change, 2)}%", html.I(className=icon), " 24hr"],
                    className=f"text-{color}",
                ),
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )


mention = html.A(
    "Data from CoinGecko", href="https://www.coingecko.com/en/api", className="small"
)
interval = dcc.Interval(interval=interval)
cards = html.Div()
app.layout = dbc.Container([interval, cards, mention], className="my-5")


@app.callback(Output(cards, "children"), Input(interval, "n_intervals"))
def update_cards(_):
    coin_data = get_data()
    if coin_data is None or type(coin_data) is dict:
        return dash.no_update

    # make a list of cards with updated prices
    coin_cards = []
    updated = None
    for coin in coin_data:
        if coin["id"] in coins:
            print(coin)
            updated = coin.get("last_updated")
            coin_cards.append(make_card(coin))

    # make the card layout
    card_layout = [
        dbc.Row([dbc.Col(card, md=3) for card in coin_cards]),
        dbc.Row(dbc.Col(f"Last Updated {updated}")),
    ]
    return card_layout


if __name__ == "__main__":
    app.run_server(debug=True)

