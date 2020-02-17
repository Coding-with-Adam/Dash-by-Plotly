# Environment used: dash1_8_0_env
import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.io as pio
import plotly.graph_objects as go

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Data from http://ghdx.healthdata.org/gbd-results-tool
df = pd.read_csv("suicide-rate-1990-2017.csv")

# print(df[:5])

dict_keys=['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen',
           'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','twentyone','twentytwo',
           'twentythree','twentyfour','twentyfive','twentysix','twentyseven','twentyeight']

years=[1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,
       2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]

n_frame={}

for y, d in zip(years, dict_keys):
    dataframe=df[(df['year']==y)&(df['region']=='Europe')]
    dataframe=dataframe.nlargest(n=5,columns=['suicide rate (deaths per 100,000)'])
    dataframe=dataframe.sort_values(by=['year','suicide rate (deaths per 100,000)'])

    n_frame[d]=dataframe

# print (n_frame)

#-------------------------------------------
fig = go.Figure(
    data=[
        go.Bar(
        x=n_frame['one']['suicide rate (deaths per 100,000)'], y=n_frame['one']['country'],orientation='h',
        text=n_frame['one']['suicide rate (deaths per 100,000)'], texttemplate='%{text:.3s}',
        textfont={'size':18}, textposition='inside', insidetextanchor='middle',
        width=0.9, marker={'color':n_frame['one']['color_code']})
    ],
    layout=go.Layout(
        xaxis=dict(range=[0, 60], autorange=False, title=dict(text='suicide rate (deaths per 100,000)',font=dict(size=18))),
        yaxis=dict(range=[-0.5, 5.5], autorange=False,tickfont=dict(size=14)),
        title=dict(text='Suicide Rates per Country: 1990',font=dict(size=28),x=0.5,xanchor='center'),
        # Add button
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          # https://github.com/plotly/plotly.js/blob/master/src/plots/animation_attributes.js
                          args=[None,
                          {"frame": {"duration": 1000, "redraw": True},
                          "transition": {"duration":250,
                          "easing": "linear"}}]
            )]
        )]
    ),
    frames=[
            go.Frame(
                data=[
                        go.Bar(x=value['suicide rate (deaths per 100,000)'], y=value['country'],
                        orientation='h',text=value['suicide rate (deaths per 100,000)'],
                        marker={'color':value['color_code']})
                    ],
                layout=go.Layout(
                        xaxis=dict(range=[0, 60], autorange=False),
                        yaxis=dict(range=[-0.5, 5.5], autorange=False,tickfont=dict(size=14)),
                        title=dict(text='Suicide Rates per Country: '+str(value['year'].values[0]),
                        font=dict(size=28))
                    )
            )
        for key, value in n_frame.items()
    ]
)

#-------------------------------------------
pio.show(fig)
