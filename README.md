## Pinecone-Wikipedia

Wikipedia is a rich source of informatiomn well-suited for semantic search.

Recent efforts have indexed Wikipedia using Cohere embeddings [here](https://huggingface.co/datasets/Cohere/wikipedia-22-12) and [here](https://huggingface.co/datasets/Cohere/wikipedia-22-12-en-embeddings?row=6).

< To add context here >

### Index

< To add context here >

### API keys

Ensure these are set:

* PINECONE_API_KEY
* PINECONE_ENVIRONMENT
* PINECONE_INDEX_NAME 
* COHERE_API_KEY 
* OPENAI_API_KEY

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

We won't need `packages`:
```
rm -rf packages
```

Modify the Dockerfile to remove `COPY ./packages ./packages`.

**(2) Add your runnable (RAG app)**

Create a file, `chain.py` with a runnable named `chain` that you want to execute. This is our RAG logic.

Add `chain.py` to `app` directory.

Import the runnable in `server.py`:
```
from app.chain import chain as pinecone_wiki_chain
add_routes(app, pinecone_wiki_chain, path="/pinecone-wikipedia")
```

Add your app dependencies to `pyproject.toml` and `poetry.lock`:
```
poetry add pinecone-client
poetry add cohere
poetry add openai
```

Update enviorment based on the updated lock file:
```
poetry install
```

Run locally
```
poetry run langchain serve
```

**(3) Deploy it with hosted LangServe**

Go to your LangSmith console and select `New Deployment`.

Specify the Github url along with the abovementioned API keys.
