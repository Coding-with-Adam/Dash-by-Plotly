from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
import os
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Create a .env file and write: OPENAI_API_KEY="insert-your-openai-token"
llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=OPENAI_API_KEY)

# data from https://www.kaggle.com/datasets/nelgiriyewithana/world-stock-prices-daily-updating
df_stocks = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/LangChain/Agents/Pandas-Agent/World-Stock-Prices-Data-small.csv")
df_stocks['Date'] = pd.to_datetime(df_stocks['Date'], utc=True)
df_stocks['Date'] = df_stocks['Date'].dt.date


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = [
    dcc.Markdown("# Pandas Agent in Dash App"),
    dcc.Dropdown(id='stock-picker',
                 options=sorted(df_stocks['Ticker'].unique()),
                 value=['AAPL','TSLA'], multi=True),
    dcc.Graph(id='line-chart', figure={}),
    dcc.Loading(dcc.Markdown(id='answer-space'),
                overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"},
                custom_spinner=html.H2(
                    ["Pandas AI analyzing data", dbc.Spinner(color="danger")])
                )
]


@callback(
    Output('line-chart', 'figure'),
    Input('stock-picker', 'value')
)
def activate_agent(stocks_chosen):
    # Create the figure
    df = df_stocks[df_stocks['Ticker'].isin(stocks_chosen)]
    print(df.head())
    fig = px.line(df, x='Date', y='High', color='Ticker')
    return fig


@callback(
    Output('answer-space', 'children'),
    Input('stock-picker', 'value')
)
def activate_agent(stocks_chosen):
    # Use pandas agent to analyze the dataset
    df = df_stocks[df_stocks['Ticker'].isin(stocks_chosen)]
    agent = create_pandas_dataframe_agent(llm=llm, 
                                          df=df,
                                          max_iterations=2,
                                          verbose=True,
                                          agent_type="tool-calling",
                                          handle_parsing_errors=True)
    response = agent.invoke("What is the dataset telling us about the performance of the stocks? "
                            "Only consider the 'High' and the 'Ticker' columns. "
                            "Please provide a summary at the end.")
    print(response)
    return response["output"]


if __name__ == '__main__':
    app.run_server(debug=True)
