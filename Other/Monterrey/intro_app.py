from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# my_output = dcc.Markdown()
app.layout = dbc.Container([                # Build Layout to customize the style and display of the page---------------
    my_output := dcc.Markdown(children=''),
    my_text := dcc.Input(value='Type Text')
])

@app.callback(                              # Callback to build powerful interactions-----------------------------------
    Output(my_output, 'children'),
    Input(my_text, 'value')
)
def update_graph(el_texto):
    return el_texto


if __name__ == '__main__':
    app.run_server(debug=True)
