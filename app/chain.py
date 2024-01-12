import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from pinecone import Pinecone as PineconeClient
import requests
load_dotenv()

# Keys
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENVIRONMENT = os.environ["PINECONE_ENVIRONMENT"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]

pinecone = PineconeClient(api_key=PINECONE_API_KEY)
embeddings = CohereEmbeddings(model="multilingual-22-12")
vectorstore = Pinecone.from_existing_index(index_name=PINECONE_INDEX_NAME,embedding=embeddings)

retriever = vectorstore.as_retriever()

def fetch_wikipedia_page(id):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&pageids={id}"
    response = requests.get(url)
    data = response.json()
    page_content = list(data['query']['pages'].values())[0]['extract']
    return page_content

def fetch_url(x):
    urls = [doc.metadata['url'] for doc in x['context']]
    ids = [url.split('=')[-1] for url in urls]
    contents = [fetch_wikipedia_page(id)[:32000] for id in ids]    
    return {"context": contents, "question": x["question"]}


# RAG prompt
template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# RAG
model = ChatOpenAI(model="gpt-4-32k")

chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | RunnableLambda(fetch_url)  # Add this line
    | prompt
    | model
    | StrOutputParser()
)


