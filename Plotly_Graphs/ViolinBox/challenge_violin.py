# Solution to Violin Challenge

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
df = df[df['Affected by']=='Disease']
print(df[:10][['Year','Period','State','Affected by','Percent of Colonies Impacted']])

#--------------------------------------------------------------------------------
# Build the violin/box plot

violinfig = px.violin(
    data_frame=df.query("State == ['{}','{}']".format('TEXAS','IDAHO')),
    x="Affected by",
    y="Percent of Colonies Impacted",
    orientation="v",
    points='all',
    box=True,
    color='State',
    color_discrete_map={"TEXAS": "limegreen" ,"IDAHO":"red"},
    hover_data=['Period'],


    labels={"State":"STATE"},
    title='What is killing our Bees',
    width=1400,
    height=600,
    template='plotly_dark',
)

violinfig.update_traces(meanline_visible=True, meanline_color='blue')

pio.show(violinfig)
