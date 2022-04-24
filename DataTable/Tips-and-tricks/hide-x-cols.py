from dash import Dash, dash_table, dcc, html, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
# Need to use Python 3.8 or higher and Dash 2.2.0 or higher

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = df[['continent', 'country', 'pop', 'lifeExp']]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    dcc.Markdown('# Hide Columns per Screen Size', style={'textAlign':'center'}),

    my_table := dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'Continent', 'id': 'continent', 'type': 'numeric'},
            {'name': 'Country', 'id': 'country', 'type': 'text'},
            {'name': 'Population', 'id': 'pop', 'type': 'numeric'},
            {'name': 'Life Expectancy', 'id': 'lifeExp', 'type': 'numeric'}
        ],
        data=df.to_dict('records'),
        page_size=10,

        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    ),
    dcc.Location(id='_pages_plugin_location')
])

# this assumes users will not resize the window on their own
# produced by @raptorbrad- https://community.plotly.com/t/how-to-hide-datatable-columns-based-on-screen-size/60582/3?u=adamschroeder
app.clientside_callback(
    """
        function(href) {
            if (window.innerWidth < 750) {
                return ['continent', 'lifeExp']
            }
            return []
        }
    """,
    Output('table', 'hidden_columns'),
    Input('_pages_plugin_location', 'href')
)


if __name__ == '__main__':
    app.run_server(debug=False, port=8003)
