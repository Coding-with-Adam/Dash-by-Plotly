import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__,
                   path='/heatmap',
                   name='Heatmap',
                   title='New heatmaps',
                   image='pg3.png',
                   description='Learn all about the heatmap.'
)

layout = html.Div(
    [
        dcc.Markdown('## This is the newest heatmap design', style={'textAlign':'center'}),
        dcc.Graph(figure= px.imshow([[1, 20, 30],
                                     [20, 1, 60],
                                     [30, 60, 1]]))
    ]
)
