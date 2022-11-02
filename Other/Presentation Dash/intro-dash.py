from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# my_output = dcc.Markdown(children='')
app.layout = dbc.Container([                # Customize the style and layout of the page--------------------------------
    my_text := dcc.Input(value='Type Text new now'),
    my_output := dcc.Markdown(children=''),
    # dcc.Dropdown(options=['NYC', 'MTL', 'SF'], value='NYC', id='my-dropdown'),
])

@app.callback(                              # Callback to build powerful interactions-----------------------------------
    Output(component_id=my_output, component_property='children'),
    Input(component_id=my_text, component_property='value'),
)
def update_text(el_texto):
    # slice the data set
    # build the graph
    return el_texto


if __name__ == '__main__':
    app.run_server(debug=True)