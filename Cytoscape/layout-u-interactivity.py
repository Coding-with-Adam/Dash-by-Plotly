import dash  # pip install dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd  # pip install pandas
import plotly.express as px
import math

# Load extra layouts
# cyto.load_extra_layouts()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Cytoscape/org-data.csv")

# layouts: preset, random, cose, circular, grid, breadthfirst, concentric, external layouts
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='dpdn',
            value='breadthfirst',
            clearable=False,
            options=[
                {'label': name.capitalize(), 'value': name}
                for name in ['breadthfirst' ,'grid', 'random', 'circle', 'cose', 'concentric']
            ]
        ),
        cyto.Cytoscape(
            id='org-chart',
            autoungrabify=True,
            minZoom=0.2,
            maxZoom=1,
            layout={'name': 'breadthfirst'},

            # layout={
            #     'name': 'circle',
            #     'radius': 250,
            #     'startAngle': math.pi * 1 / 9,
            #     'sweep': math.pi * 1 / 3
            # },

            # layout={
            #     'name': 'grid',
            #     'rows': 2,
            #     'cols': 4
            # },

            # layout={
            #     'name': 'breadthfirst', # tree
            #     'roots': '[id = "Executive Director (Harriet)"]'
            #     # 'roots': '#vp1, #vp2'
            #
            # },

            style={'width': '100%', 'height': '500px'},
            elements=
                [
                    # Nodes elements
                    {'data': {'id': x, 'label': x}} for x in df.name
                ]
                +
                [
                    # Edge elements
                    {'data': {'source': 'Executive Director (Harriet)', 'target': 'Vice President (Sarah)'}},
                    {'data': {'source': 'Executive Director (Harriet)', 'target': 'Vice President (Charlotte)'}},
                    {'data': {'source': 'Vice President (Sarah)', 'target': 'Program Officer (Sojourner)'}},
                    {'data': {'source': 'Vice President (Sarah)', 'target': 'Program Officer (Elizabeth)'}},
                    {'data': {'source': 'Vice President (Charlotte)', 'target': 'Program Associate (Ellen)'}},
                ]
        )
    ], className='six columns'),

    html.Div([
        html.Div(id='empty-div', children='')
    ],className='one column'),

    html.Div([
        dcc.Graph(id='my-graph', figure=px.bar(df, x='name', y='slaves_freed'))
    ], className='five columns'),

], className='row')


@app.callback(Output('org-chart', 'layout'),
              Input('dpdn', 'value'))
def update_layout(layout_value):
    if layout_value == 'breadthfirst':
        return {
        'name': layout_value,
        'roots': '[id = "Executive Director (Harriet)"]',
        'animate': True
        }
    else:
        return {
            'name': layout_value,
            'animate': True
        }


@app.callback(
    Output('empty-div', 'children'),
    Input('org-chart', 'mouseoverNodeData'),
    Input('org-chart','mouseoverEdgeData'),
    Input('org-chart','tapEdgeData'),
    Input('org-chart','tapNodeData'),
    Input('org-chart','selectedNodeData')
)
def update_layout(mouse_on_node, mouse_on_edge, tap_edge, tap_node, snd):
    print("Mouse on Node: {}".format(mouse_on_node))
    print("Mouse on Edge: {}".format(mouse_on_edge))
    print("Tapped Edge: {}".format(tap_edge))
    print("Tapped Node: {}".format(tap_node))
    print("------------------------------------------------------------")
    print("All selected Nodes: {}".format(snd))
    print("------------------------------------------------------------")

    return 'see print statement for nodes and edges selected.'


@app.callback(
    Output('my-graph','figure'),
    Input('org-chart','tapNodeData'),
)
def update_nodes(data):
    if data is None:
        return dash.no_update
    else:
        dff = df.copy()
        dff.loc[dff.name == data['label'], 'color'] = "yellow"
        fig = px.bar(dff, x='name', y='slaves_freed')
        fig.update_traces(marker={'color': dff['color']})
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)

    
# https://youtu.be/Ip2x7mmrBYY
