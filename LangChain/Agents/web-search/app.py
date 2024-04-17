from dotenv import find_dotenv, load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.load import dumps, loads
from dash import Dash, dcc, html, callback, Output, Input, State, no_update
# pip install -r requirements.txt

# activate api keys
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

llm = ChatOpenAI(temperature=0)

tavily_tool = TavilySearchResults()
tools = [tavily_tool]


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant. Make sure to use the tavily_search_results_json tool for information"),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

def process_chat(agent_executor, user_input, chat_history):
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    return response["output"]


app = Dash()
app.layout = html.Div([
    html.H2("Ask me anything. I'm your personal assistant that can search the web"),
    dcc.Input(id="my-input", type="text", debounce=True, style={"width":500, "height":30}),
    html.Br(),
    html.Button("Submit", id="submit-query", style={"backgroundColor":"blue", "color":"white"}),
    dcc.Store(id="store-it", data=[]),
    html.P(),
    html.Div(id="response-space")
])

@callback(
    Output("response-space", "children"),
    Output("store-it","data"),
    Input("submit-query", "n_clicks"),
    State("my-input", "value"),
    State("store-it","data"),
    prevent_initial_call=True
)
def interact_with_agent(n, user_input, chat_history):
    if len(chat_history) > 0:
        chat_history = loads(chat_history) # deserialize the chat_history (convert json to object)
    print(chat_history)

    response = process_chat(agent_executor, user_input, chat_history)
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response))

    history = dumps(chat_history)  # serialize the chat_history (convert the object to json)

    return f"Assistant: {response}", history



if __name__ == '__main__':
    app.run_server(debug=True)
