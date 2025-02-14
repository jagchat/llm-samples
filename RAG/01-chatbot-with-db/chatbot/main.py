import asyncio
import traceback
from logger import get_logger
from config_loader import app_config
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import Ollama
from chromadb import HttpClient 

logger = get_logger(__name__)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store = Chroma(
    collection_name="emp_shifts_collection",
    embedding_function=embeddings,
    client=HttpClient(host='localhost', port=38000) #Chroma service running externally (docker container)
)
ollm = Ollama(model="llama3.2:latest")

def get_response(chatState, question: str) -> str:
    logger.info("get_response: Started..")

    # retriever = vector_store.as_retriever(
    #     search_type="mmr",  # Maximal Marginal Relevance for diverse results
    #     search_kwargs={"k": 5}  # Fetch top 5 relevant chunks
    # )

    # Create retrieval chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=ollm,
        retriever=vector_store.as_retriever(),
        memory=chatState
    )    
    response = chain({"question": question})

    logger.info("get_response: Completed..")
    return response['answer']

async def main():
    logger.info("main: started..")
    if app_config is not None:
        try:
            chatState = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            while True:
                question = input("\nAsk a question (or type 'q' to quit): ")
                if question.lower() == 'q':
                    print("Goodbye!\n")
                    break
                response = get_response(chatState, question)
                print(f"{response}\n")
        except asyncio.CancelledError as e:
            print("Application Cancelled to stop..")
        except Exception as e:  # Catch all other exceptions here
            print(f"ERROR at main: {e}")
            logger.error(f"ERROR at main: {e}")
            logger.error(traceback.format_exc())
    else:
        print("ERROR at main: Application didn't start. Config.json is not found or parser error")
        logger.error(f"ERROR at main: Application didn't start. Config.json is not found or parser error")

    logger.info("main: completed..")    

if __name__ == "__main__":
    print("Process: Started..")
    logger.info("Process: Started..")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped by user (Ctrl+C).")
        logger.info("Application stopped by user (Ctrl+C).")
        print("Shutdown complete.")
        logger.info("Shutdown complete.")
    except Exception as e:  # Catch all other exceptions here
        print(f"ERROR at root: {e}")
        traceback.print_exc() 
        logger.error(f"ERROR at root: {e}")
        logger.error(traceback.format_exc())
    print("Process: Stopped.")
    logger.info("Process: Stopped.")