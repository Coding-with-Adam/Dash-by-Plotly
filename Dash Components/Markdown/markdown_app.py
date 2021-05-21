import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    html.Div([
        html.H2("Text with Markdown"),
        dcc.Textarea(id="message", placeholder="Test your Markdown",
                     style={'width': '100%', 'height': 300}),
    ],className="four columns"),

    html.Div([
        html.Hr(style={"width":4, "height":700, "border": "6px solid black"})
    ],className="one columns"),

    html.Div([
        html.H2("Result"),
        dcc.Markdown(id="markdown-result")
    ],className="seven columns"),

])

@app.callback(
    Output("markdown-result", "children"),
    Input("message","value")
)
def text_update(value):
    return value


if __name__ == '__main__':
    app.run_server(debug=True)