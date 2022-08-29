import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', order=0)

# resume sample template from https://zety.com/
layout = html.Div([
    dcc.Markdown('# Adam Schroeder', style={'textAlign':'center'}),
    dcc.Markdown('New York, USA', style={'textAlign': 'center'}),

    dcc.Markdown('### Professional Summary', style={'textAlign': 'center'}),
    html.Hr(),
    dcc.Markdown('Highly motivate Sales Associate with extensive customer service and sales experience. \n'
                 'Outgoing sales professional with track record of driving increased sale, improving \n'
                 'buying experience and elevating company profile with target market.',
                 style={'textAlign': 'center', 'white-space': 'pre'}),

    dcc.Markdown('### Skills', style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
            * Guest services 
            * Inventory control procedures
            * Merchandising expertise
            ''')
        ], width={"size": 3, "offset": 1}),
        dbc.Col([
            dcc.Markdown('''
            * Loss prevention 
            * Cash register operations
            * Product promotions
            ''')
        ], width=3)
    ], justify='center'),

    dcc.Markdown('### Work History', style={'textAlign': 'center'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('03/2018 to current', style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Senior Sales Associate \n'
                         'Bed Bath & Beyond Inc - New York, NY',
                         style={'white-space': 'pre'},
                         className='ms-3'),
            html.Ul([
                html.Li('Applied security and loss prevention training toward recognizing risks and reducing store theft'),
                html.Li('Trained and developed sales team associates in products, selling techniques and procedures'),
                html.Li('Maintained organized, presentable merchandise to drive continuous sales'),
                html.Li('Implemented up-selling strategies for recommending accessories and couplementary purchases')
            ])
        ], width=5)
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('06/2017 to 03/2018',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Sales Associate \n'
                         'Target - New York, NY',
                         style={'white-space': 'pre'},
                         className='ms-3'),
            html.Ul([
                html.Li(
                    'Maintained organized, presentable merchandise to drive continuous sales'),
                html.Li(
                    'Trained and developed sales team associates in products, selling techniques and procedures'),
                html.Li(
                    'Organized racks and shelves to maintain store visual appeal, engage customers and promote merchandise'),
                html.Li(
                    'Implemented up-selling strategies for recommending accessories and couplementary purchases')
            ])
        ], width=5)
    ], justify='center'),

    dcc.Markdown('### Education', style={'textAlign': 'center'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('2013',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Bachelor of Arts: Business Administration\n'
                         'San Francisco State University - San Francisco, CA',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=5)
    ], justify='center'),
])
