from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from chromadb.config import Settings
from chromadb import HttpClient 
import os

# Set your OpenAI API key (important!)
os.environ["OPENAI_API_KEY"] = "----"  # Replace with your actual key

embeddings = OpenAIEmbeddings()

vector_store = Chroma(
    collection_name="emp_collection",
    embedding_function=embeddings,
    client=HttpClient(host='localhost', port=9000) #Chroma service running externally (docker container)
)

from langchain.docstore.document import Document
test_doc = Document(page_content="Test document", metadata={"test_key": "test_value"})
test_id = "test_id_1" # Test ID
vector_store.add_documents(documents=[test_doc], ids=[test_id])
