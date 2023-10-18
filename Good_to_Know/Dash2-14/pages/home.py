from dash import register_page, html, callback, Input, Output

register_page(__name__, "/")

translations = {
    "en": {
        "title": "Hello world",
        "subtitle": "This is the home page.",
    },
    "fr": {
        "title": "Bonjour le monde",
        "subtitle": "Ceci est la page d'accueil.",
    }
}

def layout(stored_data, language_chosen):
    return [
        html.H1(translations[language_chosen]["title"]),
        html.H2(translations[language_chosen]["subtitle"]),
    ]
