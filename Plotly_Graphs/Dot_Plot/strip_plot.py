# Charming Data channel: Data visualizations in python

import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) #pip install plotly==4.5.4
import plotly.express as px
import plotly.io as pio

#--------------------------------------------------------------------------------------------
# Filter Data
df = pd.read_csv("suicide_rates.csv")
mapping = {'G.I. Generation':'G.I. Generation 1901-1927','Silent':"Silent 28'-45'",
           "Boomers":"Boomers 46'-64'","Generation X":"Generation X 65'-80'",
           "Millenials":"Millenials 81'-96'","Generation Z":"Generation Z 96'-2012"}
df['generation'] = df['generation'].map(mapping)

# year_list = [1992,1993,1994,1995]
# df = df[df['year'].isin(year_list)]
# df = df.groupby(['sex','country','generation','year'], as_index=False)[['suicides/100k pop']].mean()
df = df.groupby(['sex','country','generation'], as_index=False)[['suicides/100k pop']].mean()
print (df[:5])
#--------------------------------------------------------------------------------------------

stripfig = px.strip(
    data_frame=df,
    x='generation',
    y='suicides/100k pop',
    category_orders={"generation":["G.I. Generation 1901-1927","Silent 28'-45'","Boomers 46'-64'",
    "Generation X 65'-80'","Millenials 81'-96'","Generation Z 96'-2012"]},
    hover_data=['country'],        # values appear as extra data in the hover tooltip
    # color='sex',                 # differentiate color between marks
    # color_discrete_sequence=["springgreen","yellow"],             # set specific marker colors for discrete values
    # color_discrete_map={"male":"rosybrown" ,"female":"orangered"},  # map your chosen colors
    # orientation='v',             # 'v','h': orientation of the marks
    # stripmode='group',           # in 'overlay' mode, bars are top of one another.
                                   # in 'group' mode, bars are placed beside each other.
#--------------------------------------------------------------------------------------------
    # facet_row='year',            # assign marks to subplots in the vertical direction
    # facet_col='year',            # assigns marks to subplots in the horizontal direction
    # facet_col_wrap=2,            # maximum number of subplot columns. Do not set facet_row!
#--------------------------------------------------------------------------------------------

    # log_x=True,                  # x-axis is log-scaled
    # log_y=True,                  # y-axis is log-scaled
    # hover_name='country',        # values appear in bold in the hover tooltip
    # custom_data=['population'],  # values are extra data to be used in Dash callbacks

    # labels={"sex":"Gender",
    # "generation":"GENERATION"},  # map the labels
    # title='Suicide Rate',        # figure title
    # width=1000,                  # figure width in pixels
    # height=600,                  # igure height in pixels
    # template='seaborn',          # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
    #                              # 'plotly_white', 'plotly_dark', 'presentation',
    #                              # 'xgridoff', 'ygridoff', 'gridon', 'none'

    # animation_frame='year',      # assign marks to animation frames
    # # animation_group='sex',     # use only when df has multiple rows with same object
    # # range_x=[5,50],            # set range of x-axis
    # range_y=[0,190],             # set range of x-axis
)
# stripfig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000

pio.show(stripfig)
