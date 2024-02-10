"""
In the last exercise, you (the app developer) controled the model temperature. Let's give our app user the ability to control the temperature.
Exercise 3: Modify the app so that the app user can choose a number from 0 to 2. This number will represent the model temperature.
            A - fill in the State arguments in the callback decorator
            B - add the second argument in the callback function that points to the temperature value chosen
            C - add the temperature parameter inside the ChatOpenAI model
**Solution** can be found in -- https://charming-data.circle.so/c/langchain-education/quickstart-llm-chain            
"""
from dash import Dash, html, dcc, Input, Output, State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI

# activate api key
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Initialize the Dash app
app = Dash()
# Define the layout of the app
app.layout = html.Div([
    html.H1(children='My LLM App - All About AI'),
    html.Div("Select model temperature"),
    dcc.Input(id='model-temperature', type='number', value=0.7, min=0, max=2, step=0.1, style={'width':200}),
    dcc.Input(id='input-field', type='text', debounce=True, placeholder='Ask a question about AI...', value=None, style={'width':300}),
    html.Div(id='answer-div', children=''),  # This div will display the answer
])


@app.callback(
    Output(component_id='answer-div', component_property='children'),    # The component to update
    Input(component_id='input-field', component_property='value'),       # Input component that triggers the callback
    State(component_id='', component_property=''), ## A ##
    prevent_initial_call=True
)
def update_title(user_request):  ## B ##
    # define the model and chain
    output_parser = StrOutputParser()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")  ## C ##
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Always answer AI questions with skepticism."),
        ("user", "{input}")
    ])
    chain = prompt | llm | output_parser

    answer = chain.invoke({"input": user_request})
    return answer


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
