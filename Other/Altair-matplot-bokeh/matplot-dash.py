from dash import Dash, html, dcc, Input, Output, dash_table  # pip install dash
import dash_bootstrap_components as dbc
import pandas as pd

import matplotlib.pyplot as plt             # pip install matplotlib
import mpld3                                # pip install mpld3


df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Berlin_crimes.csv")
print(df.head())


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Interactive Matplotlib with Dash", className='mb-2', style={'textAlign':'center'}),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='yeardropdown',
                value=2012,
                clearable=False,
                options=[{'label': x, 'value': x} for x in df.Year.unique()])
        ], width=6),
        dbc.Col([
            dcc.Dropdown(
                id='distdropdown',
                value='Mitte',
                clearable=False,
                options=[{'label': x, 'value': x} for x in
                         sorted(df.District.unique())])
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Iframe(
                id='scatter-plot',
                srcDoc=None,  # here is where we will put the graph we make
                style={'border-width': '5', 'width': '100%',
                       'height': '500px'}),

        ], width=6),
        dbc.Col([
            html.Iframe(
                id='bar-plot',
                srcDoc=None,  # here is where we will put the graph we make
                style={'border-width': '5', 'width': '100%',
                       'height': '500px'}),

        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='table-placeholder', children=[])
        ], width=12),
    ]),

])

# Create interactivity between components and graph
@app.callback(
    Output('scatter-plot', 'srcDoc'),
    Output('bar-plot', 'srcDoc'),
    Output('table-placeholder', 'children'),
    Input('yeardropdown', 'value'),
    Input('distdropdown', 'value')
)
def plot_data(selected_year, selected_district):

    # filter data based on user selection
    dff = df[df.Year == selected_year]
    dff = dff[dff.District == selected_district]

    # build scatter plot
    fig, ax = plt.subplots()
    ax.scatter(x=dff.Damage, y=dff.Graffiti, s=dff.Drugs)
    ax.set_xlabel("Damage")
    ax.set_ylabel("Graffiti")
    ax.grid(color='lightgray', alpha=0.7)
    html_scatter = mpld3.fig_to_html(fig)

    # build bar plot
    fig, ax = plt.subplots()
    ax.bar(x=dff.Location, height=dff.Robbery)
    ax.set_xlabel(selected_district)
    ax.set_ylabel("Robbery")
    ax.grid(color='lightgray', alpha=0.7)
    html_bar = mpld3.fig_to_html(fig)

    # build DataTable
    mytable = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dff.columns],
        data=dff.to_dict('records'),
    )

    return html_scatter, html_bar, mytable


if __name__ == '__main__':
    app.run_server(debug=False, port=8002)
