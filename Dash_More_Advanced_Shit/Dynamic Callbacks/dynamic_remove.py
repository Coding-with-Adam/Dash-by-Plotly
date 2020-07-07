import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State, MATCH
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv("Caste.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
        html.Button(
            'Add Chart', id='add-chart', n_clicks=0,
            # style={'display': 'inline-block'}
        ),
    ]),

    html.Div(id='container', children=[]),
    html.Button('Remove Chart', id='remove-chart', n_clicks=0),
])


@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks'),
     Input('remove-chart', 'n_clicks')],
    [State('container', 'children')],
    prevent_initial_call=True
)
def display_graphs(add_clicks, remove_clicks, div_children):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'add-chart':
        new_child = html.Div(
            children=[
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph',
                        'index': add_clicks
                    },
                    figure={}
                ),
                dcc.RadioItems(
                    id={
                        'type': 'dynamic-choice',
                        'index': add_clicks
                    },
                    options=[{'label': 'Bar Chart', 'value': 'bar'},
                             {'label': 'Line Chart', 'value': 'line'},
                             {'label': 'Pie Chart', 'value': 'pie'}],
                    value='bar',
                    style={"width": "50%"}
                ),
                dcc.Dropdown(
                    id={
                        'type': 'dynamic-dpn-s',
                        'index': add_clicks
                    },
                    options=[{'label': s, 'value': s} for s in np.sort(df['state_name'].unique())],
                    multi=True,
                    value=["Andhra Pradesh", "Maharashtra"],
                ),
                dcc.Dropdown(
                    id={
                        'type': 'dynamic-dpn-ctg',
                        'index': add_clicks
                    },
                    options=[{'label': c, 'value': c} for c in ['caste', 'gender', 'state_name']],
                    value='state_name',
                    clearable=False
                ),
                dcc.Dropdown(
                    id={
                        'type': 'dynamic-dpn-num',
                        'index': add_clicks
                    },
                    options=[{'label': n, 'value': n} for n in ['detenues', 'under_trial', 'convicts', 'others']],
                    value='convicts',
                    clearable=False
                )
            ]
        )
        div_children.append(new_child)

    elif triggered_id == 'remove-chart' and len(div_children) > 0:
        div_children = div_children[:-1]

    return div_children


@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input({'type': 'dynamic-dpn-s', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-dpn-ctg', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-dpn-num', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def update_graph(s_value, ctg_value, num_value, chart_choice):
    dff = df[df['state_name'].isin(s_value)]

    if chart_choice == 'bar':
        dff = dff.groupby([ctg_value], as_index=False)[['detenues', 'under_trial', 'convicts', 'others']].sum()
        fig = px.bar(dff, x=ctg_value, y=num_value)
        return fig
    elif chart_choice == 'line':
        if len(s_value) == 0:
            return {}
        else:
            dff = dff.groupby([ctg_value, 'year'], as_index=False)[['detenues', 'under_trial', 'convicts', 'others']].sum()
            fig = px.line(dff, x='year', y=num_value, color=ctg_value)
            return fig
    elif chart_choice == 'pie':
        fig = px.pie(dff, names=ctg_value, values=num_value)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
