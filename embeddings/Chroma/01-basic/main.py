import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

current_directory = os.path.dirname(os.path.abspath(__file__))
chroma_data_directory = os.path.join(current_directory, "./chroma-data" )
os.makedirs(chroma_data_directory)
vector_store = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings,
    persist_directory=chroma_data_directory 
)

# Add texts to the collection
texts = ["I have employees Scott and Smith", "Scott works as a Technician", "Smith works as an Engineer"]
vector_store.add_texts(texts)

# Perform a similarity search
results = vector_store.similarity_search("Who is Technician?", k=1)
print(results)