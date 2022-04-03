from dash import Dash, dcc  # pip install dash==2.3.0  (or higher)
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = px.data.stocks()
print(df.head())
fig_left = px.line(df, 'date', ['NFLX', 'AAPL', 'GOOG'])
fig_left.update_yaxes(title=dict(text='$(a+b)^{2 } = a^{2 } + ab + b^{2}$'))

fig_right = px.line(df, 'date', ['NFLX', 'AAPL', 'GOOG'])
fig_right.update_yaxes(title=dict(text=r'$\text{Google} = a^{2 } + ab + b^{2}$'))

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dcc.Markdown('# Dash 2.3.0 now has Mathjax', style={'textAlign': 'center'}, className='mb-3'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('## Mathjax Alone:'),
        ], width=4),
        dbc.Col([
            dcc.Markdown('## Mathjax WITH Text:')
        ], width=4)
    ], className='mb-3', justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('$x=\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$', mathjax=True),  # make sure to user raw string (r) if you're using one backslash
        ], width=4),
        dbc.Col([
            dcc.Markdown('Add text outside of dollar signs $x=\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$', mathjax=True)
        ], width=4)
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_left, mathjax=True)
        ], width=6),

        dbc.Col([
            dcc.Graph(figure=fig_right, mathjax=True)
        ], width=6),
    ])
])


if __name__=='__main__':
    app.run_server(debug=False)
