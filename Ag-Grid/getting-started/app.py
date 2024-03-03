import dash_ag_grid as dag
from dash import Dash
import pandas as pd

# df = pd.read_csv("space-mission-data.csv") # if your excel sheet is located in your computer

# Incorporat data from excel sheet on Google Drive
url = 'https://drive.google.com/file/d/1OPxHt2VimBAa4YXoLpSL7lHIJdR45XbU/view?usp=sharing' # replace this with your own link
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)

app = Dash(__name__)
app.layout = dag.AgGrid(
    rowData=df.to_dict("records"),
    columnDefs=[{"field": i} for i in df.columns],
)

if __name__ == "__main__":
    app.run_server(debug=True)
