# Environment: dash1_8_0_env
import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px
import plotly.io as pio

import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

the_years = ["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"]

df = pd.read_csv("Gender_StatsData.csv")
df = df.loc[:26219]
df = df[(df["Indicator Name"]=="Lower secondary completion rate, female (% of relevant age group)")|\
        (df["Indicator Name"]=="Lower secondary completion rate, male (% of relevant age group)")]
df = df.groupby(["Country Name","Country Code","Indicator Name"], as_index=False)[the_years].mean()

countries=["Arab World","South Asia","Middle East & North Africa","Latin America & Caribbean","East Asia & Pacific","European Union"]
df = df[df['Country Name'].isin(countries)]
# print(df[:20])
df = pd.melt(df,id_vars=['Country Name','Country Code','Indicator Name'],var_name='Year',value_name='Rate')
# print(df[:20])
# print(df['Country Name'].unique())




fig = px.scatter(df, x="Rate", y="Country Name", color="Indicator Name", animation_frame="Year",
                 range_x=[40,90], range_y=[-0.5,5.5],
                 title="Gender Inequality in Lower Secondary Schools",
                 labels={"2000":"Lower secondary completion rate (%)", "Indicator Name":"Gender"} # customize axis label
      )

fig.data[0].name = 'Female'
fig.data[1].name = 'Male'
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 600
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 400

# print(fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'])
pio.show(fig)

# fig = px.scatter(df, x="2000", y="lifeExp", animation_frame="year", animation_group="country",
#            size="pop", color="continent", hover_name="country",
#            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

# print (fig)
# pio.show(fig)

# df = px.data.gapminder()
# dff= df.groupby(['country','year'], as_index=False)['lifeExp'].mean().sort_values(by=['year'])
#
# print (dff[:50])



# app = dash.Dash(__name__)

#---------------------------------------------------------------
# app.layout = html.Div([
#
#     html.Div([
#         dcc.Graph(id='the_graph')
#     ]),
#
#     html.Div([
#         dcc.Input(id='input_state', type='number', inputMode='numeric', value=2007, max=2007, min=1952, required=True, step=5),
#         html.Button(id='submit_button', n_clicks=0, children='Submit',autoFocus=True),
#         html.Div(id='output_state'),
#     ]),
#
# ])
#
# #---------------------------------------------------------------
# @app.callback(
#     [Output('output_state', 'children'),
#     Output(component_id='the_graph', component_property='figure')],
#     [Input(component_id='submit_button', component_property='n_clicks')],
#     [State(component_id='input_state', component_property='value')]
# )
#
# def update_output(num_clicks, val_selected):
#     # df = px.data.gapminder().query("year=={}".format(val_selected))
#
#     df = px.data.gapminder()
#     dff= df.groupby(['country','year','iso_alpha'], as_index=False)['lifeExp'].mean().sort_values(by=['year'])
#     print(dff[:10])
#
#     fig = px.choropleth(dff, locations="iso_alpha", animation_frame="year",
#                         color="lifeExp", # lifeExp is a column of gapminder
#                         hover_name="country", # column to add to hover information
#                         color_continuous_scale=px.colors.sequential.Plasma)
#
#     return ('The input value was "{}" and the button has been clicked {} times'.format(val_selected, num_clicks), fig)
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
