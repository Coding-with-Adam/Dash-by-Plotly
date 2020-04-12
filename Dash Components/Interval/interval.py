import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.graph_objects as go

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

#------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Interval(
                id='my_interval',
                disabled=False,     #if True, the counter will no longer update
                interval=1*3000,    #increment the counter n_intervals every interval milliseconds
                n_intervals=0,      #number of times the interval has passed
                max_intervals=4,    #number of times the interval will be fired.
                                    #if -1, then the interval has no limit (the default)
                                    #and if 0 then the interval stops running.
    ),

    html.Div(id='output_data', style={'font-size':36}),
    dcc.Input(id="input_text",type='text'),
    dcc.Graph(id="mybarchart"),

])

#------------------------------------------------------------------------
@app.callback(
    [Output('output_data', 'children'),
     Output('mybarchart', 'figure')],
    [Input('my_interval', 'n_intervals')]
)
def update_graph(num):
    """update every 3 seconds"""
    if num==0:
        raise PreventUpdate
    else:
        y_data=num
        fig=go.Figure(data=[go.Bar(x=[1, 2, 3, 4, 5, 6, 7, 8, 9], y=[y_data]*9)],
                      layout=go.Layout(yaxis=dict(tickfont=dict(size=22)))
        )

    return (y_data,fig)

#------------------------------------------------------------------------
@app.callback(
    Output('my_interval', 'max_intervals'),
    [Input('input_text', 'value')]
)
def stop_interval(retrieved_text):
    if retrieved_text == 'stop':
        max_intervals = 0
    else:
        raise PreventUpdate

    return (max_intervals)
#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
