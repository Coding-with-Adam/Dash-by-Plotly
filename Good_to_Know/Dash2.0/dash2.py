from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# incorporate data into app
df = pd.read_csv("social_capital.csv")
print(df.head())

# Customize your own Layout
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

figure_space = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df.columns.values[2:],
                        value='Cesarean Delivery Rate',
                        clearable=False)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([figure_space], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),

], fluid=True)

# Callback allows components to interact
@app.callback(
    Output(figure_space, 'figure'),
    Input(dropdown, 'value')
)
def update_graph(column_name):
    # https://plotly.com/python/choropleth-maps/
    fig = px.choropleth(data_frame=df,
                        locations='STATE',
                        locationmode="USA-states",
                        scope="usa",
                        height=700,
                        color=column_name,
                        title=column_name,
                        animation_frame='YEAR')
    return fig

# Run app
if __name__=='__main__':
    app.run_server(debug=True)