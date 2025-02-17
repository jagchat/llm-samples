from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import HuggingFaceEmbeddings
import weaviate
from weaviate.connect import ConnectionParams

client = weaviate.Client(
    url="http://localhost:9080",  # Update if needed
    timeout_config=(5, 60)  # (connect timeout, read timeout)
)

# Check connection
if client.is_ready():
    print("Connected to Weaviate successfully!")
else:
    print("Failed to connect to Weaviate.")

# Initialize the HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create a class (collection) in Weaviate if it doesn't exist
class_name = "Employee"
class_config = {
    "class": class_name,
    "vectorizer": "none",  # We'll use LangChain's embeddings
    "properties": [
        {"name": "description", "dataType": ["text"]},
        {"name": "name", "dataType": ["string"]},
        {"name": "role", "dataType": ["string"]},
        {"name": "department", "dataType": ["string"]}
    ]
}

# Check if class exists, if not create it
if not client.schema.exists(class_name):
    client.schema.create_class(class_config)

# Initialize Weaviate vector store
vector_store = Weaviate(
    client=client,
    index_name=class_name,
    text_key="description",
    embedding=embeddings,
    by_text=False
)

# Sample employee data
employees = [
    {"name": "Scott", "role": "Technician", "department": "Engineering", "description": "Scott is a skilled technician."},
    {"name": "Smith", "role": "Engineer", "department": "Engineering", "description": "Smith is a lead engineer."},
    {"name": "Alice", "role": "Manager", "department": "Management", "description": "Alice manages the engineering team."},
]

# Separate texts and metadata
texts = [emp["description"] for emp in employees]
metadatas = [{"name": emp["name"], "role": emp["role"], "department": emp["department"]} for emp in employees]

# Add documents to Weaviate
vector_store.add_texts(texts=texts, metadatas=metadatas)

# Example Queries using Weaviate

# 1. Find employees in the Engineering department:
results = vector_store.similarity_search_with_score(
    "engineer",
    k=2,
    filter={
        "path": ["department"],
        "operator": "Equal",
        "valueString": "Engineering"
    }
)
print("\nEngineering Department Employees:")
for doc, score in results:
    print(f"Document: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")

# 2. Find Technicians:
results = vector_store.similarity_search_with_score(
    "technical skills",
    k=1,
    filter={
        "path": ["role"],
        "operator": "Equal",
        "valueString": "Technician"
    }
)
print("\nTechnicians:")
for doc, score in results:
    print(f"Document: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")

# 3. Find employees named Smith:
results = vector_store.similarity_search_with_score(
    "employee information",
    k=1,
    filter={
        "path": ["name"],
        "operator": "Equal",
        "valueString": "Smith"
    }
)
print("\nSmith:")
for doc, score in results:
    print(f"Document: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")