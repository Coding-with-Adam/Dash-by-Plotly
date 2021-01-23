import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

# data source: https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017
# data owner: Chubak Bidpaa
df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Kindergarten in Iran',
            style={'textAlign': 'center'}),

    dcc.Graph(id='bargraph',
              figure=px.bar(df, barmode='group', x='Years',
                            y=['Girls Kindergarten',
                               'Boys Kindergarten']
                            ).add_layout_image(
                                  dict(
                                      source="https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/dash-plotly-logo.png",
                                      # source="assets/dash-plotly-logo.png",
                                      xref="paper",
                                      yref="paper",
                                      x=0,
                                      y=1,
                                      sizex=1,
                                      sizey=1,
                                      sizing="stretch",
                                      opacity=0.5,
                                      layer="below"
                                  )
                            ).update_layout(
                                template="plotly_white")
              )
])


if __name__=='__main__':
    app.run_server(debug=True, port=3000)
