import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio


#--------------------------------------------------------------------------------
# Import and filter data
df = pd.read_csv("dup_bees.csv")
df['Value'] = pd.to_numeric(df['Value'])
mapping = {'HONEY, BEE COLONIES, AFFECTED BY DISEASE - INVENTORY, MEASURED IN PCT OF COLONIES':'Disease',
           'HONEY, BEE COLONIES, AFFECTED BY OTHER CAUSES - INVENTORY, MEASURED IN PCT OF COLONIES':'Other',
           'HONEY, BEE COLONIES, AFFECTED BY PESTICIDES - INVENTORY, MEASURED IN PCT OF COLONIES':'Pesticides',
           'HONEY, BEE COLONIES, AFFECTED BY PESTS ((EXCL VARROA MITES)) - INVENTORY, MEASURED IN PCT OF COLONIES':'Pests_excl_Varroa',
           'HONEY, BEE COLONIES, AFFECTED BY UNKNOWN CAUSES - INVENTORY, MEASURED IN PCT OF COLONIES':'Unknown',
           'HONEY, BEE COLONIES, AFFECTED BY VARROA MITES - INVENTORY, MEASURED IN PCT OF COLONIES':'Varroa_mites'}
df['Data Item'] = df['Data Item'].map(mapping)
df.rename(columns={'Data Item':'Affected by', 'Value':'Percent of Colonies Impacted'}, inplace=True)
df = df[df['Affected by']=='Varroa_mites']
df = df[df['Year']==2018]
df = df.groupby(['State'])[['Percent of Colonies Impacted']].mean()
df.reset_index(inplace=True)

state_codes = {
    'District of Columbia' : 'dc','Mississippi': 'MS', 'Oklahoma': 'OK',
    'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR',
    'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA',
    'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ',
    'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT',
    'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT',
    'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV',
    'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI',
    'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND',
    'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY',
    'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH',
    'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD',
    'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA',
    'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX',
    'Nevada': 'NV', 'Maine': 'ME'}

df['state_code'] = df['State'].apply(lambda x : state_codes[x])
print(df)

#--------------------------------------------------------------------------------
# Build the map plot

beemap = px.choropleth(
            data_frame=df,
            locationmode='USA-states',
            locations='state_code',
            scope="usa",
            color='Percent of Colonies Impacted',
            hover_data=['State','Percent of Colonies Impacted'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            title='Bees affected by Varroa Mites 2018',
            template='plotly_dark',
            labels={'Percent of Colonies Impacted':'% of Bee Colonies'}
            )

beemap.update_layout(title={'x':0.5,'xanchor':'center','font':{'size':20}})

beemap.update_traces(hovertemplate=
        "<b>%{customdata[0]}</b><br><br>" +
        "Percent of Colonies Impacted: %{customdata[1]:.3s}" +
        "<extra></extra>",
)
beemap.update_layout(
    annotations=[
        dict(
            x=0.525,
            y=0.09,
            showarrow=False,
            text="TX: 21%",
        ),
        dict(
            x=0.49,
            y=0.47,
            showarrow=False,
            text="KS: 61%",
        ),
        dict(
            x=0.38,
            y=0.49,
            showarrow=False,
            text="CO: 54%",
        ),
        dict(
            x=0.27,
            y=0.75,
            showarrow=False,
            text="ID: 57%",
        ),
        dict(
            x=0.63,
            y=0.4,
            showarrow=False,
            text="TN: 45%",
        ),
        dict(
            x=0.71,
            y=0.7,
            showarrow=True,
            text="NY: 33%",
        ),
        dict(
            x=0.45,
            y=0.64,
            showarrow=True,
            text="NE: 9%",
        ),
        dict(
            x=0.2,
            y=0.47,
            showarrow=False,
            text="CA: 46%",
        ),
        dict(
            x=0.37,
            y=0.1,
            showarrow=True,
            text="HI: 82%",
        ),
        dict(
            x=0.79,
            y=0.09,
            showarrow=False,
            text="FL: 40%",
        ),
    ]
)

pio.show(beemap)
