import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) #pip install plotly==4.5.4
import plotly.express as px
import plotly.io as pio

# excel sheet from https://www.kaggle.com/rajanand/prison-in-india/data
# National Crime Records Bureau (NCRB), Govt of India has shared this dataset
df = pd.read_csv("Caste.csv")
df = df[df['state_name']=='Maharashtra']
df = df.groupby(['year','gender',],as_index=False)[['detenues','under_trial','convicts','others']].sum()
print (df[:5])

#fake margin of error, standard deviation, or 95% confidence interval
# df['err_plus'] = df['convicts']/100
# df['err_minus'] = df['convicts']/40

barchart = px.bar(
    data_frame=df,
    x="year",
    y="convicts",
    color="gender",               # differentiate color of marks
    opacity=0.9,                  # set opacity of markers (from 0 to 1)
    orientation="v",              # 'v','h': orientation of the marks
    barmode='relative',           # in 'overlay' mode, bars are top of one another.
                                  # in 'group' mode, bars are placed beside each other.
                                  # in 'relative' mode, bars are stacked above (+) or below (-) zero.
    #----------------------------------------------------------------------------------------------
    # facet_row='caste',          # assign marks to subplots in the vertical direction
    # facet_col='caste',          # assigns marks to subplots in the horizontal direction
    # facet_col_wrap=2,           # maximum number of subplot columns. Do not set facet_row!

    # color_discrete_sequence=["pink","yellow"],               # set specific marker colors. Color-colum data cannot be numeric
    # color_discrete_map={"Male": "gray" ,"Female":"red"},     # map your chosen colors
    # color_continuous_scale=px.colors.diverging.Picnic,       # set marker colors. When color colum is numeric data
    # color_continuous_midpoint=100,                           # set desired midpoint. When colors=diverging
    # range_color=[1,10000],                                   # set your own continuous color scale
    #----------------------------------------------------------------------------------------------
    # text='convicts',            # values appear in figure as text labels
    # hover_name='under_trial',   # values appear in bold in the hover tooltip
    # hover_data=['detenues'],    # values appear as extra data in the hover tooltip
    # custom_data=['others'],     # invisible values that are extra data to be used in Dash callbacks or widgets

    # log_x=True,                 # x-axis is log-scaled
    # log_y=True,                 # y-axis is log-scaled
    # error_y="err_plus",         # y-axis error bars are symmetrical or for positive direction
    # error_y_minus="err_minus",  # y-axis error bars in the negative direction

    labels={"convicts":"Convicts in Maharashtra",
    "gender":"Gender"},           # map the labels of the figure
    title='Indian Prison Statistics', # figure title
    width=1400,                   # figure width in pixels
    height=720,                   # figure height in pixels
    template='gridon',            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                  # 'plotly_white', 'plotly_dark', 'presentation',
                                  # 'xgridoff', 'ygridoff', 'gridon', 'none'

    # animation_frame='year',     # assign marks to animation frames
    # # animation_group=,         # use only when df has multiple rows with same object
    # # range_x=[5,50],           # set range of x-axis
    # range_y=[0,9000],           # set range of x-axis
    # category_orders={'year':    # force a specific ordering of values per column
    # [2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001]},

)

# barchart.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
# barchart.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

# barchart.update_layout(uniformtext_minsize=14, uniformtext_mode='hide',
#                        legend={'x':0,'y':1.0}),
# barchart.update_traces(texttemplate='%{text:.2s}', textposition='outside',
#                        width=[.3,.3,.3,.3,.3,.3,.6,.3,.3,.3,.3,.3,.3])


pio.show(barchart)
