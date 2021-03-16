import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Callbacks/Client-side-callback/opsales.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(
        id='clientside-graph'
    ),
    dcc.Store(
        id='clientside-store-figure', data={}
    ),
    dcc.Dropdown(
        id='shipping-type',
        options=[
            {'label': x, 'value': x} for x in df['Shipping Mode'].unique()
        ],
        value='Second Class'
    ),
    dcc.Input(
        id='clientside-graph-title',
        value='Placeholder Title'
    ),
])


# Serverside callback
@app.callback(
    Output('clientside-graph', 'figure'),
    Input('shipping-type', 'value'),
    Input('clientside-graph-title','value')
)
def update_store_data(shipping, text):
    dff = df[df['Shipping Mode'] == shipping]
    fig = px.histogram(dff, x="Customer Segment", y="Sales",
                 color='Department Name', title=text)
    return fig




# Serverside callback
# @app.callback(
#     Output('clientside-store-figure', 'data'),
#     Input('shipping-type', 'value'),
# )
# def update_store_data(shipping):
#     dff = df[df['Shipping Mode'] == shipping]
#     stored_figure = px.histogram(dff, x="Customer Segment", y="Sales", color='Department Name')
#     # store hostogram on client side - browser
#     return stored_figure
#
# # Clientside callback
# app.clientside_callback(
#     """
#     function(figure_data, title_text) {
#         if(figure_data === undefined) {
#             return {'data': [], 'layout': {}};
#         }
#         const fig = Object.assign({}, figure_data, {
#                 'layout': {
#                     ...figure_data.layout,
#                     'title': {
#                         ...figure_data.layout.title, text: title_text
#                     }
#                 }
#         });
#         return fig;
#     }
#     """,
#     Output('clientside-graph', 'figure'),
#     Input('clientside-store-figure', 'data'),
#     Input('clientside-graph-title','value')
# )


if __name__ == '__main__':
    app.run_server(debug=True, port=1286)

    
# https://youtu.be/wHUzUHTPfo0
