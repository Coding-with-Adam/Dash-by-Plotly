# import the libraries----------------------------------------------------
import plotly.express as px
import pandas as pd

# read, clean, and filter the data----------------------------------------
# data source: https://mappingpoliceviolence.org/aboutthedata
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/DPhi%20Presentation/MPVDataset.csv")

df = df[df["State"].isin(['NY', 'CA', 'TX'])]
df = df[df["Victim's race"].isin(["White", "Black", "Hispanic", "Asian"])]
df["Victim's age"] = pd.to_numeric(df["Victim's age"], errors='coerce')

df = df.groupby(["Victim's race"])[["Victim's age"]].mean()

# df['date'] = pd.to_datetime(df['Date of Incident (month/day/year)']).dt.year
# df = df.groupby(['date', "Victim's race"])[["Victim's age"]].mean()

# df = df.groupby(["Victim's race", "State"])[["Victim's age"]].mean()

df = df.reset_index()


# build the graph---------------------------------------------------------
fig = px.bar(
    data_frame=df,
    x="Victim's race",
    y="Victim's age",
#     animation_frame="date",
#     range_y=[0,45],
#     facet_col="State"

)

fig.show()
