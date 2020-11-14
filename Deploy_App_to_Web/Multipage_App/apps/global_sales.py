import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# owner: shivp Kaggle. Source: https://data.mendeley.com/datasets
# dataset was modified. Original data: https://www.kaggle.com/shivkp/customer-behaviour
dfg = pd.read_csv(DATA_PATH.joinpath("opsales.csv"))

layout = html.Div([
    html.H1('General Product Sales', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Payment type", style={"fontSize":"150%"}),
            dcc.Dropdown(
                id='pymnt-dropdown', value='DEBIT', clearable=False,
                persistence=True, persistence_type='session',
                options=[{'label': x, 'value': x} for x in sorted(dfg["Type"].unique())]
            )
        ], className='six columns'),

        html.Div([
            html.Pre(children="Country of destination", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='country-dropdown', value='India', clearable=False,
                persistence=True, persistence_type='local',
                options=[{'label': x, 'value': x} for x in sorted(dfg["Order Country"].unique())]
            )
            ], className='six columns'),
    ], className='row'),

    dcc.Graph(id='my-map', figure={}),
])


@app.callback(
    Output(component_id='my-map', component_property='figure'),
    [Input(component_id='pymnt-dropdown', component_property='value'),
     Input(component_id='country-dropdown', component_property='value')]
)
def display_value(pymnt_chosen, country_chosen):
    dfg_fltrd = dfg[(dfg['Order Country'] == country_chosen) &
                    (dfg["Type"] == pymnt_chosen)]
    dfg_fltrd = dfg_fltrd.groupby(["Customer State"])[['Sales']].sum()
    dfg_fltrd.reset_index(inplace=True)
    fig = px.choropleth(dfg_fltrd, locations="Customer State",
                        locationmode="USA-states", color="Sales",
                        scope="usa")
    return fig

