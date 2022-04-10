from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# Instantiate our App and incorporate BOOTSTRAP theme stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Incorporate data into App
df = px.data.gapminder()
print(df.columns)

# Build the layout to define what will be displayed on the page
app.layout = dbc.Container([
    dbc.Row([
       dbc.Col([
           html.H1("The Title of Our App")
       ], width=8)
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            html.Label('Dropdown'),
            dcc.Dropdown(options=[x for x in df.year.unique()],
                         value=df.year[0]),
        ], width=6),
        dbc.Col([
            html.Label('Radio Items'),
            dcc.RadioItems(options=['New York City', 'Montréal', 'San Francisco'],
                           value='Montréal'),
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            html.Label('Slider'),
            dcc.Slider(min=0, max=10, step=1, value=5),
        ], width=6),
        dbc.Col([
            html.Label('Text Input'),
            html.Br(),
            dcc.Input(value='Initial text', type='text'),
        ], width=6)
    ]),
])

# callback is used to create app interactivity
#@callback()

# Run the App
if __name__ == '__main__':
    app.run_server(port=8001)
