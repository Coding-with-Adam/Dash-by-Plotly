# Code belongs to yazid - https://github.com/leberber
from dash import  Dash, dcc, html, Input, Output, clientside_callback, ClientsideFunction
import dash_mantine_components as dmc
from data import tradeData


app = Dash(__name__, external_scripts=['https://cdn.jsdelivr.net/npm/apexcharts'])
app.layout = html.Div(
    children=[
        dcc.Store(id='ApexchartsSampleData', data=tradeData),
        html.H1("Javascript Charts inside a Dash App"),
        dmc.Center(
            dmc.Paper(
                shadow="sm",
                style={'height':'600px', 'width':'800px', 'marginTop':'100px'},
                children=[
                    html.Div(id='apexAreaChart'),
                    dmc.Center(
                        children=[
                            dmc.SegmentedControl(
                                id="selectCountryChip",
                                value="Canada",
                                data=['Canada', 'USA', 'Australia'],
                            )
                        ]
                    )
                ]
            )
        )
    ]
)


clientside_callback(
    ClientsideFunction(
        namespace='apexCharts',
        function_name='areaChart'
    ),
    Output("apexAreaChart", "children"),
    Input("ApexchartsSampleData", "data"),
    Input("selectCountryChip", "value"),
)


if __name__ == "__main__":
    app.run_server(debug=True)
