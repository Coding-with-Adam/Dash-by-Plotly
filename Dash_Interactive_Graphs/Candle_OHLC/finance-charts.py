from dash import Dash, html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Dash_Interactive_Graphs/Candle_OHLC/oil_prices.csv')
df.Date = pd.to_datetime(df.Date)

app.layout = dbc.Container([
    html.H1('Candlestick vs OHLC Charts', style={'textAlign': 'center'}),

    dbc.Row([
        dbc.Col([html.Label('Volume of oil over:'),
                 dcc.Input(id='oil-volume', type='number', min=80000,
                           max=700000, step=10000, value=80000)
        ], width=4),
    ]),

    dbc.Row([
        dbc.Col([html.Label('CandleStick Chart')], width=dict(size=4, offset=2)),
        dbc.Col([html.Label('OHLC Chart')], width=dict(size=4, offset=2))
    ]),

    dbc.Row([
        dbc.Col([dcc.Graph(id='candle', figure={}, style={'height': '80vh'})], width=6),
        dbc.Col([dcc.Graph(id='ohlc', figure={}, style={'height': '80vh'})], width=6)
    ]),
], fluid=True)


@callback(
    Output(component_id='candle', component_property='figure'),
    Output(component_id='ohlc', component_property='figure'),
    Input(component_id='oil-volume', component_property='value')
)
def build_graphs(chosen_volume):  # represents that which is assigned to the component property of the Input
    dff = df[df.Volume > chosen_volume]
    print(dff.head())

    fig_candle = go.Figure(
        go.Candlestick(x=dff['Date'],
                       open=dff['Open'],
                       high=dff['High'],
                       low=dff['Low'],
                       close=dff['Close'],
                       text=dff['Volume'])
    )
    fig_candle.update_layout(margin=dict(t=30, b=30))  # xaxis_rangeslider_visible=False,

    fig_ohlc = go.Figure(
        go.Ohlc(x=dff['Date'],
                open=dff['Open'],
                high=dff['High'],
                low=dff['Low'],
                close=dff['Close'],
                text=dff['Volume'])
    )
    fig_ohlc.update_layout(margin=dict(t=30, b=30))
    
    return fig_candle, fig_ohlc


if __name__=='__main__':
    app.run_server()