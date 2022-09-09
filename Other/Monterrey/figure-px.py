import plotly.express as px
import pandas as pd

# https://www.kaggle.com/datasets/tsarina/mexico-city-airbnb?select=listings1.csv
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Monterrey/airbnb.csv")


fig = px.scatter_mapbox(data_frame=df, lat="latitude", lon="longitude", color='price', height=600,
                        color_continuous_scale=px.colors.sequential.Sunset,
                        range_color=[0, 1000], zoom=11,
                        hover_data={'latitude':False, 'longitude':False, 'room_type':True,
                                    'minimum_nights':True})
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

