import plotly.express as px
import pandas as pd

# Data src:  https://llewellynjean.shinyapps.io/NBARefDatabase/
# Credit to: https://twitter.com/owenlhjphillips
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Plotly_Graphs/Radar-chart/NBA_Referee_Stats.csv")
df = df[df['Season']=='2016-17']
df = df[df['Season type']=='Regular Season']
df = df.iloc[:4, :19]

# Convert from wide data to long data to plot radar chart
df = pd.melt(df, id_vars=['Referee'], var_name='foul', value_name='stats',
             value_vars=['Kicked ball', 'Technical', 'Shooting block'],
)
print(df)

# radar chart Plotly examples - https://plotly.com/python/radar-chart/
# radar chart Plotly docs = https://plotly.com/python-api-reference/generated/plotly.express.line_polar.html#plotly.express.line_polar
fig = px.line_polar(df, r='stats', theta='foul', color='Referee', line_close=True,
                    hover_name='Referee',
                    range_r=[5,25]
                    )
fig.show()
