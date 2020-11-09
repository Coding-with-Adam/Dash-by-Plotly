import dash  # Dash 1.16 or higher
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
# need to pip install statsmodels for trendline='ols' in scatter plot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Data from U.S. Congress, Joint Economic Committee, Social Capital Project. https://www.jec.senate.gov/public/index.cfm/republicans/2018/4/the-geography-of-social-capital-in-america
df = pd.read_csv("social-capital-project.csv")

app.layout = html.Div([
    html.Label("State:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='states-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(df.State.unique())],
        value='Alaska',
        clearable=False
    ),

    html.Label("Counties:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id='counties-dpdn', options=[], multi=True),

    dcc.Graph(id='display-map', figure={})
])


# Populate the options of counties dropdown based on states dropdown
@app.callback(
    Output('counties-dpdn', 'options'),
    Input('states-dpdn', 'value')
)
def set_cities_options(chosen_state):
    dff = df[df.State==chosen_state]
    return [{'label': c, 'value': c} for c in sorted(dff.County.unique())]


# populate initial values of counties dropdown
@app.callback(
    Output('counties-dpdn', 'value'),
    Input('counties-dpdn', 'options')
)
def set_cities_value(available_options):
    return [x['value'] for x in available_options]


@app.callback(
    Output('display-map', 'figure'),
    Input('counties-dpdn', 'value'),
    Input('states-dpdn', 'value')
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
                         hover_data={'bubble_size':False},
                         labels={'% adults graduated high school':'% graduated high school',
                                 '% without health insurance':'% no health insurance',
                                 '% in fair or poor health':'% poor health'}
                         )
        return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
