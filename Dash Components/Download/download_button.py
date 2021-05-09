import dash
from dash.dependencies import Output, Input
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd

FONT_AWESOME = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

external_stylesheets = [dbc.themes.BOOTSTRAP, FONT_AWESOME]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = dbc.Container(
    [
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        ),

        dbc.Button(id='btn',
            children=[html.I(className="fa fa-download mr-1"), "Download"],
            color="info",
            className="mt-1"
        ),

        dcc.Download(id="download-component"),
    ],
    className='m-4'
)


@app.callback(
    Output("download-component", "data"),
    Input("btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dict(content="Always remember, we're better together.", filename="hello.txt")
    # return dcc.send_data_frame(df.to_csv, "mydf_csv.csv")
    # return dcc.send_data_frame(df.to_excel, "mydf_excel.xlsx", sheet_name="Sheet_name_1")
    # return dcc.send_file("./assets/data_file.txt")
    # return dcc.send_file("./assets/bees-by-Lisa-from-Pexels.jpg")


if __name__ == "__main__":
    app.run_server(debug=True)
