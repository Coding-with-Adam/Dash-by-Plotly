# Bar charts are useful for displaying data that is classified into nominal or ordinal categories.
# A bar chart uses bars to show comparisons between categories of data. A bar chart will always have two axis.
# One axis will generally have numerical values, and the other will describe the types of categories being compared.

import pandas as pd #(version 0.24.2)
import datetime as dt
import dash         #(version 1.0.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly       #(version 4.4.1)
import plotly.express as px

df = pd.read_csv("Urban_Park_Ranger_Animal_Condition_Response.csv")

#-------------------------------------------------------------------------------------
# Drop rows w/ no animals found or calls w/ varied age groups
df = df[(df['# of Animals']>0) & (df['Age']!='Multiple')]

# Extract month from time call made to Ranger
df['Month of Initial Call'] = pd.to_datetime(df['Date and Time of initial call'])
df['Month of Initial Call'] = df['Month of Initial Call'].dt.strftime('%m')

# Copy columns to new columns with clearer names
df['Amount of Animals'] = df['# of Animals']
df['Time Spent on Site (hours)'] = df['Duration of Response']
#-------------------------------------------------------------------------------------

app = dash.Dash(__name__)

#-------------------------------------------------------------------------------------
app.layout = html.Div([

        html.Div([
            html.Pre(children= "NYC Calls for Animal Rescue",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),

        html.Div([
            html.Label(['X-axis categories to compare:'],style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='xaxis_raditem',
                options=[
                         {'label': 'Month Call Made', 'value': 'Month of Initial Call'},
                         {'label': 'Animal Health', 'value': 'Animal Condition'},
                ],
                value='Animal Condition',
                style={"width": "50%"}
            ),
        ]),

        html.Div([
            html.Br(),
            html.Label(['Y-axis values to compare:'], style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='yaxis_raditem',
                options=[
                         {'label': 'Time Spent on Site (hours)', 'value': 'Time Spent on Site (hours)'},
                         {'label': 'Amount of Animals', 'value': 'Amount of Animals'},
                ],
                value='Time Spent on Site (hours)',
                style={"width": "50%"}
            ),
        ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])

#-------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
)

def update_graph(x_axis, y_axis):

    dff = df
    # print(dff[[x_axis,y_axis]][:1])

    barchart=px.bar(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            title=y_axis+': by '+x_axis,
            # facet_col='Borough',
            # color='Borough',
            # barmode='group',
            )

    barchart.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})

    return (barchart)

if __name__ == '__main__':
    app.run_server(debug=True)
