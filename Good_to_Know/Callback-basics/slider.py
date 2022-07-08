from dash import Dash, dcc, html, Output, Input, State, callback
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    dcc.Slider(10,20, step=1, value=12, id='my-slider'),
    dcc.Markdown(children='This is the Title of the App', id='text-displayed', style={'fontSize':10})
])

@callback(
    Output(component_id='text-displayed', component_property='style'),
    Input(component_id='my-slider', component_property='value')
)
def update_text(user_selected):  # the function argument comes from the component property of the Input
    print(user_selected)
    print(type(user_selected))
    return {'fontSize' : user_selected}  # the returned object is assigned to the component property of the Output

if __name__=='__main__':
    app.run(port=8002)