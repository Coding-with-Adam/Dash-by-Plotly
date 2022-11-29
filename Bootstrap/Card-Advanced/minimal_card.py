from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP])

# MINIMAL DASH BOOTSTRAP CARD-------------------------------------------------------------------------------------------
card =  dbc.Card(
    dbc.CardBody(
        [
            html.H1("Sales"),
            html.H3("$104.2M")
        ],
    ),
)


# STYLING THE CARD (adding color and centering text)--------------------------------------------------------------------
# card =  dbc.Card(
#     dbc.CardBody(
#         [
#             html.H1("Sales"),
#             html.H3("$104.2M", className="text-success")
#         ],
#     ),
#     className="text-center"
# )


# CARD WITH ICONS (adding icon and background color)-------------------------------------------------------------------
# card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H1(children=[html.I(className="bi bi-bank me-2"), "Profit"]),
#             html.H3("$8.3M"),
#             html.H4(html.I("10.3% vs LY", className="bi bi-caret-up-fill text-success")),
#         ],
#     ),
#     className="text-center m-4 bg-primary text-white",
# )


app.layout=dbc.Container(card)


if __name__ == "__main__":
    app.run_server(debug=True)
