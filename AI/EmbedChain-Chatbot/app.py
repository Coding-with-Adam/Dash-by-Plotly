import os
from dash import Dash, html, dcc, callback, Input, Output, State
from embedchain import App
# pip install -r requirements.txt

# Create a bot instance
os.environ["OPENAI_API_KEY"] = "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"
ai_bot = App.from_config(config_path="config.yaml")

# Embed resources: websites, PDFs, videos
ai_bot.add("https://www.wildbirdfund.org/page-sitemap.xml", data_type="sitemap")
# ai_bot.add("https://nycaudubon.org/our-work/conservation/project-safe-flight")
# ai_bot.add("Birds Flying Into Windows.pdf", data_type='pdf_file')
# ai_bot.add("https://www.youtube.com/watch?v=l8LDTRxc0Bc")

app = Dash()
app.layout = html.Div([
    html.H1('WILD BIRD FUND'),
    html.H3('This AI Chatbot was trained on the wildbirdfund website. It was built to help people understand how to keep city birds '
            'safe and take care of them when injured.'),
    html.Label('Ask your question:'),
    html.Br(),
    dcc.Textarea(id='question-area', value=None, style={'width': '25%', 'height': 100}),
    html.Br(),
    html.Button(id='submit-btn', children='Submit'),
    dcc.Loading(id="load", children=html.Div(id='response-area', children='')),
])

@callback(
    Output('response-area', 'children'),
    Input('submit-btn', 'n_clicks'),
    State('question-area', 'value'),
    prevent_initial_call=True
)
def create_response(_, question):
    # What kind of glass should I use to keep birds safe from window collisions?
    answer = ai_bot.query(question)
    return answer


if __name__ == '__main__':
    app.run_server(debug=False)
