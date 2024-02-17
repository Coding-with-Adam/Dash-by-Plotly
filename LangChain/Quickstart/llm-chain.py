# pip install langchain
# pip install langchain-openai
# pip install python-dotenv
from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)  # load api key


# Basic Model Usage -------------------------------------------------------
# https://api.python.langchain.com/en/latest/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html#
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
answer = llm.invoke("Can you tell me about AI's role in the world?")
print(answer)



# Adding Prompts ----------------------------------------------------------
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
#
# output_parser = StrOutputParser() # stringify the answer
# llm = ChatOpenAI(model_name="gpt-3.5-turbo")
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "Always answer AI questions with skepticism."),
#     ("user", "{input}")
# ])
# chain = prompt | llm | output_parser
# answer = chain.invoke({"input": "Can you tell me about AI's role in the world?"})
# print(answer)



# Create your own ChatGPT -------------------------------------------------
# from dash import Dash, html, dcc, Input, Output
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
#
# # define the model and chain
# output_parser = StrOutputParser()
# llm = ChatOpenAI(model_name="gpt-3.5-turbo")
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "Always answer AI questions with skepticism."),
#     ("user", "{input}")
# ])
# chain = prompt | llm | output_parser
#
# # Initialize the Dash app
# app = Dash()
# # Define the layout of the app
# app.layout = html.Div([
#     html.Div(children='My LLM App - All About AI'),  # This div will display the app title
#     # This input field lets the user type their question or request
#     dcc.Input(id='input-field', type='text', debounce=True, placeholder='Ask a question about AI...', value=None),
#     html.Div(id='answer-div', children=''),  # This div will display the answer
# ])
#
#
# @app.callback(
#     Output(component_id='answer-div', component_property='children'),  # The component to update
#     Input(component_id='input-field', component_property='value'),     # The Input component that triggers the update
#     prevent_initial_call=True
# )
# def update_title(user_request):
#     answer = chain.invoke({"input": user_request})
#     return answer
#
#
# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=False)
