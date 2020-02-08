# Environment: dash1_8_0_env
import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px
import plotly.io as pio

import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# df = px.data.gapminder()
# fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
#            size="pop", color="continent", hover_name="country",
#            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

# print (fig)
# pio.show(fig)

# df = px.data.gapminder()
# dff= df.groupby(['country','year'], as_index=False)['lifeExp'].mean().sort_values(by=['year'])
#
# print (dff[:50])



app = dash.Dash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=2007, max=2007, min=1952, required=True, step=5),
        html.Button(id='submit_button', n_clicks=0, children='Submit',autoFocus=True),
        html.Div(id='output_state'),
    ]),

])

#---------------------------------------------------------------
@app.callback(
    [Output('output_state', 'children'),
    Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')]
)

def update_output(num_clicks, val_selected):
    # df = px.data.gapminder().query("year=={}".format(val_selected))

    df = px.data.gapminder()
    dff= df.groupby(['country','year','iso_alpha'], as_index=False)['lifeExp'].mean().sort_values(by=['year'])
    print(dff[:10])

    fig = px.choropleth(dff, locations="iso_alpha", animation_frame="year",
                        color="lifeExp", # lifeExp is a column of gapminder
                        hover_name="country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)

    return ('The input value was "{}" and the button has been clicked {} times'.format(val_selected, num_clicks), fig)

if __name__ == '__main__':
    app.run_server(debug=True)
