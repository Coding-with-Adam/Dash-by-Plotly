import os
from dash import Dash, html, dcc, callback, Input, Output, State
from embedchain import App
# pip install -r requirements.txt

# Create a bot instance
os.environ["OPENAI_API_KEY"] = "my-access-token-here"
ai_bot = App.from_config(config_path="config.yaml")

# Embed resources: websites, PDFs, videos
ai_bot.add("https://nycaudubon.org/our-work/conservation/project-safe-flight")
# ai_bot.add("https://www.wildbirdfund.org/page-sitemap.xml", data_type="sitemap")
# ai_bot.add("Birds Flying Into Windows.pdf", data_type='pdf_file')
# ai_bot.add("https://www.youtube.com/watch?v=l8LDTRxc0Bc")

app = Dash()
app.layout = html.Div([
    html.H1('Learn to Keep Birds safe'),
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
