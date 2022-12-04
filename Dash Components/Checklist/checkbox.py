# Video:    [Checklist - Python Dash Plotly](https://youtu.be/amRFPjSgEnk )
# Docs:     [dcc.Checklist](https://dash.plotly.com/dash-core-components/checklist)
#

import pandas as pd     
import datetime as dt

import dash                                     # pip install dash
from dash import dcc, html, Input, Output
import plotly.express as px

df = pd.read_csv("Urban_Park_Ranger_Animal_Condition_Response.csv")  # https://drive.google.com/file/d/1m63TNoZdDUtH5XhK-mc4kDFzO9j97eWW/view?usp=sharing

#------------------------------------------------------------------------------
# Drop rows w/ no animals found or calls w/ varied age groups
df = df[(df['# of Animals']>0) & (df['Age']!='Multiple')]

# Create column for month from time call made to Ranger
df['Month Call Made'] = pd.to_datetime(df['Date and Time of initial call'])
df['Month Call Made'] = df['Month Call Made'].dt.strftime('%m')
df.sort_values('Month Call Made', inplace=True)
df['Month Call Made'] = df['Month Call Made'].replace({"01":"January","02":"February","03":"March",
                                                       "04":"April","05":"May","06":"June",
                                                       "07":"July","08":"August","09":"September",
                                                       "10":"October","11":"November","12":"December",})
# Copy columns to new columns with clearer names
df['Amount of Animals'] = df['# of Animals']
#------------------------------------------------------------------------------

app = dash.Dash(__name__)

#------------------------------------------------------------------------------
app.layout = html.Div([

        html.Div([
            html.Pre(children= "NYC Calls for Animal Rescue",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),

        html.Div([
            dcc.Checklist(
                id='my_checklist',                      # used to identify component in callback
                options=[
                         {'label': x, 'value': x, 'disabled':False}
                         for x in df['Month Call Made'].unique()
                ],
                value=['January','July','December'],    # values chosen by default

                className='my_box_container',           # class of the container (div)
                # style={'display':'flex'},             # style of the container (div)

                inputClassName='my_box_input',          # class of the <input> checkbox element
                # inputStyle={'cursor':'pointer'},      # style of the <input> checkbox element

                labelClassName='my_box_label',          # class of the <label> that wraps the checkbox input and the option's label
                # labelStyle={'background':'#A5D6A7',   # style of the <label> that wraps the checkbox input and the option's label
                #             'padding':'0.5rem 1rem',
                #             'border-radius':'0.5rem'},

                #persistence='',                        # stores user's changes to dropdown in memory ( I go over this in detail in Dropdown video: https://youtu.be/UYH_dNSX1DM )
                #persistence_type='',                   # stores user's changes to dropdown in memory ( I go over this in detail in Dropdown video: https://youtu.be/UYH_dNSX1DM )
            ),
        ]),

        html.Div([
            dcc.Graph(id='the_graph')
    ]),

])

#------------------------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_checklist', component_property='value')]
)
def update_graph(options_chosen):

    dff = df[df['Month Call Made'].isin(options_chosen)]
    print (dff['Month Call Made'].unique())

    piechart=px.pie(
            data_frame=dff,
            values='Amount of Animals',
            names='Month Call Made',
            )

    return (piechart)

#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
