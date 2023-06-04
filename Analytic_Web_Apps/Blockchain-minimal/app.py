from dash import Dash, html, dcc, Input, Output, callback  # pip install dash
import dash_bootstrap_components as dbc                    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                                        # pip install pandas
from urllib.request import Request, urlopen
from dotenv import dotenv_values                           # pip install python-dotenv
import json


# get eth-to-usd dataset
df_eth_usd = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/Blockchain-minimal/Gemini_ETHUSD_d.csv")
df_eth_usd['date'] = pd.to_datetime(df_eth_usd['date'])

# get eth-addresses dataset
df_eth_addr = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/Blockchain-minimal/DailyActiveEthAddress.csv")
df_eth_addr['date'] = pd.to_datetime(df_eth_addr['date'])

# set up beaconchain api key for data on gas prices
config = dotenv_values(".env")
api_key = config['API_KEY']
# your .env file should have this line: API_KEY = "your-beaconchain-api-key"

# function to build one card for each gas price category
def make_card(key, get_data):
    return dbc.Card(
        [
            dbc.CardHeader(html.H2(key)),
            dbc.CardBody([
                html.H3(
                    f"{int(get_data[key] / 1000000000)} GWei",
                    id=key),
            ])
        ], className="text-center shadow")


# display app components on page
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Live Gas Prices", style={'textAlign': 'center'}),
    dbc.Row(children=[], id='gas-data-display',className="my-4"),
    dbc.Row([
        dbc.Col([
            html.H3("Eth Value"),
            dcc.Dropdown(options=df_eth_usd.columns[3:], value='open', clearable=False, id='col_price'),
            dcc.Graph(figure={}, id='eth_usd_graph')
        ], width=6),
        dbc.Col([
            html.H3("Active Ethereum Addresses"),
            dcc.Dropdown(options=df_eth_addr.columns[1:], value='Unique Address Total Count', clearable=False, id='col_addr'),
            dcc.Graph(figure={}, id='eth_addr_graph')
        ], width=6)
    ]),
    dcc.Interval(id='update_trigger', interval=1000*4) # trigger every 4 seconds
])

# build the graphs based on dropdown value selected
@callback(
    Output(component_id='eth_usd_graph', component_property='figure'),
    Output('eth_addr_graph', component_property='figure'),
    Input('col_price', component_property='value'),
    Input('col_addr', component_property='value')
)
def udpate_graph(col_p_selected, col_a_selected):
    price_fig = px.line(data_frame=df_eth_usd, x='date', y=col_p_selected)
    addr_fig = px.line(data_frame=df_eth_addr, x='date', y=col_a_selected)
    return price_fig, addr_fig


# interval component triggers the callback to pull the current gas prices
@callback(
    Output('gas-data-display','children'),
    Input('update_trigger','n_intervals')
)
def udpate_gas_price(_):
    gas_price = {"code":200,"data":{"rapid":31701870016,"fast":24753659720,"standard":24753659720,"slow":24753659720}}

    # req = Request(
    #     url=f'https://beaconcha.in/api/v1/execution/gasnow?apikey={api_key}',
    #     headers={'User-Agent': 'Mozilla/5.0'}
    # )
    # web_byte = urlopen(req).read()
    # gas_price_string = web_byte.decode('utf-8')
    # gas_price = json.loads(gas_price_string)  # convert string to dict
    # gas_price["data"].pop("timestamp")
    # gas_price["data"].pop("priceUSD")
    # print(gas_price)
    
    gas_cards = [dbc.Col(make_card(y, gas_price["data"])) for y in gas_price["data"]]
    return gas_cards


if __name__ == '__main__':
    app.run(debug=True)
