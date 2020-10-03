import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px

df = px.data.gapminder()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(id='dpdn2', value=['Germany','Brazil'], multi=True,
                 options=[{'label': x, 'value': x} for x in
                          df.country.unique()]),
    html.Div([
        dcc.Graph(id='pie-graph', figure={}, className='six columns'),
        dcc.Graph(id='my-graph', figure={},
                  clickData={'points': [{'curveNumber': 0, 'pointNumber': 0, 'pointIndex': 0, 'x': 1952, 'y': 2108.944355, 'customdata': ['Brazil', 'Americas', 50.917, 56602560]}]},
                  hoverData={'points': [{'curveNumber': 0, 'pointNumber': 0, 'pointIndex': 0, 'x': 1952, 'y': 2108.944355, 'customdata': ['Brazil', 'Americas', 50.917, 56602560]}]},
                  config={
                      'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize'
                      'showTips': False,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                        },
                  className='six columns'
                  )
    ])
])


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(country_chosen):
    dff = df[df.country.isin(country_chosen)]
    fig = px.line(data_frame=dff, x='year', y='gdpPercap', color='country',
                  custom_data=['country', 'continent', 'lifeExp', 'pop'])
    fig.update_traces(mode='lines+markers')
    return fig


# Dash version 1.16.0 or higher
@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_side_graph(hov_data, clk_data, slct_data, country_chosen):
    print(f'click data: {clk_data}')
    print(f'hover data: {hov_data}')
    # print(hov_data['points'][0]['customdata'][0])
    # print(slct_data)
    dff2 = df[df.country.isin(country_chosen)]
    hov_year = hov_data['points'][0]['x']
    dff2 = dff2[dff2.year == hov_year]
    fig2 = px.pie(data_frame=dff2, values='pop', names='country', title=f'Population for: {hov_year}')
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)
