# Environment: dash1_8_0_env
import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# http://ghdx.healthdata.org/gbd-results-tool
df = pd.read_csv("suicide-rates-age.csv")
dff= df.groupby(['Year'], as_index=False)['70+','50-69yo','5-14yo','15-49yo'].mean()

dff = dff.T.reset_index()
dff.columns = dff.iloc[0]
dff=dff.drop(dff.index[0]).rename(columns={'Year':'age_group'})

dff['color_code'] = ['#FA8072','#00FFFF','#a367db','#33FF8A']

dff['age_group'] = pd.Categorical(dff['age_group'], ['5-14yo','15-49yo','50-69yo','70+'])
dff.sort_values("age_group", inplace=True)


years=[1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,
       2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]


#------------------------------------------------------
# https://github.com/plotly/plotly.js/blob/master/src/plots/animation_attributes.js
fig = go.Figure(
    data=[go.Bar(x=dff[suicide_avg], y=dff['age_group'],orientation='h',
                 text=dff[suicide_avg], texttemplate='%{text:.3s}',
                 textfont={'size':18}, textposition='inside', insidetextanchor='middle',
                 width=0.9, marker={'color':dff['color_code']})

        for suicide_avg in years if suicide_avg==1990
    ],
    layout=go.Layout(
        xaxis=dict(range=[0, 40], autorange=False, title=dict(text='Global suicide rate (deaths per 100,000)', font=dict(size=18))),
        yaxis=dict(range=[-0.5, 4.5], autorange=False, tickfont=dict(size=16)),
        title=dict(text='Suicide Rates per Age Group: 1990',font=dict(size=28),x=0.5,xanchor='center'),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None,
                          {"frame": {"duration": 1000, "redraw": True},
                          "transition": {"duration":250,
                          "easing": "circle-in-out"}}]
            )]
        )]
    ),
    frames=[
            go.Frame(data=[
                        go.Bar(x=dff[suicide_avg], y=dff['age_group'],
                        orientation='h',text=dff[suicide_avg],
                        marker={'color':dff['color_code']})
                    ],
                    layout=go.Layout(
                                xaxis=dict(range=[0, 40], autorange=False),
                                yaxis=dict(range=[-0.5, 4.5], autorange=False,tickfont=dict(size=16)),
                                title=dict(text='Suicide Rates per Age Group: '+str(suicide_avg),font=dict(size=28)),
                        )
                    )

            for suicide_avg in years
    ]
)

pio.show(fig)
