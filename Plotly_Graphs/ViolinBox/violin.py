import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio

#--------------------------------------------------------------------------------
# Import and filter data
df = pd.read_csv("bees.csv")
df['Value'] = pd.to_numeric(df['Value'])
mapping = {'HONEY, BEE COLONIES, AFFECTED BY DISEASE - INVENTORY, MEASURED IN PCT OF COLONIES':'Disease',
           'HONEY, BEE COLONIES, AFFECTED BY OTHER CAUSES - INVENTORY, MEASURED IN PCT OF COLONIES':'Other',
           'HONEY, BEE COLONIES, AFFECTED BY PESTICIDES - INVENTORY, MEASURED IN PCT OF COLONIES':'Pesticides',
           'HONEY, BEE COLONIES, AFFECTED BY PESTS ((EXCL VARROA MITES)) - INVENTORY, MEASURED IN PCT OF COLONIES':'Pests_excl_Varroa',
           'HONEY, BEE COLONIES, AFFECTED BY UNKNOWN CAUSES - INVENTORY, MEASURED IN PCT OF COLONIES':'Unknown',
           'HONEY, BEE COLONIES, AFFECTED BY VARROA MITES - INVENTORY, MEASURED IN PCT OF COLONIES':'Varroa_mites'}
df['Data Item'] = df['Data Item'].map(mapping)
df.rename(columns={'Data Item':'Affected by', 'Value':'Percent of Colonies Impacted'}, inplace=True)
print(df[:10][['Year','Period','State','Affected by','Percent of Colonies Impacted']])

#--------------------------------------------------------------------------------
# Build the violin/box plot

violinfig = px.violin(
    # data_frame=df.query("State == ['{}','{}']".format('ALABAMA','NEW YORK')),
    data_frame=df,
    x="Affected by",
    y="Percent of Colonies Impacted",
    category_orders={'Affected by':['Disease','Unknown','Pesticides','Other','Pests_excl_Varroa','Varroa_mites']},
    orientation="v",              # vertical 'v' or horizontal 'h'
    # points='all',               # 'outliers','suspectedoutliers', 'all', or False
    # box=True,                   # draw box inside the violins
    # color='State',              # differentiate markers by color
    # violinmode="overlay",       # 'overlay' or 'group'
    # color_discrete_sequence=["limegreen","red"],
    # color_discrete_map={"ALABAMA": "blue" ,"NEW YORK":"magenta"}, # map your chosen colors

    # hover_name='Year',          # values appear in bold in the hover tooltip
    # hover_data=['State'],       # values appear as extra data in the hover tooltip
    # custom_data=['Program'],    # values are extra data to be used in Dash callbacks

    # facet_row='State',          # assign marks to subplots in the vertical direction
    # facet_col='Period',         # assign marks to subplots in the horizontal direction
    # facet_col_wrap=2,           # maximum number of subplot columns. Do not set facet_row

    # log_x=True,                 # x-axis is log-scaled
    # log_y=True,                 # y-axis is log-scaled

    labels={"State":"STATE"},     # map the labels
    title='What is killing our Bees',
    width=1400,                   # figure width in pixels
    height=600,                   # igure height in pixels
    template='presentation',      # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                  # 'plotly_white', 'plotly_dark', 'presentation',
                                  # 'xgridoff', 'ygridoff', 'gridon', 'none'

    # animation_frame='Year',     # assign marks to animation frames
    # animation_group='',         # use only when df has multiple rows with same object
    # range_x=[5,50],             # set range of x-axis
    # range_y=[-5,100],           # set range of y-axis
    # category_orders={'Year':[2015,2016,2017,2018,2019]},    # set a specific ordering of values per column
)

# violinfig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000

# violinfig.update_layout(
#         yaxis = dict(
#         tickfont=dict(size=8)))

pio.show(violinfig)
