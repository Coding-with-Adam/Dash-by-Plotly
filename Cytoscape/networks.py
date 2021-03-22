import dash  # pip install dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd  # pip install pandas
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Cytoscape/org-data.csv")

app.layout = html.Div([
    html.Div([
        cyto.Cytoscape(
            id='org-chart',
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '500px'},
            elements=[
                # Nodes elements
                {'data': {'id': 'ed', 'label': 'Executive Director (Harriet)'},
                 'position': {'x': 150, 'y': 50},
                 'locked': True
                },

                {'data': {'id': 'vp1', 'label': 'Vice President (Sarah)'},
                 'position': {'x': 0, 'y': 150},
                 'grabbable': False
                },

                {'data': {'id': 'vp2', 'label': 'Vice President (Charlotte)'},
                 'position': {'x': 300, 'y': 150},
                'selectable': False
                },

                {'data': {'id': 'po1', 'label': 'Program Officer (Sojourner)'},
                 'position': {'x': -100, 'y': 250},
                 'selected': True
                },

                {'data': {'id': 'po2', 'label': 'Program Officer (Elizabeth)'},
                 'position': {'x': 150, 'y': 250}
                },

                {'data': {'id': 'pa', 'label': 'Program Associate (Ellen)'},
                 'position': {'x': 300, 'y': 350}
                },

                # Edge elements
                {'data': {'source': 'ed', 'target': 'vp1', 'label': 'ED to VP1'}},
                {'data': {'source': 'ed', 'target': 'vp2'}},
                {'data': {'source': 'vp1', 'target': 'po1'}},
                {'data': {'source': 'vp1', 'target': 'po2'}},
                {'data': {'source': 'vp2', 'target': 'pa'}},
            ]
        )
    ], className='six columns'),

    html.Div([
        dcc.Graph(id='my-graph')
    ], className='six columns'),

], className='row')


@app.callback(
    Output('my-graph','figure'),
    Input('org-chart','tapNodeData'),
)
def update_nodes(data):
    if data is None:
        dff = df.copy()
        dff.loc[dff.name == 'Program Officer (Sojourner)', 'color'] = "yellow"
        fig = px.bar(dff, x='name', y='slaves_freed')
        fig.update_traces(marker={'color': dff['color']})
        return fig
    else:
        print(data)
        dff = df.copy()
        dff.loc[dff.name == data['label'], 'color'] = "yellow"
        print(dff)
        fig = px.bar(dff, x='name', y='slaves_freed')
        fig.update_traces(marker={'color': dff['color']})
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)

    
# https://youtu.be/g8xBlilTV4w
