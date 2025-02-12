from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from chromadb.config import Settings
from chromadb import HttpClient 

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings,
    client=HttpClient(host='localhost', port=9000) #Chroma service running externally (docker container)
)

# Add texts to the collection
texts = ["I have employees Scott and Smith", "Scott works as a Technician", "Smith works as an Engineer"]
vector_store.add_texts(texts)

# Perform a similarity search
results = vector_store.similarity_search("Who is Technician?", k=1)
print(results)