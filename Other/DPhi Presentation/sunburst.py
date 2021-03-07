# import the libraries
import plotly.express as px
import pandas as pd
import numpy as np

# read, clean, and filter the data----------------------------------------
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/DPhi%20Presentation/MPVDataset.csv")

df = df[df["State"].isin(['NY', 'CA', 'TX'])]
df = df[df["Victim's race"].isin(["White", "Black", "Hispanic", "Asian"])]
df["Victim's age"] = pd.to_numeric(df["Victim's age"], errors='coerce').fillna(0).astype(np.int64)

# build the graph---------------------------------------------------------
fig = px.sunburst(
    data_frame=df,
    path=["Weapon", 'State', "Victim's race"],  # Root, branches, leaves
    color="Weapon",
    # color="Victim's age",
    # title="7-year Breakdown of Deaths by Police",
    # template='ggplot2',               # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
    #                                   # 'plotly_white', 'plotly_dark', 'presentation',
    #                                   # 'xgridoff', 'ygridoff', 'gridon', 'none'
)

fig.show()