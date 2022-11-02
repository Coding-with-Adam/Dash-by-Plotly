import plotly.express as px
import pandas as pd
# Graphing docs - https://plotly.com/python/
# High level - https://plotly.com/python-api-reference/plotly.express.html
# https://plotly.com/python/reference/index/

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/salaries-ai-jobs-net.csv')
df = df[df.salary < 251000]


fig = px.histogram(data_frame=df, x="salary", nbins=20, color='experience_level', barmode='group')
fig = px.histogram(df, x="salary", nbins=20, facet_col='experience_level')

# fig = px.histogram(df, x="salary", nbins=20, color='experience_level', barmode='group')
# fig.update_traces(showlegend=False)

# fig.update_traces(marker_opacity=0.6)

# fig.update_layout(hoverlabel_font_size=20)

fig.show()



