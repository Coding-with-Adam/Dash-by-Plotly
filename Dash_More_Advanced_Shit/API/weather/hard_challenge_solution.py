# Solution to change your app to show yesterday’s forecast of "mintemp" & “avgtemp” in New York
# Changes made to lines 15,19,37

import pandas as pd     #(version 1.0.0)

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__)

#-------------------------------------------------------------------------------
categories=["mintemp","avgtemp"]

def update_weather():
    weather_requests = requests.get(
        "http://api.weatherstack.com/forecast?access_key=88ffb416536794b25ea52f6e9a6c6c28&query=New%20York"
    )
    json_data = weather_requests.json()
    df = pd.DataFrame(json_data)

    return([
            html.Table(
                className='table-weather',
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    name+": "+str(data)
                                ]
                            )
                        ]
                    )
            for name,data in zip(categories,map(df['forecast']['2020-04-17'].get, categories)) #make sure to change date
        ])
    ])

#-------------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Interval(
                id='my_interval',
                disabled=False,     #if True the counter will no longer update
                n_intervals=0,      #number of times the interval has passed
                interval=300*1000,  #increment the counter n_intervals every 5 minutes
                max_intervals=100,  #number of times the interval will be fired.
                                    #if -1, then the interval has no limit (the default)
                                    #and if 0 then the interval stops running.
    ),

    html.Div([
        html.Div(id="weather", children=update_weather()
        )
    ]),

])

#-------------------------------------------------------------------------------
# Callback to update news
@app.callback(Output("weather", "children"), [Input("my_interval", "n_intervals")])
def update_weather_div(n):
    return update_weather()

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
