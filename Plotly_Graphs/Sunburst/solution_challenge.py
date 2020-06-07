import plotly.express as px
import pandas as pd

df = pd.read_csv("MPVDataset.csv")
df = df[df["State"].isin(['AL', 'OR', 'SC'])]
df = df[df["Victim's race"].isin(["White", "Black", "Hispanic", "Asian"])]


fig = px.sunburst(
    data_frame=df,
    path=["State", "Unarmed", "Victim's gender"],
    color="Victim's gender",
    color_discrete_map={'Male':'purple', 'Female':'greenyellow'},
    # hover_data={"Victim's gender": False, "id":False, "labels":False},  # (Plotly version 4.8.0 or higher)
)

fig.update_traces(textinfo='label+percent parent')
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

fig.show()
