import dash
from dash import dcc, callback, Output, Input, dash_table  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px

df = px.data.tips()
print(df.head())
# convert dataframe to list of dictionaries because dcc.Store
# accepts dict | list | number | string | boolean
df = df.to_dict('records')

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True, use_pages=True
)

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

app.layout = dbc.Container(
    [navbar,dash.page_container,
     dcc.Store(id="stored-data", data=df),
     dcc.Store(id="store-dropdown-value", data=None)
     ],
    fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True, port=8003)

