from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
# Need to use Python 3.8 or higher and Dash 2.2.0 or higher

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = df[['continent', 'country', 'pop', 'lifeExp']]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Created sortable/non-sortable columns: produces by https://community.plotly.com/t/datatable-add-sorting-to-only-one-column/31399/8?u=adamschroeder
table_columns  = [
    {'name': 'Continent', 'id': 'continent', 'type': 'numeric', 'sortable': True},
    {'name': 'Country', 'id': 'country', 'type': 'text', 'sortable': True},
    {'name': 'Population', 'id': 'pop', 'type': 'numeric', 'sortable': False},
    {'name': 'Life Expectancy', 'id': 'lifeExp', 'type': 'numeric', 'sortable': False}
]

non_sortable_column_ids = [col['id'] for col in table_columns if col.pop('sortable') is False]
print(non_sortable_column_ids)
table_css = [
    {
        'selector': f'th[data-dash-column="{col}"] span.column-header--sort',
        'rule': 'display: none',
    }
    for col in non_sortable_column_ids
]
print(table_css)

app.layout = dbc.Container([
    dcc.Markdown('# Partially Sort Columns', style={'textAlign':'center'}),

    my_table := dash_table.DataTable(
        columns=table_columns,
        css=table_css,
        data=df.to_dict('records'),
        page_size=10,
        sort_action='native',

        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=False, port=8004)
