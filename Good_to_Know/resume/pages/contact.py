import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, order=3)

green_text = {'color':'green'}

def layout():
    return dbc.Row([
        dbc.Col([
    dcc.Markdown('# Adam Schroeder', className='mt-3'),
    dcc.Markdown('### FC Barcelona Forward', className='mb-5'),
    dcc.Markdown('### Personal info', style={'color':'gray'}),
    dcc.Markdown('Address', style=green_text),
    dcc.Markdown('Barcelona, Spain 08010'),
    dcc.Markdown('Phone Number', style=green_text),
    dcc.Markdown('212-123-4567'),
    dcc.Markdown('Email', style=green_text),
    dcc.Markdown('adam@myemail.com'),
    dcc.Markdown('Linkedin', style=green_text),
    dcc.Markdown('[www.linkedin.com/in/adam-schroeder-17b5a819/](https://www.linkedin.com/in/adam-schroeder-17b5a819/)', link_target='_blank'),
    dcc.Markdown('YouTube', style=green_text),
    dcc.Markdown('[www.youtube.com/charmingdata](https://www.youtube.com/charmingdata)', link_target='_blank'),
        ], width={'size':6, 'offset':2})
], justify='center')