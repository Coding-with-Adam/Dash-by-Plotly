import os
import openai  # pip install openai
from dash import Dash,dcc, html, Input, Output, State  # pip install dash
import dash_bootstrap_components as dbc                # pip install dash-bootstrap-components

openai.api_key = "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"

# Initialize the ChatGPT model
model_options = ['text-davinci-003','text-curie-001', 'text-babbage-001', 'text-ada-001', 'text-davinci-002', 'text-davinci-001']

# Instantiate the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Dash-ChatGPT Example"),

    dbc.Row([
        dbc.Col([
            html.Label("Model:"),
            dcc.Dropdown(model_options, value="text-davinci-003", id='models'),
        ],width=6),
        dbc.Col([
            html.Label("Temperature:"),
            dcc.Slider(min=0, max=2, step=0.1, value=0.7, id='temperatures'),
        ], width=6)
    ], className='mb-5'),

    dbc.Row([
        dbc.Col([
            dcc.Input(id='input-text', type='text',
                      placeholder='Type your message here',
                      style={'width': 500}),
            html.Button('Submit', id='submit-button', n_clicks=0),

        ],width=6)
    ], justify="center"),

    dcc.Loading(
        children=[
            html.Div(id='output-text')
        ],
        type="circle",
    )
])

# Define the callback function
@app.callback(
    Output('output-text', 'children'),
    Input('submit-button', 'n_clicks'),
    State('input-text', 'value'),
    State('models', 'value'),
    State('temperatures', 'value')
)
def update_output(n_clicks, text_input, model_input, temp_input):
    if n_clicks >0:
        # Get the response from ChatGPT
        response = openai.Completion.create(
            model=model_input,
            prompt=f"{text_input}\n",
            # The maximum number of tokens to generate in the completion.
            max_tokens=400,
            # temperature to use between 0 and 2. Higher values like 0.8 will make the output more random,
            # while lower values like 0.2 will make it more focused and deterministic.
            temperature=temp_input
        )

        # Extract the generated text from the response
        generated_text = response.choices[0].text

        # Return the generated text as the output
        return generated_text

if __name__ == '__main__':
  app.run_server(debug=True)
