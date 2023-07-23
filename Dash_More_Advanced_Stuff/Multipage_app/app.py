import dash  # pip install dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True
)

# for x in dash.page_registry.values():
#     print(x)

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Multi Page App Plugin Demo",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(html.Div([
    navbar, dash.page_container
]), fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
