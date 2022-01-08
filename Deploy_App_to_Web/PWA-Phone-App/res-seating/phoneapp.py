from dash import Dash, dcc, html, Output, Input, callback
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv('Open_Restaurant_Applications.csv')

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR, dbc_css],
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, '
                       'initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )
app.index_string = '''<!DOCTYPE html>
<html>
<head>
<title>My app title</title>
<link rel="manifest" href="./assets/manifest.json" />
{%metas%}
{%favicon%}
{%css%}
</head>
<script type="module">
   import 'https://cdn.jsdelivr.net/npm/@pwabuilder/pwaupdate';
   const el = document.createElement('pwa-update');
   document.body.appendChild(el);
</script>
<body>
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', ()=> {
      navigator
      .serviceWorker
      .register('./assets/sw01.js')
      .then(()=>console.log("Ready."))
      .catch(()=>console.log("Err..."));
    });
  }
</script>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''

server = app.server
load_figure_template('vapor')

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(src='/assets/mylogo.png', style={'width': '5.5vw','margin-top': '5%', 'border-radius': '50%',
                            'max-width':'100%', 'height':'auto'})
        ]),
        dbc.Col([
            html.H1('Open Seating Restaurant Tracker', style={'textAlign': 'center'}),
        ], width=11)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label('Approved for Sidewalk Seating:', className='mt-5'),
            dcc.RadioItems(id='sidewalk-seating',
                           options=[{'label': 'yes', 'value': 'yes'},
                                    {'label': 'no', 'value': 'no'}],
                           value='yes', inputClassName="mx-1"
                          ),
            html.Label('Approved for Roadway Seating:', className='mt-2'),
            dcc.RadioItems(id='roadway-seating',
                           options=[{'label': 'yes', 'value': 'yes'},
                                    {'label': 'no', 'value': 'no'}],
                           value='no', inputClassName="mx-1"
                           ),
            html.Label('Select borough:', className='mt-2'),
            dcc.RadioItems(id='boro',
                           options=[{'label': 'All', 'value': 'All'}]
                                   +
                                   [{'label': x, 'value': x} for x in df.Borough.unique()],
                           value='All', inputClassName="mx-1"
                           ),
        ], xs=12, sm=12, md=12, lg=3, xl=3
        ),

        dbc.Col(dcc.Graph(id='my-map', config={'displayModeBar':False}, className='mt-2'),
                xs=10, sm=10, md=10, lg=9, xl=9)
    ], justify='center'),
],
fluid=True,
className="dbc"
)

@callback(
    Output('my-map','figure'),
    Input('sidewalk-seating','value'),
    Input('roadway-seating', 'value'),
    Input('boro','value')
)
def undate_map(sidewalk_y_n, roadway_y_n, boro_v):
    dff = df.copy()
    dff = dff[dff['Approved for Sidewalk Seating'] == sidewalk_y_n]
    dff = dff[dff['Approved for Roadway Seating'] == roadway_y_n]
    dff = dff if boro_v == 'All' else dff[dff['Borough'] == boro_v]

    fig = px.scatter_mapbox(data_frame=dff, lat='Latitude', lon='Longitude',
                            hover_data={'Restaurant Name': True,
                                        'Business Address': True,
                                        'Latitude': False, 'Longitude': False,
                                        'Approved for Roadway Seating': True,
                                        'Approved for Sidewalk Seating': True},
                            mapbox_style="carto-positron",
                            zoom=10, template='vapor'
                            )
    fig.update_traces(marker={'color': '#39FF14'}),
    return fig


if __name__=='__main__':
    app.run_server(debug=False)