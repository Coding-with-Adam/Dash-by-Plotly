import dash  # pip install dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd  # pip install pandas

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Cytoscape/org-data.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

my_elements=[
    # Nodes elements
    {'data': {'id': 'ed', 'label': 'Executive Director (Harriet)'},
     'classes': 'purple' # One class
     },

    {'data': {'id': 'vp1', 'label': 'Vice President (Sarah)'},
     'classes': 'square' # One class
     },

    {'data': {'id': 'vp2', 'label': 'Vice President (Charlotte)'},
     'classes': 'square' # One class
     },

    {'data': {'id': 'po1', 'label': 'Program Officer (Sojourner)'},
     'classes': 'green diamond'  # Multiple classes
     },

    {'data': {'id': 'po2', 'label': 'Program Officer (Elizabeth)'},
     'classes': 'green diamond ' # Multiple classes
     },

    {'data': {'id': 'pa', 'label': 'Program Associate (Ellen)'},
     'classes': 'myimage' # One class
     },

    # Edge elements
    {'data': {'source': 'ed', 'target': 'vp1', 'weight': 1}, 'classes': 'purple'},
    {'data': {'source': 'ed', 'target': 'vp2', 'weight': 2}},
    {'data': {'source': 'vp1', 'target': 'po1', 'weight': 3}},
    {'data': {'source': 'vp1', 'target': 'po2', 'weight': 4}},
    {'data': {'source': 'vp2', 'target': 'pa', 'weight': 5}}
]

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
            minZoom=0.2,
            maxZoom=2,
            layout={'name': 'breadthfirst'},
            elements=my_elements,
            style={'width': '100%', 'height': '500px'},
            stylesheet=[
                # Group selectors for NODES
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)'
                    }
                },

                # Group selectors for EDGES
                {
                    'selector': 'edge',
                    'style': {
                        'label': 'data(weight)'
                    }
                },

                # Class selectors
                {
                    'selector': '.purple',
                    'style': {
                        'background-color': 'purple',
                        'line-color': 'purple'
                    }
                },
                {
                    'selector': '.square',
                    'style': {
                        'shape': 'square',
                    }
                },
                {
                    'selector': '.myimage',
                    'style': {
                        'width': 100,
                        'height': 100,
                        'background-image': ['./assets/sunny-and-cloud.jpg']
                    }
                },
                {
                    'selector': '.green',
                    'style': {
                        'background-color': 'green',
                        'line-color': 'green'
                    }
                },
                {
                    'selector': '.diamond',
                    'style': {
                        'shape': 'diamond',
                    }
                },

                # Conditional Styling
                # this weight class only exists within the EDGES
                {
                    'selector': '[weight > 3]',
                    'style': {
                        'width': 20
                    }
                },
                # *= means string contains...
                {
                    'selector': '[label *= "rah"]',
                    'style': {
                        'background-color': '#000000',
                    }
                }
            ]
        )
    ], className='six columns'),

], className='row')


@app.callback(Output('org-chart', 'layout'),
              Input('dpdn', 'value'))
def update_layout(layout_value):
    if layout_value == 'breadthfirst':
        return {
        'name': layout_value,
        'roots': '[id = "ed"]',
        'animate': True
        }
    else:
        return {
            'name': layout_value,
            'animate': True
        }



if __name__ == '__main__':
    app.run_server(debug=True, port=4000)

    
# https://youtu.be/iuHFwHgQIwg
    
