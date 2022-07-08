from dash import Dash, dcc, html, Output, Input, State, callback
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    dcc.RadioItems(options=['car','house','ship'], value='ship', id='my-radio-btn'),
    dcc.Markdown(children='', id='text-displayed')
])

@callback(
    Output(component_id='text-displayed', component_property='children'),
    Input(component_id='my-radio-btn', component_property='value')
)
def update_text(user_selected):  # the function argument comes from the component property of the Input
    print(user_selected)
    print(type(user_selected))
    return f"The Radio Button value you chose was: {user_selected}"  # the returned object is assigned to the component property of the Output

if __name__=='__main__':
    app.run(port=8001)
