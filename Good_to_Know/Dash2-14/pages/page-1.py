import pandas as pd
from dash import register_page, html, dcc
import plotly.express as px

register_page(__name__, "/page-1")

translations = {
    "en": {
        "title": "Our first page",
        "subtitle": "This is the First page.",
    },
    "fr": {
        "title": "Notre première page",
        "subtitle": "Ceci est la première page.",
    }
}

def layout(stored_data, language_chosen):
    fig = px.scatter(stored_data, x="sepal_width", y="sepal_length")

    return [
        html.H1(translations[language_chosen]["title"]),
        html.H2(translations[language_chosen]["subtitle"]),
        dcc.Graph(figure=fig)
    ]
