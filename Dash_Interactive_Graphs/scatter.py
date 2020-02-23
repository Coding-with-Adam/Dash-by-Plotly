import pandas as pd     #(version 0.24.2)

import dash             #(version 1.0.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly          #(version 4.4.1)
import plotly.express as px

df = pd.read_csv("suicide_rates.csv")

mark_values = {1985:'1985',1988:'1988',1991:'1991',1994:'1994',
               1997:'1997',2000:'2000',2003:'2003',2006:'2006',
               2009:'2009',2012:'2012',2015:'2015',2016:'2016'}

app = dash.Dash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([
        html.Div([
            html.Pre(children= "Suicide Rates 1985-2016",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),

        html.Div([
            dcc.Graph(id='the_graph')
        ]),

        html.Div([
            dcc.RangeSlider(id='the_year',
                min=1985,
                max=2016,
                value=[1985,1988],
                marks=mark_values,
                step=None)
        ],style={"width": "70%", "position":"absolute",
                 "left":"5%"})

])
#---------------------------------------------------------------
@app.callback(
    Output('the_graph','figure'),
    [Input('the_year','value')]
)

def update_graph(years_chosen):
    # print(years_chosen)

    dff=df[(df['year']>=years_chosen[0])&(df['year']<=years_chosen[1])]
    # filter df rows where column year values are >=1985 AND <=1988
    dff=dff.groupby(["country"], as_index=False)["suicides/100k pop",
                    "gdp_per_capita ($)"].mean()
    # print (dff[:3])

    scatterplot = px.scatter(
        data_frame=dff,
        x="suicides/100k pop",
        y="gdp_per_capita ($)",
        hover_data=['country'],
        text="country",
        height=550
    )

    scatterplot.update_traces(textposition='top center')

    return (scatterplot)

if __name__ == '__main__':
    app.run_server(debug=True)
