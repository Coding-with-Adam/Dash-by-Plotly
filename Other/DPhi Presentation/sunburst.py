import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/DPhi%20Presentation/MPVDataset.csv")

df = df[df["State"].isin(['NY', 'CA', 'TX'])]
df = df[df["Victim's race"].isin(["White", "Black", "Hispanic", "Asian"])]
# df["Victim's age"] = pd.to_numeric(df["Victim's age"], errors='coerce').fillna(0).astype(np.int64)

fig = px.sunburst(
    data_frame=df,
    path=["Weapon", 'State', "Victim's race"],  # Root, branches, leaves
    # color="Weapon",
    color="Victim's age",
)

fig.show()