from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

# Instantiate our App and incorporate BOOTSTRAP theme stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Incorporate data into App
df = px.data.gapminder()
print(df.head())

# Build the scatter plot
fig = px.scatter(data_frame=df, x="gdpPercap", y="lifeExp", size="pop",
                 color="continent", hover_name="country", log_x=True,
                 size_max=60, range_y=[30, 90], animation_frame='year')

# Build the layout to define what will be displayed on the page
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Life Expectancy vs. GDP", style={'textAlign': 'center'})
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='our-plot', figure=fig)
        ], width=12)
    ])
])


# callback is used to create app interactivity
#@callback()

# Run the App
if __name__ == '__main__':
    app.run_server()
