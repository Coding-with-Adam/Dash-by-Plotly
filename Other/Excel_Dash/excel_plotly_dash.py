import dash
import plotly.express as px
import pandas as pd


# Data Exploration with Pandas (Python)
# ----------------------------------------------------------------

df = pd.read_csv("vgsales.csv")  # GregorySmith Kaggle

print(df[:3])
print(df.iloc[:5, [2,3,4,5,10]])
print(df['Genre'].nunique())
print(df['Genre'].unique())
print(sorted(df['Year'].unique()))


# Data Visualization with Plotly (Python)
# ----------------------------------------------------------------

fig_pie = px.pie(data_frame=df, names='Genre', values='Japan Sales')
fig_pie = px.pie(data_frame=df, names='Genre', values='North American Sales')
fig_pie.show()

fig_hist = px.histogram(data_frame=df, x='Genre', y='Japan Sales')
fig_hist = px.histogram(data_frame=df, x='Year', y='Japan Sales')
fig_hist.show()

df = df.groupby(['Year','Genre']).sum()
df = df.reset_index()
print(df[-6:])
fig_bar = px.bar(data_frame=df, x='Year', y='Japan Sales', facet_col='Genre',
                 facet_col_wrap=3)
fig_bar.show()


# Interactive Graphs with Dash (Python)
# ----------------------------------------------------------------

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

app = dash.Dash(__name__)

app.layout= html.Div([
    html.H1("Excel Analysis of Graphs"),
    dcc.Dropdown(id='genre-choice',
                 options=[{'label': x, 'value': x}
                          for x in sorted(df['Genre'].unique())],
                 value='Action'
                 ),
    dcc.Graph(id='my-graph', figure={}),
])


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='genre-choice', component_property='value')
)
def interactive_graphing(value):
    print(value)
    dff = df[df.Genre==value]
    fig_hist = px.bar(data_frame=dff, x='Year', y='Japan Sales')
    return fig_hist


if __name__=='__main__':
    app.run_server()
