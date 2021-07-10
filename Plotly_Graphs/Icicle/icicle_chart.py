import pandas as pd
import plotly.express as px  # Plotly version >= 5.0

# data from: https://data.virginia.gov/Education/Bills-of-Sale-of-Enslaved-Individuals-1718-1862-/j2xt-sjy7
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Plotly_Graphs/Icicle/Bills_of_Sale_of_Enslaved_Individuals__1718-1862.csv")
print(df.head()[['Period', 'Locality']])

fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality'],
                values='Slaves')

# fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality'],
#                 values='Slaves', color='Locality')

# fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality', 'Gender'],
#                 values='Slaves', color='Gender')

# fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality', 'Enslaver_Buyer'],
#                 values='Slaves')

# fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality', 'Enslaver_Buyer'],
#                 values='Slaves', color='Age')

# fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality', 'Enslaver_Buyer'],
#                 values='Slaves', color='Age', color_continuous_scale='RdBu')

# fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality'],
#                 values='Slaves', color='Locality')
# fig.update_traces(root_color="lightgrey", tiling=dict(orientation='h', flip='x'))

# fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality'],
#                 values='Slaves', color='Locality')
# fig.update_traces(root_color="lightgrey", tiling=dict(orientation='v', flip='y'))

# fig = px.icicle(df, path=[px.Constant("all"), 'Period', 'Locality'],
#                 values='Slaves', maxdepth=2)
fig.update_traces(root_color="lightgrey", tiling=dict(orientation='h'))

fig.show()
