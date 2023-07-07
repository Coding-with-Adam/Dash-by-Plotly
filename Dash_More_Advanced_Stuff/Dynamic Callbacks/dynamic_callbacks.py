import dash  # version 1.13.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv("Caste.csv")
df.rename(columns={'under_trial': 'under trial', 'state_name': 'state'}, inplace=True)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
        html.Button('Add Chart', id='add-chart', n_clicks=0),
    ]),
    html.Div(id='container', children=[])
])


@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                options=[{'label': 'Bar Chart', 'value': 'bar'},
                         {'label': 'Line Chart', 'value': 'line'},
                         {'label': 'Pie Chart', 'value': 'pie'}],
                value='bar',
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-s',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in np.sort(df['state'].unique())],
                multi=True,
                value=["Andhra Pradesh", "Maharashtra"],
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-ctg',
                    'index': n_clicks
                },
                options=[{'label': c, 'value': c} for c in ['caste', 'gender', 'state']],
                value='state',
                clearable=False
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-num',
                    'index': n_clicks
                },
                options=[{'label': n, 'value': n} for n in ['detenues', 'under trial', 'convicts', 'others']],
                value='convicts',
                clearable=False
            )
        ]
    )
    div_children.append(new_child)
    return div_children


@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-s', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-ctg', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-num', 'index': MATCH}, component_property='value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def update_graph(s_value, ctg_value, num_value, chart_choice):
    print(s_value)
    dff = df[df['state'].isin(s_value)]

    if chart_choice == 'bar':
        dff = dff.groupby([ctg_value], as_index=False)[['detenues', 'under trial', 'convicts', 'others']].sum()
        fig = px.bar(dff, x=ctg_value, y=num_value)
        return fig
    elif chart_choice == 'line':
        if len(s_value) == 0:
            return {}
        else:
            dff = dff.groupby([ctg_value, 'year'], as_index=False)[['detenues', 'under trial', 'convicts', 'others']].sum()
            fig = px.line(dff, x='year', y=num_value, color=ctg_value)
            return fig
    elif chart_choice == 'pie':
        fig = px.pie(dff, names=ctg_value, values=num_value)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
