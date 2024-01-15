## Pinecone-Serverless

Pinecone is one of the most popular LangChain vectorstore integration partners.

The launch of Pinecone serverless enables “unlimited” index capacity via cloud object storage (ex. S3, GCS) along with decreased cost to serve (only pay for what you use).

This pairs well with LangServe and LangSmith, making it easy to build production RAG applications.

This template repo provide one such example.

### Index

Follow instructions from Pinecone on setting up your serverless index.

### API keys

Ensure these are set:

* PINECONE_API_KEY
* PINECONE_ENVIRONMENT
* PINECONE_INDEX_NAME 
* OPENAI_API_KEY

Note: the choice of embedding model may require additional API keys, such as:
* COHERE_API_KEY

### Notebook

For prototyping:
```
poetry run jupyter notebook
```

### Deployment

This repo was created by following these steps:

**(1) Create a LangChain app.**

Run:
```
langchain app new .  
```

This creates two folders:
```
app: This is where LangServe code will live
packages: This is where your chains or agents will live
```

It also creates:
```
Dockerfile: App configurations
pyproject.toml: Project configurations
```

Add your app dependencies to `pyproject.toml` and `poetry.lock` to support Pinecone serverless:
```
poetry add pinecone-client==3.0.0.dev8
poetry add langchain-community==0.0.12
poetry add cohere
poetry add openai
poetry add jupyter
```

Update enviorment based on the updated lock file:
```
poetry install
```

**(2) Add your runnable (RAG app)**

Create a file, `chain.py` with a runnable named `chain` that you want to execute. 

This is our RAG logic (e.g., that we prototyped in our notebook).

Add `chain.py` to `app` directory.

Import the LCEL object in `server.py`:
```
from app.chain import chain as pinecone_wiki_chain
add_routes(app, pinecone_wiki_chain, path="/pinecone-wikipedia")
```

Run locally
```
poetry run langchain serve
```

**(3) Deploy it with hosted LangServe**

Go to your LangSmith console.

Select `New Deployment`.

Specify this Github url.

Add the abovementioned API keys as secrets.
