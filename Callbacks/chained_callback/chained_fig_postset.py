import dash  # Dash 1.16 or higher
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
# need to pip install statsmodels for trendline='ols' in scatter plot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Data from U.S. Congress, Joint Economic Committee, Social Capital Project. https://www.jec.senate.gov/public/index.cfm/republicans/2018/4/the-geography-of-social-capital-in-america
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Callbacks/chained_callback/social-capital-project.csv")

app.layout = html.Div([
    html.Label("State:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='states-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(df.State.unique())],
        value=None,
        clearable=False
    ),
    html.Label("Counties:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id='counties-dpdn',
                 options=[],
                 value=[],
                 multi=True),
    html.Div(id='graph-container', children=[])
])


# Populate the counties dropdown with options and values
@app.callback(
    Output('counties-dpdn', 'options'),
    Output('counties-dpdn', 'value'),
    Input('states-dpdn', 'value'),
)
def set_cities_options(chosen_state):
    dff = df[df.State==chosen_state]
    counties_of_states = [{'label': c, 'value': c} for c in sorted(dff.County.unique())]
    values_selected = [x['value'] for x in counties_of_states]
    return counties_of_states, values_selected


# Create graph component and populate with scatter plot
@app.callback(
    Output('graph-container', 'children'),
    Input('counties-dpdn', 'value'),
    Input('states-dpdn', 'value'),
    prevent_initial_call=True
)
def update_grpah(selected_counties, selected_state):
    if len(selected_counties) == 0:
        return dash.no_update
    else:
        dff = df[(df.State==selected_state) & (df.County.isin(selected_counties))]

        fig = px.scatter(dff, x='% without health insurance', y='% in fair or poor health',
                         color='% adults graduated high school',
                         trendline='ols',
                         size='bubble_size',
                         hover_name='County',
                         # hover_data={'bubble_size':False},
                         labels={'% adults graduated high school':'% graduated high school',
                                 '% without health insurance':'% no health insurance',
                                 '% in fair or poor health':'% poor health'}
                         )
        return dcc.Graph(id='display-map', figure=fig)


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

    
# https://youtu.be/ZxshFO0bbZM
