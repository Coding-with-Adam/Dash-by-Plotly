import plotly.express as px
import pandas as pd

# Data src:  https://www.kaggle.com/manohar676/hotel-reviews-segmentation-recommended-system
# Credit to: Manohar Reddy
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Plotly_Graphs/Radar-chart/ExistingHotels_CustomerVisitsdata-1554810038262.csv")
df = df[df['Hotelid'].isin(['hotel_101','hotel_102','hotel_103'])]
print(df.iloc[:20, :8])

df = df.groupby('Hotelid')[['Cleanliness_rating', 'Service_rating', 'Value_rating',
                            'Rooms_rating','Checkin_rating',
                            'Businessservice_rating']].mean().reset_index()
print(df)

# Convert from wide data to long data to plot radar chart
df = pd.melt(df, id_vars=['Hotelid'], var_name='category', value_name='rating',
             value_vars=['Cleanliness_rating', 'Service_rating', 'Value_rating',
                         'Rooms_rating','Checkin_rating','Businessservice_rating'],
)
print(df)

# radar chart Plotly examples - https://plotly.com/python/radar-chart/
# radar chart Plotly docs = https://plotly.com/python-api-reference/generated/plotly.express.line_polar.html#plotly.express.line_polar
fig = px.line_polar(df, r='rating', theta='category', color='Hotelid', line_close=True,
                            line_shape='linear',  # or spline
                    hover_name='Hotelid',
                    hover_data={'Hotelid':False},
                    markers=True,
                    # labels={'rating':'stars'},
                    # text='Hotelid',
                    # range_r=[0,10],
                    direction='clockwise',  # or counterclockwise
                    start_angle=45
                    )
# fig.update_traces(fill='toself')
fig.show()
