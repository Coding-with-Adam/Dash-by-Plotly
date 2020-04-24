import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) #pip install plotly==4.5.4
import plotly.express as px
import plotly.io as pio

df = pd.read_csv("final_covid.csv")
df.dropna(subset=['women'], inplace=True)
df['total_employed'] = pd.to_numeric(df['total_employed'])
df['total_employed'] = df['total_employed']*1000


scatterplot = px.scatter(
    data_frame=df,
    x="proximity",
    y="exposure",
    size="total_employed",
    color="Majority Employed",
    opacity=0.8,
    color_discrete_map={"Women":"red","Men":"greenyellow"},
    custom_data=['occupation'],

    marginal_x='box',
    marginal_y='box',

    labels={"exposure":"Exposed to Diseases",
    "proximity":"Physical proximity to others"},
    title='Workers at Highest Risk of Coronavirus',
    # height=800,
    template='ggplot2',     # 'ggplot2','plotly_dark'
)

scatterplot.update_traces(hovertemplate=
        "<b>%{customdata}</b><br><br>" +
        "Exposure: %{y}<br>" +
        "Proximity: %{x}<br>" +
        "Total Employed: %{marker.size:,}" +
        "<extra></extra>",
)

scatterplot.data[5].hovertemplate = "<br>%{y}<br><extra></extra>"
scatterplot.update_layout(legend=dict(x=.8, y=1))
scatterplot.write_html("covidwomen.html")
pio.show(scatterplot)
