from dash import Dash, html, dcc, callback, Output, Input, State
from langchain_community.agent_toolkits import GmailToolkit
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import find_dotenv, load_dotenv

# activate api keys
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Connect to Gmail and tools ----------------------------------------------
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()

# Use the LLM -------------------------------------------------------------
instructions = """You are an assistant that creates email drafts."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
llm = ChatOpenAI(temperature=0)
agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    # This is set to False to prevent information about my email showing up on the screen
    # Normally, it is helpful to have it set to True however.
    verbose=True,
    return_intermediate_steps=True  # Whether to return the agent’s trajectory of intermediate steps at the end in addition to the final output.
)

# response = agent_executor.invoke(
#     {
#         "input": "Create a gmail draft of an email from me, Adam, to a real estate agency called Mike Castles, whose email address is: tutorialemailonly2@gmail.com. The email will ask the agency information about their current house listing and prices as well as request a time to meet."
#     }
# )
# )
#
# print(response['Output'])
# exit()

def process_chat(agent_executor, user_input, chat_history):
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    return [response["output"], response['intermediate_steps'][0]]


app = Dash()
app.layout = [
    dcc.Store(id="store-it", data=[]),
    html.H1("Email Creating App"),
    dcc.Textarea(id='llm-request', style={'width': '30%', 'height': 300}),
    html.Button('Submit', id='btn'),
    html.Div(id='output-space')
]

@callback(
    Output('output-space', 'children'),
    Output("store-it", "data"),
    Input('btn', 'n_clicks'),
    State('llm-request', 'value'),
    State("store-it", "data"),
    prevent_initial_call=True
)
def draft_email(_, user_input, chat_history):
    if len(chat_history) > 0:
        chat_history = loads(chat_history) # deserialize the chat_history (convert json to object)
    print(chat_history)

    response = process_chat(agent_executor, user_input, chat_history)
    # print(response[1][0].tool_input['message'])
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response[0]))

    history = dumps(chat_history)  # serialize the chat_history (convert the object to json)
    # Create a gmail draft of an email from me, Adam, to a real estate agency called Mike Castles, whose email address is: tutorialemailonly2@gmail.com. The email will ask the agency information about their current house listing and prices as well as request a time to meet.
    # Please update the last sentence of the email draft to offer to meet next Monday at 10am.
    # Thank you. Please send the email.
    return [response[0], html.P(), response[1][0].tool_input['message']], history


if __name__ == "__main__":
    app.run(debug=True)
