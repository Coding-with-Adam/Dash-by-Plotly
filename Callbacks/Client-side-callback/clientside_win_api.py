import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Callbacks/Client-side-callback/opsales.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Button('Print Graphs', id='printing'),
    html.Div(id='hidden-content'),
    html.H1('Analysis of Store Sales', style={'textAlign':'center'}),
    dcc.Graph(id='one', figure=px.pie(df, names="Shipping Mode", values="Sales").update_traces(textinfo='label+percent', showlegend=False)),
    dcc.Graph(id='two', figure=px.histogram(df, x="Order Status", y="Sales")),
    dcc.Graph(id='thr', figure=px.pie(df, names="Customer Segment", values="Sales").update_traces(textinfo='label+percent', showlegend=False)),
])

app.clientside_callback(
    """
    function(clicks) {
        if (clicks > 0) {
          window.print()
        }
        return ""
    }
    """,
    Output('hidden-content', 'children'),
    Input('printing', 'n_clicks')
)

# app.clientside_callback(
#     """
#     function(clicks) {
#         if (clicks > 0) {
#         var myWindow = window.open("", "", "width=200,height=100");
#         myWindow.document.write("<p>A new window!</p>");
#         myWindow.focus();
#         }
#         return ""
#     }
#     """,
#     Output('hidden-content', 'children'),
#     Input('printing', 'n_clicks')
# )

if __name__ == '__main__':
    app.run_server(debug=True)

    
    
# https://youtu.be/wHUzUHTPfo0
