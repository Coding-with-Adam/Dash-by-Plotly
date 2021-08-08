import dash
import dash_bootstrap_components as dbc
import twitter

api = twitter.Api(consumer_key='dA7IdoRKgaACPuZu8hJb9qo0K',
                      consumer_secret='8dz7XjbUUylgw7Da5Zs2YoYBQSLVObvz0jG25uVRmioleqioA4',
                      access_token_key='3296439504-ft6rRDSdVOhUBNFnUOZlWOG4wFgxO41n8Z6l0Fj',
                      access_token_secret='gOcOD0XwEwxLHVtbV089n8DVOtrnRGR5EAzlv6quP2Xjc')
# ensure you connected correctly
# print(api.VerifyCredentials())
# exit()

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )