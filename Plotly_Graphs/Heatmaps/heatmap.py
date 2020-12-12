import plotly.express as px
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Plotly_Graphs/Heatmaps/Berlin_crimes.csv")
df = df.groupby(['District'])[
    ['Graffiti','Robbery', 'Agg_assault', 'Burglary']].median().reset_index()
print(df[:15])
df = pd.melt(df, id_vars=['District'], value_vars=['Graffiti', 'Robbery', 'Agg_assault', 'Burglary'],
             var_name='Crime')
print(df[:15])
df = df.pivot('Crime','District','value')
print(df)

# https://plotly.com/python/builtin-colorscales/)
fig = px.imshow(df,color_continuous_scale=px.colors.sequential.Plasma,
                title="Berlin Crime Distribution")
fig.update_layout(title_font={'size':27}, title_x=0.5)
fig.update_traces(hoverongaps=False,
                  hovertemplate="District: %{y}"
                                "<br>Crime: %{x}"
                                "<br>Cases: %{z}<extra></extra>"
                  )
fig.show()


# df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Plotly_Graphs/Heatmaps/Berlin_crimes.csv")
# df = df.groupby(['District'])[
#     ['Graffiti','Robbery', 'Agg_assault', 'Burglary']].median().reset_index()
# data = df[['Graffiti', 'Robbery', 'Agg_assault', 'Burglary']].values.tolist()
# print(data)
# # reshape the list of lists to swap y,x axes in graph
# # data=[list(i) for i in zip(*data)]
# # print(data)
# 
# fig = px.imshow(data,
#                 labels=dict(x="Crime Type", y="District", color="Median Crime"),
#                 x=['Graffiti', 'Robbery', 'Agg_assault', 'Burglary'],
#                 y=df['District'],
#                 color_continuous_scale=px.colors.sequential.Plasma
#                )
# fig.show()
