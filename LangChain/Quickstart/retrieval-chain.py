from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI

# activate api key
# .env file should have: OPENAI_API_KEY="my-openAI-key"
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
llm = ChatOpenAI(model_name="gpt-3.5-turbo")  # load chat model


# load HTML pages and parse them with `BeautifulSoup`
loader = WebBaseLoader("https://en.wikipedia.org/wiki/Paris")
docs = loader.load()  # load parse text
# print(docs)
# exit()


embeddings = OpenAIEmbeddings()  # load embedding model to turn text to array of numbers
# split the docs' text into smaller chunks of text (because we have too much text to pass to an LLM)
# and index it into a vectorstore
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
# print(documents)
# exit()
vector = FAISS.from_documents(documents, embeddings)


prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)  # chain the LLM to the prompt


# create a chain that will retrieve the most relevant docs (based on the input question)
# and pass them in as the `context`
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({"input": "What was Paris architecture like in the 19th century"})
print(response["answer"])
