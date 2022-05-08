# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
mytext = dcc.Markdown(children='')
myinput = dbc.Input(value="# Hello World - let's build web apps in Python!")

# Customize your own Layout
app.layout = dbc.Container([mytext, myinput])

# Callback allows components to interact
@app.callback(
    Output(mytext, component_property='children'),
    Input(myinput, component_property='value')
)
def update_title(user_input):  # function arguments come from the component property of the Input
    return user_input  # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(port=8052)
