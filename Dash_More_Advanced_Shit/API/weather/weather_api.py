import pandas as pd     #(version 1.0.0)

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__)

#-------------------------------------------------------------------------------
categories=["observation_time","temperature","wind_speed","precip","humidity",
            "cloudcover","feelslike","uv_index","visibility"]

def update_weather():
    weather_requests = requests.get(
        "http://api.weatherstack.com/current?access_key=88ffb416536794b25ea52f6e9a6c6c28&query=New%20York"
    )
    json_data = weather_requests.json()
    df = pd.DataFrame(json_data)
    print (df.columns)
    print (df[:20])
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
            for name,data in zip(categories,df['current'][categories])
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
