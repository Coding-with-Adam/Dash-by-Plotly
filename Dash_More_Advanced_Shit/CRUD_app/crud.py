import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Input(
            id='adding-rows-name',
            placeholder='Enter a column name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Column', id='adding-columns-button', n_clicks=0)
    ], style={'height': 50}),

    dash_table.DataTable(
        id='our-table',
        columns=[{'name': 'Product', 'id': 'Product', 'deletable': False, 'renamable': False},
                 {'name': 'Version', 'id': 'Version', 'deletable': True, 'renamable': True},
                 {'name': 'Price', 'id': 'Price', 'deletable': True, 'renamable': True},
                 {'name': 'Sales', 'id': 'Sales', 'deletable': False, 'renamable': False}],
        data=[{'Product': 'Iphone', 'Version': '6a', 'Price': 799, 'Sales': 2813},
              {'Product': 'Iphone', 'Version': '9', 'Price': 900, 'Sales': 5401},
              {'Product': 'Iphone', 'Version': '7', 'Price': 799, 'Sales': 2513},
              {'Product': 'Iphone', 'Version': '8', 'Price': 850, 'Sales': 5401},
              {'Product': 'Galaxy', 'Version': 'S9', 'Price': 900, 'Sales': 6084},
              {'Product': 'Galaxy', 'Version': 'S10', 'Price': 1000, 'Sales': 7084},
              {'Product': 'Galaxy', 'Version': 'S20', 'Price': 1200, 'Sales': 9084},
              {'Product': 'Pixel', 'Version': '1', 'Price': 400, 'Sales': 2084},
              {'Product': 'Pixel', 'Version': '2', 'Price': 500, 'Sales': 3033},
              {'Product': 'Pixel', 'Version': '3', 'Price': 600, 'Sales': 6000}],
        editable=True,                  # allow user to edit data inside tabel
        row_deletable=True,             # allow user to delete rows
        sort_action="native",           # give user capability to sort columns
        sort_mode="single",             # sort across 'multi' or 'single' columns
        filter_action="native",         # allow filtering of columns
        page_action='none',             # render all of the data at once. No paging.
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'right'
            } for c in ['Price', 'Sales']
        ]
    ),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),
    html.Button('Export to Excel', id='save_to_csv', n_clicks=0),

    # Create notification when saving to excel
    html.Div(id='placeholder', children=[]),
    dcc.Store(id="store", data=0),
    dcc.Interval(id='interval', interval=1000),

    dcc.Graph(id='my_graph')

])
# ------------------------------------------------------------------------------------------------


@app.callback(
    Output('our-table', 'columns'),
    [Input('adding-columns-button', 'n_clicks')],
    [State('adding-rows-name', 'value'),
     State('our-table', 'columns')],
)
def add_columns(n_clicks, value, existing_columns):
    print(existing_columns)
    if n_clicks > 0:
        existing_columns.append({
            'name': value, 'id': value,
            'renamable': True, 'deletable': True
        })
    print(existing_columns)
    return existing_columns


@app.callback(
    Output('our-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('our-table', 'data'),
     State('our-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    # print(rows)
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    # print(rows)
    return rows


@app.callback(
    Output('my_graph', 'figure'),
    [Input('our-table', 'data')])
def display_graph(data):
    df_fig = pd.DataFrame(data)
    # print(df_fig)
    fig = px.bar(df_fig, x='Product', y='Sales')
    return fig


@app.callback(
    [Output('placeholder', 'children'),
     Output("store", "data")],
    [Input('save_to_csv', 'n_clicks'),
     Input("interval", "n_intervals")],
    [State('our-table', 'data'),
     State('store', 'data')]
)
def df_to_csv(n_clicks, n_intervals, dataset, s):
    output = html.Plaintext("The data has been saved to your folder.",
                            style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
    no_output = html.Plaintext("", style={'margin': "0px"})

    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if input_triggered == "save_to_csv":
        s = 6
        df = pd.DataFrame(dataset)
        df.to_csv("Your_Sales_Data.csv")
        return output, s
    elif input_triggered == 'interval' and s > 0:
        s = s-1
        if s > 0:
            return output, s
        else:
            return no_output, s
    elif s == 0:
        return no_output, s


if __name__ == '__main__':
    app.run_server(debug=True)
