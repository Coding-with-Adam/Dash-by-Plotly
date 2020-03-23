import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) #pip install plotly==4.5.4
import plotly.express as px
import plotly.io as pio

#------------------------------------------------------------------------
# Filter the data
# Data from https://covidtracking.com/api/
df = pd.read_csv("covid-19-states-daily.csv")
df['dateChecked'] = pd.to_datetime(df['dateChecked'])
df = df[df['dateChecked'].dt.date.astype(str) == '2020-03-17']
df = df[df['death']>=5]
print (df)

pie_chart = px.pie(
        data_frame=df,
        values='death',
        names='state',
        color='state',                      #differentiate markers (discrete) by color
        color_discrete_sequence=["red","green","blue","orange"],     #set marker colors
        # color_discrete_map={"WA":"yellow","CA":"red","NY":"black","FL":"brown"},
        hover_name='negative',              #values appear in bold in the hover tooltip
        # hover_data=['positive'],            #values appear as extra data in the hover tooltip
        # custom_data=['total'],              #values are extra data to be used in Dash callbacks
        labels={"state":"the State"},       #map the labels
        title='Coronavirus in the USA',     #figure title
        template='presentation',            #'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                            #'plotly_white', 'plotly_dark', 'presentation',
                                            #'xgridoff', 'ygridoff', 'gridon', 'none'
        width=800,                          #figure width in pixels
        height=600,                         #figure height in pixels
        hole=0.5,                           #represents the hole in middle of pie
        )

# pie_chart.update_traces(textposition='outside', textinfo='percent+label',
#                         marker=dict(line=dict(color='#000000', width=4)),
#                         pull=[0, 0, 0.2, 0], opacity=0.7, rotation=180)



pio.show(pie_chart)
