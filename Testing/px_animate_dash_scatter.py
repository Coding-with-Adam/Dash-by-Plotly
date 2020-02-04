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
step_num=2016

app = dash.Dash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([
        html.Div([
            html.Pre(children= "Suicide Rates 1985-2016",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),

        dcc.Interval(id='auto-stepper',
                     interval=1*1000, # in milliseconds
                     n_intervals=0,
                     max_intervals=7 
        ),

        html.Div([
            dcc.Graph(id='the_graph')
        ]),

        html.Div([
            dcc.Slider(id='the_year',
                min=1985,
                max=step_num,
                value=1985,
                marks=mark_values,
                included=False)
        ],style={"width": "70%", "position":"absolute",
                 "left":"5%"})

])
#---------------------------------------------------------------

@app.callback(
    [Output('the_year', 'value'),
    Output('the_graph','figure')],
    [Input('auto-stepper', 'n_intervals')])

def on_click(n_intervals):
    if n_intervals == 0:

        dff=df[df['year']==n_intervals+1985]
        dff=dff.groupby(["country"], as_index=False)["suicides/100k pop",
                        "gdp_per_capita ($)"].mean()

        scatterplot = px.scatter(
            data_frame=dff,
            x="suicides/100k pop",
            y="gdp_per_capita ($)",
            hover_data=['country'],
            text="country",
            range_x=[0,60],
            range_y=[0,50000],
            height=550,
            title=n_intervals+1985
        )

        scatterplot.update_traces(textposition='top center')
        scatterplot.update_layout(transition=dict(duration=500, easing='cubic-in-out'))

        return (1985,scatterplot)

    else:
        dff=df[df['year']==n_intervals+1985]
        dff=dff.groupby(["country"], as_index=False)["suicides/100k pop",
                        "gdp_per_capita ($)"].mean()

        scatterplot = px.scatter(
            data_frame=dff,
            x="suicides/100k pop",
            y="gdp_per_capita ($)",
            hover_data=['country'],
            text="country",
            range_x=[0,60],
            range_y=[0,50000],
            height=550,
            title=n_intervals+1985
        )

        scatterplot.update_traces(textposition='top center')
        scatterplot.update_layout(transition=dict(duration=250, easing='cubic-in-out'))

        return (((n_intervals+1985)%step_num), scatterplot)

if __name__ == '__main__':
    app.run_server(debug=True)
