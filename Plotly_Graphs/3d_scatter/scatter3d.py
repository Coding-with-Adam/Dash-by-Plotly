import pandas as pd  # (version 1.0.0)
import plotly.express as px  # (version 4.7.0)
import plotly.io as pio
import numpy as np
import plotly.graph_objects as go

# Use for animation rotation at the end
x_eye = -1.25
y_eye = 2
z_eye = 0.5

df = pd.read_csv('female_labour_cleaned.csv')
df = df[df['Year'].isin(['2010'])]
df = df[df['Continent'].isin(['Africa', 'Europe'])]

# df = df[df['Year'].isin(['1990','1995','2000','2005','2010'])]
df['resized_pop'] = df['population'] / 100000000  # use for size parameter

fig = px.scatter_3d(
    data_frame=df,
    x='GDP per capita',
    y='% Econ. active',
    z='Years in school (avg)',
    color="Continent",
    color_discrete_sequence=['magenta', 'green'],
    # color_discrete_map={'Europe': 'black', 'Africa': 'yellow'},
    # opacity=0.3,              # opacity values range from 0 to 1
    # symbol='Year',            # symbol used for bubble
    # symbol_map={"2005": "square-open", "2010": 3},
    # size='resized_pop',       # size of bubble
    # size_max=50,              # set the maximum mark size when using size
    log_x=True,  # you can also set log_y and log_z as a log scale
    # range_z=[9,13],           # you can also set range of range_y and range_x
    template='ggplot2',         # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                # 'plotly_white', 'plotly_dark', 'presentation',
                                # 'xgridoff', 'ygridoff', 'gridon', 'none'
    title='Female Labor Force Participation Analysis',
    labels={'Years in school (avg)': 'Years Women are in School'},
    # hover_data={'Continent': False, 'GDP per capita': ':.1f'},
    hover_name='Entity',        # values appear in bold in the hover tooltip
    height=700,                 # height of graph in pixels

    # animation_frame='Year',   # assign marks to animation frames
    # range_x=[500,100000],
    # range_z=[0,14],
    # range_y=[5,100]

)

# fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
# fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

# Use for animation rotation
# fig.update_layout(scene_camera_eye=dict(x=x_eye, y=y_eye, z=z_eye),
#                   updatemenus=[dict(type='buttons',
#                                     showactive=False,
#                                     y=1,
#                                     x=0.8,
#                                     xanchor='left',
#                                     yanchor='bottom',
#                                     pad=dict(t=45, r=10),
#                                     buttons=[dict(label='Play',
#                                                   method='animate',
#                                                   args=[None, dict(frame=dict(duration=250, redraw=True),
#                                                                    transition=dict(duration=0),
#                                                                    fromcurrent=True,
#                                                                    mode='immediate'
#                                                                    )]
#                                                   )
#                                              ]
#                                     )
#                                ]
#                   )
#
#
# def rotate_z(x, y, z, theta):
#     w = x + 1j * y
#     return np.real(np.exp(1j * theta) * w), np.imag(np.exp(1j * theta) * w), z
#
#
# frames = []
#
# for t in np.arange(0, 6.26, 0.1):
#     xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
#     frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xe, y=ye, z=ze))))
# fig.frames = frames
#
#
# fig.write_html("My3dPlot.html")
pio.show(fig)
