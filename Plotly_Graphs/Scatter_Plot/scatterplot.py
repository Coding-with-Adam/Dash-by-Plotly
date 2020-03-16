import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0) #pip install plotly==4.5.0
import plotly.express as px
import plotly.io as pio
import statsmodels.api as sm

tips = px.data.tips()
tips['tbl_size'] = tips['size']
# print (tips[:3])

#fake margin of error, standard deviation, or 95% confidence interval
tips['err_plus'] = tips['total_bill']/100
tips['err_minus'] = tips['total_bill']/40


scatterplot = px.scatter(
    data_frame=tips,
    x="total_bill",
    y="tip",

    size="tbl_size",                                          # differentiate markers by size
    size_max=13,                                              # set maximum marker size
    symbol="smoker",                                          # differentiate markers by symbol
    symbol_sequence=[3,'square-open'],                        # set marker symbols
    symbol_map={"No": "square-open" ,"Yes":3},                # map your chosen symbols
    color="day",                                              # differentiate markers by color
    opacity=0.5,                                              # set opacity of markers
    color_discrete_sequence=["red","green","blue","black"],   # set marker colors. When color colum isn't numeric data
    color_discrete_map={"Thur": "green" ,"Fri":"red",         # map your chosen colors
                        "Sat":"black","Sun":"brown"},
    color_continuous_scale=px.colors.diverging.Armyrose,      # set marker colors. When color colum is numeric data
    color_continuous_midpoint=2,                              # set desired midpoint. When colors=diverging

    text='tbl_size',            # values appear in figure as text labels
    hover_name='time',          # values appear in bold in the hover tooltip
    hover_data=['time'],        # values appear as extra data in the hover tooltip
    custom_data=['tbl_size'],   # values are extra data to be used in Dash callbacks

    facet_row='tbl_size',       # assign marks to subplots in the vertical direction
    facet_col='tbl_size',       # assign marks to subplots in the horizontal direction
    facet_col_wrap=3,           # maximum number of subplot columns. Do not set facet_row
    marginal_x='rug',           # subplot is drawn to visualize the axis distribution
    marginal_y='box',           # options:'rug','box','violin','histogram'
    trendline='ols',            # regression line: 'ols','lowess' (import statsmodels)
    log_x=True,                 # x-axis is log-scaled
    log_y=True,                 # y-axis is log-scaled
    error_y="err_plus",         # y-axis error bars are symmetrical or for positive direction
    error_y_minus="err_minus",  # y-axis error bars in the negative direction

    labels={"tip":"the TIP",
    "smoker":"SMOKER or NOT"},  # map the labels
    title='All Tips',           # figure title
    width=500,                  # figure width in pixels
    height=1000,                # igure height in pixels
    template='plotly_dark',     # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                # 'plotly_white', 'plotly_dark', 'presentation',
                                # 'xgridoff', 'ygridoff', 'gridon', 'none'

    animation_frame='tbl_size', # assign marks to animation frames
    #animation_group=,          # use only when df has multiple rows with same object
    range_x=[5,50],             # set range of x-axis
    range_y=[0,10],             # set range of x-axis
    category_orders={'tbl_size':[1,2,3,4,5,6]},    # set a specific ordering of values per column

)

# scatterplot.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
# scatterplot.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

# print(scatterplot)

pio.show(scatterplot)
