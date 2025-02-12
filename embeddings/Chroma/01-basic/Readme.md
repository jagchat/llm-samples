# Chroma Embeddings demo

- Everything is local
- Uses HuggingFaceEmbeddings for embedding text data
- Uses Chroma as a vector database that stores embeddings
- Chroma uses the sqlite3 library to create and manage the database.
- We are not having Chroma as a separate service.
  - If Chroma doesn't find any service, it automatically creates the sqlite database file (and related artifacts) in the `chroma-data` folder (and persists embeddings).

## Run locally

- Ensure .venv is activated
- Ensure python packages are installed in the virtual environment
- Run `python3 main.py`
