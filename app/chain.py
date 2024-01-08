import os
import pinecone
from langchain_core.pydantic_v1 import BaseModel
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Pinecone
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import CohereEmbeddings
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Keys
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENVIRONMENT = os.environ["PINECONE_ENVIRONMENT"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]

# Vectorstore
pinecone.init(api_key=PINECONE_API_KEY,
              environment=PINECONE_ENVIRONMENT)
embeddings = CohereEmbeddings(model="multilingual-22-12")
vectorstore = Pinecone.from_existing_index(PINECONE_INDEX_NAME, 
                                           embeddings)
retriever = vectorstore.as_retriever()

# RAG prompt
template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# RAG
model = ChatOpenAI()
chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)