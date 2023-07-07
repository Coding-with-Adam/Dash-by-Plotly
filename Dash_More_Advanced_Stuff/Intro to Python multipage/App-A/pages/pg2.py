import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__)

df = px.data.tips()

layout = html.Div(
    [
        dcc.RadioItems([x for x in df.day.unique()], id='day-choice'),
        dcc.Graph(id='bar-fig',
                  figure=px.bar(df, x='smoker', y='total_bill'))
    ]
)

