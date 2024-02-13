from dash import Dash, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Dash_Interactive_Graphs/domain-notable-ai-system.csv")
df = df[df.Entity != "Not specified"]


app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
app.layout = dbc.Container(
    [
        dcc.Markdown("## Domain of notable artificial intelligence systems, by year of publication\n"
                     "###### Specific field, area, or category in which an AI system is designed to operate or solve problems."),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(id='domain-graph'),
                            dcc.Dropdown(id="year-slct",
                                         options=df['Year'].unique(),
                                         value='2020')
                        ]),
                        className="my-3"
                    ),
                    width=6
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(id='line-graph'),
                            dcc.Dropdown(id="domain-slct",
                                         multi=True,
                                         options=sorted(df['Entity'].unique()),
                                         value=['Multimodal', 'Language'])
                        ]),
                        className="my-3"
                    ),
                    width=6
                ),
            ]
        )
    ]
)


@callback(
    Output("domain-graph", "figure"),
    Input("year-slct", "value"),
)
def update_pie_chart(year_chosen):
    year_chosen = int(year_chosen)
    df_dom_filtrd = df[df['Year'] == year_chosen]
    pie_chart = px.pie(df_dom_filtrd, names='Entity', values='Annual number of AI systems by domain')
    return pie_chart


@callback(
    Output("line-graph", "figure"),
    Input("domain-slct", "value"),
)
def update_line_graph(domains_chosen):
    print(domains_chosen)
    df_filtrd = df[df['Year']>1999]
    df_filtrd = df_filtrd[df_filtrd['Entity'].isin(domains_chosen)]
    line_graph = px.line(df_filtrd, x='Year', y='Annual number of AI systems by domain', color='Entity')
    return line_graph


if __name__ == "__main__":
    app.run(debug=True)
