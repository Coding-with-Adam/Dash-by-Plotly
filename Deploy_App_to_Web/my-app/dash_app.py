from dash import Dash, dcc   # pip install dash
import dash_ag_grid as dag   # pip install dash-ag-grid
import plotly.express as px
import pandas as pd          # pip install pandas

df = pd.read_csv('space-mission-data.csv')

app = Dash()
app.layout = [
    dag.AgGrid(
        rowData=df.to_dict("records"),
        columnDefs=[{"field": i} for i in df.columns],
    ),
    dcc.Graph(figure=px.histogram(df, x='price'))
]

if __name__ == '__main__':
    app.run(debug=True)
