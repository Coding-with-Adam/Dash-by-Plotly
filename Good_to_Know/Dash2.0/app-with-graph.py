# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px

# incorporate data into app
df = px.data.medals_long()

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
mytitle = dcc.Markdown(children='# App that analyzes Olympic medals')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot'],
                        value='Bar Plot',  # initial value displayed when page first loads
                        clearable=False)

# Customize your own Layout
app.layout = dbc.Container([mytitle, mygraph, dropdown])

# Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    if user_input == 'Bar Plot':
        fig = px.bar(data_frame=df, x="nation", y="count", color="medal")

    elif user_input == 'Scatter Plot':
        fig = px.scatter(data_frame=df, x="count", y="nation", color="medal",
                         symbol="medal")

    return fig  # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(port=8053)
