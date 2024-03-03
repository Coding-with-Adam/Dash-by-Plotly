import micropip
await micropip.install("dash_ag_grid")
await micropip.install("dash-mantine-components")
await micropip.install("urllib3")
await micropip.install('openpyxl')


import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import dash_ag_grid as dag
import dash_mantine_components as dmc
import base64
def create_onedrive_directdownload (onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    print(resultUrl)
    return resultUrl

url = create_onedrive_directdownload("https://1drv.ms/x/s!AoKPiuofdvp_ltlppz8OsI8UmSVP1w?e=UVI006")
print(url)
df = pd.read_excel(url, engine='openpyxl')
print(df)

app = Dash(__name__)

app.layout = html.Div([
    dmc.Alert(
    "Hi from Dash Mantine Components. You can create some great looking dashboards using me!",
    title="Welcome!",
    color="violet"),
    dag.AgGrid(
        id="grid",
        rowData=df.to_dict("records"),
        columnDefs=[{"field": i} for i in df.columns],
        defaultColDef={"filter": True},
        columnSize="sizeToFit",
    ),
    dcc.Graph(figure=px.histogram(df, x=df.columns[1]))
])

if __name__ == '__main__':
    app.run(debug=True)
