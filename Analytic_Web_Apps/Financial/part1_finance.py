import dash                                # pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries # pip install alpha-vantage


# -------------------------------------------------------------------------------
# Set up initial key and financial category

# key = '7FEDJMHY3CM2KPEC' # Use your own API Key or support my channel if you're using mine :)
# # https://github.com/RomelTorres/alpha_vantage
# # Chose your output format or default to JSON (python dict)
# ts = TimeSeries(key, output_format='pandas') # 'pandas' or 'json' or 'csv'
# ttm_data, ttm_meta_data = ts.get_intraday(symbol='TTM',interval='1min', outputsize='compact')
# df = ttm_data.iloc[:50].copy()
# df=df.transpose()
# df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
#                  "4. close":"close","5. volume":"volume"},inplace=True)
# df=df.reset_index().rename(columns={'index': 'indicator'})
# df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
# df = df[df['indicator']!='volume']


# df.to_csv("data2.csv", index=False)
# exit()


# Read the data we already downloaded from the API
dff = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/Financial/data.csv")
dff = dff[dff.indicator.isin(['high'])]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardImg(
                        src="/assets/tata.png",
                        top=True,
                        style={"width": "6rem"},
                    ),

                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.P("CHANGE (1D)")
                            ]),

                            dbc.Col([
                                dcc.Graph(id='indicator-graph', figure={},
                                          config={'displayModeBar':False})
                            ])
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='daily-line', figure={},
                                          config={'displayModeBar':False})
                            ])
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.Button("SELL"),
                            ]),

                            dbc.Col([
                                dbc.Button("BUY")
                            ])
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.Label(id='low-price', children="12.237"),
                            ]),
                            dbc.Col([
                                dbc.Label(id='high-price', children="13.418"),
                            ])
                        ])
                    ]),
                ],
                style={"width": "24rem"},
                className="mt-3"
            )
        ], width=6)
    ], justify='center'),

    dcc.Interval(id='update', n_intervals=0, interval=1000*5)
])

# Indicator Graph
@app.callback(
    Output('indicator-graph', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    dff_rv = dff.iloc[::-1]
    day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]

    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':12})
    fig.update_layout(height=30, width=70)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')

    return fig


if __name__=='__main__':
    app.run_server(debug=True, port=3000)

 # https://youtu.be/iOkMaeU8dqE
