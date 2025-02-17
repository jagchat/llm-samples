# Weaviate Embeddings demo

- Everything is local
- Uses HuggingFaceEmbeddings for embedding text data
- Uses Weaviate as a vector database that stores embeddings
- Weaviate runs as a docker container
- VectorAdmin for (Weaviate) embeddings viewer
  -- Check docker-compose for more details

## Run locally

- Ensure .venv is activated
- Ensure python packages are installed in the virtual environment
- Run `./start-chroma.ps1`
- Run `python3 main.py`
