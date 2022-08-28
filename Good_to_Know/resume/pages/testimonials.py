import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, order=2)

def layout():
    return html.Div([
    html.H3("People that I've had the pleasure to work with", style={'textAlign':'center'}, className='my-3'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('#### Xavier Hernández Creus'),
            dcc.Markdown('FC Barcelona Head Coach')
        ], width=2),
        dbc.Col([
            dcc.Markdown('Adam is very professional. I really appreciate his quick thinking '
                         'and great teamwork. I know a coach is not supposed to say this, but '
                         'although O. Dembélé is a great player, Adam is my Forward Favorito.',
                         className='ms-3'),
        ], width=5)
    ], justify='center'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('#### Ousmane Dembélé'),
            dcc.Markdown('FC Barcelona Attacking Midfielder')
        ], width=2),
        dbc.Col([
            dcc.Markdown('Adam is so good with the ball. Every time he has the ball, I can see the stadium rise to its feet.'
                         ' And he always shares goal opportunities with his teammates. The opposite of selfish. I know it is not '
                         'appropriate for a player to say this, but I wish Adam was our coach instead of Xavier.',
                         className='ms-3'),
        ], width=5)
    ], justify='center'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('#### Eric Garcia'),
            dcc.Markdown('FC Barcelona Defender')
        ], width=2),
        dbc.Col([
            dcc.Markdown('I feel so lucky to have a teammate like Adam on my team. People talk about Messi all the time '
                         'but the talent Adam has for making goals is unmatched. Plus, Adam has never evaded taxes, so you '
                         'would be lucky to have him on your team.',
                         className='ms-3'),
        ], width=5)
    ], justify='center')
])
