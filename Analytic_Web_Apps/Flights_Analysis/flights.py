from dash import Dash, html, dcc, Output, Input, dash_table, callback   # pip install dash
import dash_bootstrap_components as dbc                                  # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN, dbc.icons.FONT_AWESOME])
server = app.server

# our data
df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/Flights_Analysis/europe-flights-reduced.csv')
df['YEAR'] = df['YEAR'].astype(str)

# create datatable
def create_table(data):
    # pivot table
    pbc = data.groupby(['GEO','PARTNER'])['Value'].sum().reset_index()
    pbc = pbc.pivot(index='GEO', columns='PARTNER')['Value'].reset_index()
    pbc = pbc[pbc['GEO'].isin(['Allemagne','Espagne','France','Grèce','Italie',
                               'Pays-Bas','Portugal','Royaume-Uni','Suisse','Turquie'])]

    # add total values row and column
    sums_col = pbc.select_dtypes(np.number).sum()
    pbc = pd.concat([pbc, sums_col.to_frame().T], ignore_index=True)
    pbc.at[10, 'GEO'] = 'Total'

    sums_r = pbc.select_dtypes(np.number).sum(axis=1)
    pbc['total'] = sums_r

    return dash_table.DataTable(
        data=pbc.to_dict('records'),
        fixed_columns={'headers': True, 'data': 1},
        style_table={'minWidth': '100%'}
    )


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Span([
                    html.I(className='fa-solid fa-plane-departure'),
                " Number of Passangers between European countries 2019-2021 ",
                html.I(className="fa-solid fa-plane-departure")], className='h2')
    ], width=10)
    ], justify='center', className='my-2'),

    dbc.Row([
        dbc.Col([html.Label('YEAR', className='bg-secondary')],width=2),
        dbc.Col([html.Label('Number of passangers per Year', className='bg-secondary')], width={"size": 4, "offset": 1}),
        dbc.Col([html.Label('Total passangers per Month', className='bg-secondary')], width={"size": 4, "offset": 1})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(['2019', '2020', '2021'], multi=True, id='year_dpdn'),
            html.Label('MONTH', className='bg-secondary'),
            dcc.Dropdown([1,2,3,4,5,6,7,8,9,10,11,12], multi=True, id='month_dpdn'),
            html.Label('GEO', className='bg-secondary'),
            dcc.Dropdown([x for x in sorted(df['GEO'].unique())], multi=True, id='geo_dpdn'),
            html.Label('PARTNER', className='bg-secondary'),
            dcc.Dropdown([x for x in sorted(df['PARTNER'].unique())], multi=True, id='partner_dpdn'),
            html.Label('Number of countries', className='bg-secondary'),
            html.H1(id='num_country')
        ], width=2),
        dbc.Col([
            dcc.Graph(id='hist', config={'displayModeBar':False})
        ], width=4),
        dbc.Col([
            dcc.Graph(id='line', config={'displayModeBar':False})
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([html.Label("Number of Passengers Between Countries", className="align-middle")], width={"size": 6, "offset": 3})
    ], className='bg-secondary'),

    dbc.Row([
        dbc.Col([
            html.Div(id='my-table')
        ], width=12)
    ])
])

@callback(
    Output('hist', 'figure'),
    Output('line', 'figure'),
    Output('my-table', 'children'),
    Output('num_country', 'children'),
    Input('year_dpdn', 'value'),
    Input('month_dpdn', 'value'),
    Input('geo_dpdn', 'value'),
    Input('partner_dpdn', 'value')
)
def update_graphs(year_v, month_v, geo_v, partner_v):
    dff = df.copy()
    print(type(year_v))

    if any([year_v, month_v, geo_v, partner_v]):
        if year_v is not None:
            if len(year_v)>0:
                dff = dff.query(f"YEAR == {year_v}")
        if month_v is not None:
            if len(month_v) > 0:
                dff = dff.query(f"MONTH == {month_v}")
        if geo_v is not None:
            if len(geo_v)>0:
                dff = dff.query(f"GEO == {geo_v}")
                country_count = len(geo_v)
        if geo_v is None or len(geo_v)==0:
            country_count = 35
        if partner_v is not None:
            if len(partner_v) > 0:
                dff = dff.query(f"PARTNER == {partner_v}")

        psg_by_month = dff.groupby('MONTH')['Value'].sum().reset_index()
        psg_by_month = psg_by_month.sort_values('Value',
                                                ignore_index=True,
                                                ascending=False)
        fig_line = px.line(psg_by_month, x='MONTH', y='Value').update_xaxes(type='category').update_layout(margin=dict(l=10, r=10, t=10, b=10))

        fig_hist = px.histogram(dff, x='YEAR', y='Value').update_layout(margin=dict(l=10, r=10, t=10, b=10))

        table = create_table(dff)

        return fig_hist, fig_line, table, country_count

    if not any([year_v, month_v, geo_v, partner_v]):  # equivalent to if all are None...
        psg_by_month = df.groupby('MONTH')['Value'].sum().reset_index()
        psg_by_month = psg_by_month.sort_values('Value',
                                                ignore_index=True,
                                                ascending=False)
        fig_line = px.line(psg_by_month, x='MONTH', y='Value').update_xaxes(type='category').update_layout(margin=dict(l=10, r=10, t=10, b=10))

        fig_hist = px.histogram(dff, x='YEAR', y='Value').update_layout(margin=dict(l=10, r=10, t=10, b=10))

        table = create_table(df)


        return fig_hist, fig_line, table, df['GEO'].nunique()


if __name__=='__main__':
    app.run(debug=True)
