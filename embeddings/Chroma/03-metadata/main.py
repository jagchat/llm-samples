from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from chromadb.config import Settings
from chromadb import HttpClient 

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="emp_collection",
    embedding_function=embeddings,
    client=HttpClient(host='localhost', port=9000) #Chroma service running externally (docker container)
)

employees = [
    {"name": "Scott", "role": "Technician", "department": "Engineering", "description": "Scott is a skilled technician."},
    {"name": "Smith", "role": "Engineer", "department": "Engineering", "description": "Smith is a lead engineer."},
    {"name": "Alice", "role": "Manager", "department": "Management", "description": "Alice manages the engineering team."},
]

# Separate texts and metadata
texts = [emp["description"] for emp in employees]
metadatas = [{"name": emp["name"], "role": emp["role"], "department": emp["department"]} for emp in employees]

# Add documents to Chroma
vector_store.add_texts(texts=texts, metadatas=metadatas)

# Example Queries (using LangChain's Chroma wrapper)

# 1. Find employees in the Engineering department:
results = vector_store.similarity_search_with_score(
    "engineer", k=2,  # Search for "engineer" related descriptions
    filter={"department": "Engineering"}  # Filter by metadata
)
print("\nEngineering Department Employees:")
for doc, score in results:
    print(f"Document: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")


# 2. Find Technicians:
results = vector_store.similarity_search_with_score(
    "technical skills", k=1,
    filter={"role": "Technician"}
)
print("\nTechnicians:")
for doc, score in results:
    print(f"Document: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")

# 3. Find employees named Smith:
results = vector_store.similarity_search_with_score(
    "employee information", k=1,
    filter={"name": "Smith"}
)
print("\nSmith:")
for doc, score in results:
    print(f"Document: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")
