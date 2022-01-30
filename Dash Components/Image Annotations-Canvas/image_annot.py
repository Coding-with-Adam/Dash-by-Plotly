from dash import Dash, html, dcc, Output, Input, callback   # pip install dash
import dash_bootstrap_components as dbc                     # dash-bootstrap-components
from dash_canvas import DashCanvas                          # pip install dash-canvas
import dash_daq as daq                                      # pip install dash-daq
import plotly.express as px
import pandas as pd                                         # pip install pandas
from skimage import data  # pip install scikit-image and pip install pooch for access to demo data

btns = [
    "drawline",
    "drawopenpath",
    "drawclosedpath",
    "drawcircle",
    "drawrect",
    "eraseshape",
]

# Build image
img = data.skin()
fig_img = px.imshow(img).update_layout(dragmode="drawclosedpath")
# more dragmode option -- https://plotly.com/python/reference/layout/#layout-dragmode

# Build line chart
# https://healthdata.nj.gov/dataset/Late-Stage-Female-Breast-Cancer-Incidence-Rate-cas/3hep-nd78
df = pd.read_csv("Late-Stage_Female_Breast_Cancer_Incidence_Rate__cases_per_100_000_females.csv")
fig_scatter = px.scatter(data_frame=df, x='Year', y='Rate (per 100,000 females)', color='Race')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Late-Stage Female Breast Cancer", style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_scatter, config={"modeBarButtonsToAdd": btns})
        ], width=8),
        dbc.Col([
            html.H2('Take Notes:'),
            DashCanvas(id='my-canvas',
                       tool='pencil',
                       lineWidth=3,
                       lineColor=None
            )
        ], width=4, className='mt-5')
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_img, config={"modeBarButtonsToAdd": btns})
        ], width=6),
        dbc.Col([
            daq.ColorPicker(
                id='color-picker',
                label='Brush color',
                value=dict(hex='#119DFF')
            )], width=4, className='mt-5')
    ])
], fluid=True)


@callback(
    Output(component_id='my-canvas', component_property='lineColor'),
    Input(component_id='color-picker', component_property='value')
)
def update_canvas_linecolor(value):
    if isinstance(value, dict):
        return value['hex']
    else:
        return value


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
