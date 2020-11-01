import dash
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input


df = pd.read_csv("vgsales.csv")

app = dash.Dash(__name__)

app.layout=html.Div([
    html.H1("Graph Analysis with Charming Data"),
    dcc.Dropdown(id='genre-choice',
                 options=[{'label':x, 'value':x}
                          for x in sorted(df.Genre.unique())],
                 value='Action',
                 style={'width':'50%'}
                 ),
    dcc.Dropdown(id='platform-choice',
                 options=[{'label': x, 'value': x}
                          for x in sorted(df.Platform.unique())],
                 value='PS4',
                 style={'width':'50%'}
                 ),
    dcc.Graph(id='my-graph',
              figure={}),
])
@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='genre-choice', component_property='value'),
    Input(component_id='platform-choice', component_property='value')
)
def interactive_graphs(value_genre, value_platform):
    dff = df[df.Genre==value_genre]
    dff = dff[dff.Platform==value_platform]
    fig = px.bar(data_frame=dff, x='Year', y='Japan Sales')
    return fig


if __name__=='__main__':
    app.run_server()


