from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
# Need to use Python 3.8 or higher and Dash 2.2.0 or higher

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = df[['continent', 'country', 'pop', 'lifeExp']]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    dcc.Markdown('# DataTable Tips and Tricks', style={'textAlign':'center'}),

    dbc.Label("Show number of rows"),
    row_drop := dcc.Dropdown(value=10, clearable=False, style={'width':'35%'},
                             options=[10, 25, 50, 100]),

    my_table := dash_table.DataTable(
        columns=[
            {'name': 'Continent', 'id': 'continent', 'type': 'numeric'},
            {'name': 'Country', 'id': 'country', 'type': 'text'},
            {'name': 'Population', 'id': 'pop', 'type': 'numeric'},
            {'name': 'Life Expectancy', 'id': 'lifeExp', 'type': 'numeric'}
        ],
        data=df.to_dict('records'),
        filter_action='native',
        page_size=10,

        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    ),
    dbc.Row([
        dbc.Col([
            continent_drop := dcc.Dropdown([x for x in sorted(df.continent.unique())])
        ], width=3),
        dbc.Col([
            country_drop := dcc.Dropdown([x for x in sorted(df.country.unique())], multi=True)
        ], width=3),
        dbc.Col([
            pop_slider := dcc.Slider(0, 1500000000, 5000000, marks={'1000000000':'1 billion', '1500000000':'1.5 billion'},
                                     value=0, tooltip={"placement": "bottom", "always_visible": True})
        ], width=3),
        dbc.Col([
            lifeExp_slider := dcc.Slider(0, 100, 1, marks={'100':'100'}, value=20,
                                   tooltip={"placement": "bottom", "always_visible": True})
        ], width=3),

    ], justify="between", className='mt-3 mb-4'),

])

@callback(
    Output(my_table, 'data'),
    Output(my_table, 'page_size'),
    Input(continent_drop, 'value'),
    Input(country_drop, 'value'),
    Input(pop_slider, 'value'),
    Input(lifeExp_slider, 'value'),
    Input(row_drop, 'value')
)
def update_dropdown_options(cont_v, country_v, pop_v, life_v, row_v):
    dff = df.copy()

    if cont_v:
        dff = dff[dff.continent==cont_v]
    if country_v:
        dff = dff[dff.country.isin(country_v)]

    dff = dff[(dff['pop'] >= pop_v) & (dff['pop'] < 1500000000)]
    dff = dff[(dff['lifeExp'] >= life_v) & (dff['lifeExp'] < 100)]

    return dff.to_dict('records'), row_v


if __name__ == '__main__':
    app.run_server(debug=True, port=8001)
