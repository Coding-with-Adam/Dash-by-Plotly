
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

count = "https://user-images.githubusercontent.com/72614349/194616425-107a62f9-06b3-4b84-ac89-2c42e04c00ac.png"

# CARD WITH IMAGE-------------------------------------------------------------------------------------------------------
card = dbc.Card([
    dbc.CardImg(src=count, top=True),
    dbc.CardBody(
        [
            html.H3("Count von Count", className="text-primary"),
            html.Div("Chief Financial Officer"),
            html.Div("Sesame Street, Inc.", className="small"),
        ]
    )],
    className="shadow my-2",
    style={"maxWidth": 350},
)


# ADD LINK TO IMAGE-----------------------------------------------------------------------------------------------------
# card = dbc.Card([
#     dbc.CardLink(
#         [
#             dbc.CardImg(src=count, top=True)
#         ],
#         href="https://en.wikipedia.org/wiki/Count_von_Count"
#     ),
#     dbc.CardBody(
#         [
#             html.H3("Count von Count", className="text-primary"),
#             html.Div("Chief Financial Officer"),
#             html.Div("Sesame Street, Inc.", className="small"),
#         ]
#     )],
#     className="shadow my-2",
#     style={"maxWidth": 350},
# )


# IMAGE IN BACKGROUND---------------------------------------------------------------------------------------------------
# card = dbc.Card([
#     dbc.CardImg(src=count),
#     dbc.CardImgOverlay([
#         dbc.CardBody(
#             [
#                 html.H3("Count von Count", className="text-light text-center")
#             ],
#             style={"marginTop":160})
#     ])
# ],
#     className="shadow my-2",
#     style={"maxWidth": 350},
# )


app.layout=dbc.Container(card)

if __name__ == "__main__":
    app.run_server(debug=True)
