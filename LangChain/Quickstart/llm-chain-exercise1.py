"""
ChatOpenAI pParameters -- https://api.python.langchain.com/en/latest/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html#
Model Tokens -- https://platform.openai.com/docs/guides/text-generation/managing-tokens
Language models read and write text in chunks called tokens. In English, a token can be as short as one character
or as long as one word (e.g., a or apple). The total number of tokens in an API call affects:
  - How much your API call costs, as you pay per token
  - How long your API call takes, as writing more tokens takes more time
  - Whether your API call works at all, as total tokens must be below the model’s maximum limit (4097 tokens for gpt-3.5-turbo)

Exercise 1: Update the model's max token limit to 500.
**Solution** can be found in -- https://charming-data.circle.so/c/langchain-education/quickstart-llm-chain 
"""

from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI

# activate api key
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
answer = llm.invoke("What will the world look like in 2 years?")
print(answer)
