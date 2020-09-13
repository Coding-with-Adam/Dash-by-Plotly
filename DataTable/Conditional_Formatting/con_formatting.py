import dash  # you need Dash version 1.15.0 or higher
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px
from table_bars import data_bars

df = pd.read_csv('medical supplies.csv')
df["Part sent date"] = pd.to_datetime(df["Part sent date"]).dt.date
df["Part received date"] = pd.to_datetime(df["Part received date"]).dt.date
df['Prioritize'] = df['Machines'].apply(lambda x:
                                        '⭐⭐⭐' if x > 3000 else (
                                            '⭐⭐' if x > 1000 else (
                                                '⭐' if x > 500 else '')))

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='mydatatable',
        columns=[
            {'name': 'S/N', 'id': 'Serial number', 'type': 'numeric', 'editable': True},
            {'name': 'Machines', 'id': 'Machines', 'type': 'numeric', 'editable': False},
            {'name': 'Country', 'id': 'Country', 'type': 'text', 'editable': True},
            {'name': 'Part sent date', 'id': 'Part sent date', 'type': 'datetime', 'editable': True},
            {'name': 'Part received date', 'id': 'Part received date', 'type': 'datetime', 'editable': True},
            {'name': 'Elapsed Days', 'id': 'Elapsed Days', 'type': 'numeric', 'editable': True},
            {'name': 'Origin supplier', 'id': 'Origin supplier', 'type': 'text', 'editable': True},
            {'name': 'Feedback', 'id': 'Feedback', 'type': 'text', 'editable': True},
            {'name': 'Prioritize', 'id': 'Prioritize', 'type': 'text', 'editable': False},

        ],
        data=df.to_dict('records'),
        style_data_conditional=(
            [
                # 'filter_query', 'column_id', 'column_type', 'row_index', 'state', 'column_editable'.
                # filter_query ****************************************
                {
                    'if': {
                        'filter_query': '{Elapsed Days} > 40 && {Elapsed Days} < 60',
                        'column_id': 'Elapsed Days'
                    },
                    'backgroundColor': 'hotpink',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{Country} = Canada'
                    },
                    'backgroundColor': '#FFFF00',
                },
                # Compare columns *************************************
                {
                    'if': {
                        'filter_query': '{Part sent date} > {Part received date}',
                        'column_id': 'Part sent date'
                    },
                    'fontWeight': 'bold',
                    'color': 'red'
                },
                # Format empty cell ***********************************
                {
                    'if': {
                        'filter_query': '{Origin supplier} is blank',
                        'column_id': 'Origin supplier'
                    },
                    'backgroundColor': 'gray',
                },
                # Align text to the left ******************************
                {
                    'if': {
                        'column_type': 'text'
                        # 'text' | 'any' | 'datetime' | 'numeric'
                    },
                    'textAlign': 'left'
                },
                # Format any cell/row you want ************************
                {
                    'if': {
                        'row_index': 0,
                        'column_id': 'Feedback'
                    },
                    'backgroundColor': 'purple',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                # Format active cells *********************************
                {
                    'if': {
                        'state': 'active'  # 'active' | 'selected'
                    },
                    'border': '3px solid rgb(0, 116, 217)'
                },
                {
                    'if': {
                        'column_editable': False  # True | False
                    },
                    'cursor': 'not-allowed'
                },
            ]

            +

            [   # Highlighting bottom three values in a column ********
                {
                    'if': {
                        'filter_query': '{{Machines}} = {}'.format(i),
                        'column_id': 'Machines',
                    },
                    'backgroundColor': '#7FDBFF',
                    'color': 'white'
                }
                for i in df['Machines'].nsmallest(3)
            ]

            +

            # Adding data bars to numerical columns *******************
            data_bars(df, 'Serial number')

        )
    ),

    html.Div(dcc.Graph(id='mybar', figure={}))
])


@app.callback(
    Output(component_id='mybar', component_property='figure'),
    Input(component_id='mydatatable', component_property='derived_virtual_data')
)
def table_to_graph(row_data):
    df_table = df if row_data is None else pd.DataFrame(row_data)
    fig = px.bar(df_table, x='Country', y='Machines')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
