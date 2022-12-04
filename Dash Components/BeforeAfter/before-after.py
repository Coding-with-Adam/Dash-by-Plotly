# Video:    [Before After Image Slider - Dash Component](https://youtu.be/-0bqU94KGMw)
from dash import Dash, html                                     # pip install dash
from dash_extensions import BeforeAfter  # pip install dash-extensions==0.0.47 or higher
import dash_bootstrap_components as dbc  # dash-bootstrap-components

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col([
            html.H1("Before-After Dash Component", style={'textAlign':'center'})
        ], width=12)
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            # https://nypost.com/2020/08/05/before-and-after-satellite-images-of-the-beirut-explosion/
            html.H2("Satellite Imagery"),
            BeforeAfter(before="assets/beirut1.jpg", after="assets/beirut2.jpg", width=512, height=412, defaultProgress=0.5),
        ], width=6),
        dbc.Col([
            # https://sustainableearth.blog/2019/05/06/changes-in-marine-habitats/
            html.H2("Conservation"),
            BeforeAfter(before="assets/reef1.jpg", after="assets/reef2.jpg", width=512, height=412),
        ], width=6)

    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            # https://www.sciencetimes.com/articles/29510/20210205/mbl-researchers-imaged-first-body-plan-moments-embryo.htm
            html.H2("Marine Biology"),
            BeforeAfter(before="assets/ciona-egg1.png", after="assets/ciona-egg2.png", width=512, height=412),
        ], width=6),
        dbc.Col([
            # https://pressbooks-dev.oer.hawaii.edu/chemistry/chapter/writing-and-balancing-chemical-equations/
            html.H2("Chemistry"),
            BeforeAfter(before="assets/chemistry1.jpg",after="assets/chemistry2.jpg", width=512, height=412),
        ], width=6)
    ],className='mb-5'),
])



if __name__ == '__main__':
    app.run_server(debug=True, port=8002)
