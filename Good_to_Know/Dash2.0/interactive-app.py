from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc

# Customize your own Layout
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
mytext =  dcc.Markdown(children='')
myinput = dbc.Input(value="# Hello World - let's build web apps in Python!")

app.layout = dbc.Container([mytext, myinput])

# Callback allows components to interact
@app.callback(
    Output(mytext, component_property='children'),
    Input(myinput, component_property='value')
)
def update_graph(user_input):
    return user_input

# Run app
if __name__=='__main__':
    app.run_server(port=8052)