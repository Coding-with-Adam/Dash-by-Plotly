from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import os
import time
import plotly.graph_objects as go
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import find_dotenv, load_dotenv
# pip install kaleido==0.1.0.post1

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)  # load api key

# function for decoding graph image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# incorporate the data
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/LangChain/Graph-Insights/domain-notable-ai-system.csv")
df = df[df.Entity != "Not specified"]
df = df[df['Year'] > 1999]
df = df[df['Entity'].isin(['Multimodal', 'Language'])]

# Build the line chart
line_graph = px.line(df,
                    x='Year',
                    y='Annual number of AI systems by domain',
                    color='Entity',
                    template='plotly_dark')
line_graph.update_layout(legend_title=None)


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.layout = dbc.Container(
    [
        dcc.Markdown("## Domain of notable AI systems, by year of publication\n"
                     "###### Specific field, area, or category in which an AI system is designed to operate or solve problems."),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-graph', figure=line_graph),
                        dcc.Dropdown(id="domain-slct",
                                     multi=True,
                                     options=sorted(df['Entity'].unique()),
                                     value=['Multimodal', 'Language', 'Games']),
                        html.Div("This is a fake dropdown, just here for demo purposes.")
                    ],
                    width=6
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Button(id='btn', children='Insights', className='my-2'), width=1)
            ],
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Spinner(html.Div(id='content', children=''), fullscreen=False), width=6)
            ],
        ),
    ]
)


@callback(
    Output('content','children'),
    Input('btn','n_clicks'),
    State('line-graph','figure'),
    prevent_initial_call=True
)
def graph_insights(_, fig):
    fig_object = go.Figure(fig)
    fig_object.write_image(f"images/fig{_}.png")
    time.sleep(1)

    chat = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=256)
    image_path = f"images/fig{_}.png"
    base64_image = encode_image(image_path)
    result = chat.invoke(
        [
            # Limitations of the model -- https://platform.openai.com/docs/guides/vision/limitations
            # SystemMessage(
            #     content="You are an expert in data visualization that reads images of graphs and describes the data trends in those images. "
            #             "The graphs you will read are line charts that have multiple lines in them. Please pay careful attention to the "
            #             "legend color of each line and match them to the line color in the graph. The legend colors must match the line colors "
            #             "in the graph correctly."
            # ),
            HumanMessage(
                content=[
                    {"type": "text", "text": "What data insight can we get from this graph?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "auto",  # https://platform.openai.com/docs/guides/vision/low-or-high-fidelity-image-understanding
                        },
                    },
                ]
            )
        ]
    )
    return result.content


if __name__ == '__main__':
    app.run_server(debug=True)
