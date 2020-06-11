# data from Kaiser Family Foundation and from Mapping Police Violence
# https://www.kff.org/state-category/demographics-and-the-economy/population/
# https://mappingpoliceviolence.org/

import plotly.express as px
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

df_states = pd.read_csv("state_pop.csv")

df = pd.read_csv("MPVDataset.csv")
df["Victim's age"] = pd.to_numeric(df["Victim's age"], errors='coerce').fillna(0).astype(np.int64)
df.rename(columns={'Body Camera (Source: WaPo)': 'Body camera', "Victim's gender": "Gender",
                   "Victim's age": 'Age', 'Fleeing (Source: WaPo)': 'Fleeing'}, inplace=True)
# -------------------------------------------------------------------------------------------

app.layout = html.Div([

    html.H2("Deaths by Police (2013-2019)", style={'text-align': 'center', 'text-decoration': 'underline'}),

    html.Div([
        html.P("Center of Sunburst to Analyze:", style={'font-weight': 'bold', 'text-decoration': 'underline'}),
        html.Div([
            dcc.RadioItems(id='sunroot',
                           options=[
                               {'label': 'Victim Armed', 'value': 'Unarmed'},
                               {'label': 'Victim Gender', 'value': 'Gender'},
                               {'label': 'Victim Fleeing', 'value': 'Fleeing'},
                               {'label': 'Geography', 'value': 'Geography'},
                               {'label': 'Police Body camera', 'value': 'Body camera'},
                           ],
                           value='Unarmed',
                           labelStyle={'display': 'inline-block'}
                           )
        ], className='six columns')
    ], className='row'),

    html.P(),

    html.Div([
        html.P("Age Breakdown:", style={'font-weight': 'bold', 'text-decoration': 'underline'}),
        html.Div([
            dcc.RadioItems(id='age_breakdown',
                           options=[
                               {'label': 'Yes', 'value': 'yes'},
                               {'label': 'No', 'value': 'no'},
                           ],
                           value='no',
                           labelStyle={'display': 'inline-block'}
                           )
        ], className='six columns')
    ], className='row'),

    html.P(),

    html.Div([

        html.Div([
            html.P("Select States:", style={'font-weight': 'bold', 'text-decoration': 'underline'}),
            html.Div([
                dcc.Dropdown(id='dropdown1',
                             options=[
                                 {'label': x, 'value': x}
                                 for x in sorted(df['State'].unique())
                             ],
                             value='TX',
                             multi=False,
                             clearable=False
                             ),
            ]),

            html.Div([
                dcc.Dropdown(id='dropdown2',
                             options=[
                                 {'label': x, 'value': x}
                                 for x in sorted(df['State'].unique())
                             ],
                             value='NY',
                             multi=False,
                             clearable=False
                             ),
            ]),

            html.Div([
                dcc.Dropdown(id='dropdown3',
                             options=[
                                 {'label': x, 'value': x}
                                 for x in sorted(df['State'].unique())
                             ],
                             value='FL',
                             multi=False,
                             clearable=False
                             ),
            ]),

            html.P(),

            html.Div([
                html.P("Select Races:", style={'font-weight': 'bold', 'text-decoration': 'underline'}),
                dcc.Dropdown(id='dropdown_r',
                             options=[
                                 {'label': "Asian", 'value': 'Asian'},
                                 {'label': "Black", 'value': 'Black'},
                                 {'label': "Hispanic", 'value': 'Hispanic'},
                                 {'label': "Native American", 'value': 'Native American'},
                                 {'label': "Pacific Islander", 'value': 'Pacific Islander'},
                                 {'label': "White", 'value': 'White'}
                             ],
                             value=['White', 'Black', 'Hispanic'],
                             multi=True,
                             clearable=True
                             ),
            ]),

            html.Div(id='state_info'),

        ], className='two columns'),

        html.Div([
            dcc.Graph(id='my_sunburst'),
        ], className='ten columns'),

    ], className='row'),

])


# -------------------------------------------------------------------------------------------

@app.callback(
    [Output('my_sunburst', 'figure'),
     Output('state_info', 'children')],
    [Input('sunroot', 'value'),
     Input('age_breakdown', 'value'),
     Input('dropdown1', 'value'),
     Input('dropdown2', 'value'),
     Input('dropdown3', 'value'),
     Input('dropdown_r', 'value')]
)
def update_graph(s_root, age_color, dp1, dp2, dp3, dr4):
    dff_st = df_states[df_states['Location'].isin([dp1, dp2, dp3])]
    dff = df[df['State'].isin([dp1, dp2, dp3])]

    if len(dr4) == 0:
        dff = dff[dff["Victim's race"].isin(['White', 'Black', 'Hispanic'])]
    else:
        dff = dff[dff["Victim's race"].isin(dr4)]

    if age_color == 'no':
        fig = px.sunburst(
            data_frame=dff,
            path=[s_root, 'State', "Victim's race"],
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )

        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        fig.update_traces(textinfo='label+percent parent', hovertemplate='Label: %{label}<br>' +
                                                                         'Deaths: %{value}<br>' +
                                                                         'Under: %{parent}<br>' +
                                                                         '<extra></extra>')
        return fig, [
            html.Table(
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.P(s + " population:"),
                                    html.P("White: " + str(w) + "%"),
                                    html.P("Black: " + str(b) + "%"),
                                    html.P("Hispanic: " + str(h) + "%")
                                ], style={"border-bottom": "1px solid #55575D"}
                            )
                        ]
                    )
                    for s, w, b, h in zip(dff_st['States'], dff_st['White'], dff_st['Black'], dff_st['Hispanic'])
                ])]

    if age_color == 'yes':
        fig = px.sunburst(
            data_frame=dff,
            path=[s_root, 'State', "Victim's race"],
            color_continuous_scale=px.colors.sequential.BuGn,
            color='Age',
            range_color=[20, 50],
        )

        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        fig.update_traces(textinfo='label+percent parent', hovertemplate='Label: %{label}<br>' +
                                                                         'Deaths: %{value}<br>' +
                                                                         'Under: %{parent}<br>' +
                                                                         'Avg Age: %{color:.1f}<br>' +
                                                                         '<extra></extra>')
        return fig, [
            html.Table(
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.P(s + " breakdown:"),
                                    html.P("White: " + str(w) + "%"),
                                    html.P("Black: " + str(b) + "%"),
                                    html.P("Hispanic: " + str(h) + "%")
                                ], style={"border-bottom": "1px solid #55575D"}
                            )
                        ]
                    )
                    for s, w, b, h in zip(dff_st['States'], dff_st['White'], dff_st['Black'], dff_st['Hispanic'])
                ])]

# -------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=False)
