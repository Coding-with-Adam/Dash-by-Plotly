# https://pola-rs.github.io/polars/py-polars/html/reference/dataframe/api/polars.DataFrame.columns.html#polars.DataFrame.columns
# https://pola-rs.github.io/polars-book/user-guide/quickstart/quick-exploration-guide.html
# https://pola-rs.github.io/polars/py-polars/html/reference/lazyframe/index.html
# https://towardsdatascience.com/pandas-vs-polars-a-syntax-and-speed-comparison-5aa54e27497e
# https://towardsdatascience.com/understanding-lazy-evaluation-in-polars-b85ccb864d0c
# https://towardsdatascience.com/visualizing-polars-dataframes-using-plotly-express-8da4357d2ee0

from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import polars as pl
import pandas as pd
import time
import plotly.express as px
from datetime import datetime, date

# READ DATA: FS_sp500_Value.csv--------------------------------------------
# data source - https://www.kaggle.com/datasets/hanseopark/sp-500-stocks-value-with-financial-statement?resource=download

start = time.time()  # Pandas
df_pandas = pd.read_csv('FS_sp500_Value.csv')
end = time.time()
pd_read = round(end - start, 3)

start = time.time()  # Polars
df_polars = pl.read_csv('FS_sp500_Value.csv')
end = time.time()
pl_read = round(end - start,3)
compare_read_data = (pd_read / pl_read) * 100


# # Make polars even faster with lazyload
# # Polars - get unique ticker values to create dropdown options
# start = time.time()
# q1 = (
#     pl.scan_csv("FS_sp500_Value.csv")
#     .lazy()
#     .select(pl.col('Ticker')).unique()
# )
# dropdown_pl = dcc.Dropdown(q1.collect().to_series().to_list(), value='ACN')
# end = time.time()
# pl_read = round(end - start,3)
# print(pl_read)
#
# # Pandas - get unique ticker values to create dropdown options
# start = time.time()
# df_pandas = pd.read_csv('FS_sp500_Value.csv')
# ticker_values = df_pandas['Ticker'].unique()
# dropdown_pd = dcc.Dropdown(ticker_values, value='ACN')
# end = time.time()
# pd_read = round(end - start, 3)
# print(pd_read)
# compare_read_data = (pd_read / pl_read) * 100
# print(f"polars is {round(compare_read_data)}% faster than pandas")
# exit()


app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
app.layout = dbc.Container([
    html.H1('Compare Dash App with Pandas vs Polars', style={'textAlign': 'center'}),
    html.Div(f"Reading data with polars: {pl_read}"),
    html.Div(f"Reading data with pandas: {pd_read}"),
    html.Div(f"polars is {round(compare_read_data)}% faster than pandas", className='mb-5'),

    dbc.Row([
        dbc.Col([
            html.Div(id='polars_dates'),
            html.Div(id='pandas_dates'),
            html.Div(id='dates_compare')
        ], width=3),

        dbc.Col([
            dcc.DatePickerRange(
                id='date_chosen',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2017, 9, 19),
                initial_visible_month=date(2017, 8, 5),
                start_date=date(2011, 1, 25),
                end_date=date(2017, 8, 25)
            ),
        ], width=3)
    ], className='mb-3'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='datechart_pd')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='datechart_pl')
        ], width=6),
    ], className='mb-3'),


    dbc.Row([
            dbc.Col([
                html.Div(id='polars_new_col'),
                html.Div(id='pandas_new_col'),
                html.Div(id='new_col_compare')
            ], width=3),

            dbc.Col([
                dcc.Dropdown(['High','Low','Open','Close'], value='High', id='my_dpdn')
            ], width=3)
        ], className='mb-3'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='chart_pd')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='chart_pl')
        ], width=6),
    ]),

])


@callback(
    Output('datechart_pd', 'figure'),
    Output('datechart_pl', 'figure'),
    Output('polars_dates', 'children'),
    Output('pandas_dates', 'children'),
    Output('dates_compare', 'children'),
    Input('date_chosen', 'start_date'),
    Input('date_chosen', 'end_date')
)
def line_chart_date(start_d, end_d):
    date_start = datetime.strptime(start_d, '%Y-%m-%d')
    date_end = datetime.strptime(end_d, '%Y-%m-%d')

    # PANDAS date filtering
    start = time.time()
    df_pandas['Date'] = pd.to_datetime(df_pandas['Date'])
    mask = (df_pandas['Date'] > date_start) & (df_pandas['Date'] <= date_end)
    pd_filtered = df_pandas.loc[mask]
    pd_filtered = pd_filtered[pd_filtered['Ticker']=='ACN']
    end = time.time()
    data_sliced_pd = end - start

    fig_pd = px.line(pd_filtered, x='Date', y='High')

    # POLARS date filtering
    start = time.time()
    pl_filtered = df_polars.filter(
        pl.col("Date").is_between(date_start,date_end),
    )
    pl_filtered = pl_filtered.filter(pl.col('Ticker') == 'ACN')
    end = time.time()
    data_sliced_pl = end - start

    fig_pl = px.line(x=pl_filtered.select('Date').to_series(), y=pl_filtered.select('High').to_series())


    comparison = (data_sliced_pd / data_sliced_pl) *100
    return fig_pd, \
           fig_pl, \
           f"Data sliced with polars: {round(data_sliced_pl, 3)}", \
           f"Data sliced with pandas: {round(data_sliced_pd, 3)}", \
           f"polars is {round(comparison)}% faster than pandas"


@callback(
    Output('chart_pd', 'figure'),
    Output('chart_pl', 'figure'),
    Output('polars_new_col', 'children'),
    Output('pandas_new_col', 'children'),
    Output('new_col_compare', 'children'),
    Input('my_dpdn', 'value')
)
def line_chart_date(value):
    # PANDAS create new column
    start = time.time()
    df_pandas['price'] = df_pandas[value] * df_pandas['Volume']
    end = time.time()
    data_sliced_pd = end - start

    pd_filtered = df_pandas[df_pandas['Ticker'] == 'ACN']
    fig_pd = px.histogram(pd_filtered, x='price')

    # POLARS create new column
    start = time.time()
    df_pl = df_polars.with_columns([(pl.col(value) * pl.col('Volume')).alias("price")])
    end = time.time()
    data_sliced_pl = end - start

    pl_filtered = df_pl.filter(pl.col('Ticker') == 'ACN')
    fig_pl = px.histogram(x=pl_filtered.select('price').to_series())

    print(data_sliced_pd)
    print(data_sliced_pl)
    comparison = (data_sliced_pd / data_sliced_pl) *100
    return fig_pd, \
           fig_pl, \
           f"Data sliced with polars: {round(data_sliced_pl, 3)}", \
           f"Data sliced with pandas: {round(data_sliced_pd, 3)}", \
           f"polars is {round(comparison)}% faster than pandas"


if __name__=='__main__':
    app.run_server(debug=True)
