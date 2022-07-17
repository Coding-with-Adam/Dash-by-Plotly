import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SOLAR])
server = app.server

# page_reg = list(dash.page_registry.values())
# for x in page_reg:
#     print(x)
#     print('-------------------------------')

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
        ],
        nav=True,
        label="State",
    ),
    brand="The Fight Against Climate Change",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container
    ],
    fluid=False,
)


if __name__ == "__main__":
    app.run(debug=True)
