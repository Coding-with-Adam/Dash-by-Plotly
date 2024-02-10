"""
ChatOpenAI pParameters -- https://api.python.langchain.com/en/latest/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html#
Temperature -- https://platform.openai.com/docs/guides/text-generation/faq
A model's temperature controls how creative or conservative the generated text is. Temperature is between 0 to 2.
A higher temperature (e.g., 0.7) results in more diverse and creative output,
while a lower temperature (e.g., 0.2) makes the output more deterministic and focused.
ChatOpenAI's default temperature is 0.7.

Exercise 2: Update the model's temperature to 1.5 and explore the generated text. Then, modify to 0.1 to see what has changed.
            Limit the model to 500 tokens to reduce api key usage.

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
