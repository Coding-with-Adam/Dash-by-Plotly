import plotly.express as px
import pandas as pd

# Data put together by Gabe Salzer on data.world
# Data source: http://www.landofbasketball.com/nba_teams_year_by_year.htm
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Plotly_Graphs/Heatmaps/Historical%20NBA%20Performance.csv")
df = df.pivot('Team','Year','Winning Percentage')
print(df[:10])

df = df[df.index.isin(['Warriors', 'Knicks', 'Celtics', 'Bulls', '76ers'])]
fig = px.imshow(df, color_continuous_scale=px.colors.sequential.YlOrBr,
                title="NBA Season Winning Percentage")
fig.update_layout(title_font={'size':27}, title_x=0.5)
fig.update_traces(hoverongaps=False,
                  hovertemplate="Team: %{y}"
                                "<br>Year: %{x}"
                                "<br>Winning %: %{z}<extra></extra>"
                  )
fig.show()
