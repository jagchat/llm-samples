import time
import asyncio
import traceback
from logger import get_logger
from config_loader import app_config
from db import get_db
from stateDb import get_state
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from chromadb import HttpClient 
from datetime import date, datetime

logger = get_logger(__name__)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma(
    collection_name="emp_shifts_collection",
    embedding_function=embeddings,
    client=HttpClient(host='localhost', port=38000) #Chroma service running externally (docker container)
)

def getLastRecordId():
    logger.info("getLastRecordId: Started..")
    value = get_state().getValue("last_record_id_processed")
    result = value

    # Check if it's binary
    if isinstance(value, bytes):
        # Decode to string if appropriate
        try:
            result = value.decode('utf-8') # or other encoding
        except UnicodeDecodeError:
            logger.error(f"ERROR at getLastRecordId: Unable to decode the binary data {value}")
            print(f"ERROR at getLastRecordId: Unable to decode the binary data {value}")
          
    logger.info("getLastRecordId: Completed..")
    return result

def setLastRecordId(recordId):
    logger.info("setLastRecordId: Started..")
    get_state().setValue("last_record_id_processed", recordId)
    logger.info("setLastRecordId: Completed..")

async def getNextBatchOfShiftData(last_record_id_processed):
    logger.info("getNextBatchOfShiftData: Started..")
    
    sqlWhereClause = ""    
    if not last_record_id_processed:
        logger.info("getNextBatchOfShiftData: Last Record Id not available..")
    else:
        logger.info(f"getNextBatchOfShiftData: fetching next batch from: {last_record_id_processed}")
        sqlWhereClause = f"WHERE seq_id > {last_record_id_processed}"

    sql = f"""
            SELECT 
                s.seq_id as seq_id
                , s.shift_id as shift_id
                , s.emp_id as emp_id 
                , s.dept_id as dept_id
                , s.start_date as start_date
                , s.start_time as start_time
                , s.end_date as end_date
                , s.end_time as end_time
                , ei.first_name AS first_name
                , ei.last_name AS last_name
                , di.dept_name AS dept_name 
            FROM shifts.shift_info s
            INNER JOIN employees.employee_info ei
            	ON s.emp_id = ei.emp_id 
            INNER JOIN employees.dept_info di
            	ON s.dept_id = di.dept_id 
            {sqlWhereClause}
            ORDER BY s.seq_id ASC
            LIMIT 500;
    """

    #logger.info(f"getNextBatchOfShiftData: {sql}")
    result = await get_db().fetch_data_return_json(sql)
    logger.info("getNextBatchOfShiftData: Completed..")
    #return {"isError": "false", "data": result} 
    return result

def generateEmbeddings(records):
    logger.info("generateEmbeddings: Started..")
    if records is not None and len(records) > 0:
        context_batch = []
        for record in records:
            s_start_date = datetime.strptime(str(record['start_date']), "%Y-%m-%d")
            f_start_date = s_start_date.strftime("%m/%d/%Y")
            s_end_date = datetime.strptime(str(record['end_date']), "%Y-%m-%d")
            f_end_date = s_end_date.strftime("%m/%d/%Y")
            record_text = (
                f"Employee {record['first_name']} {record['last_name']} with Employee ID: {record['emp_id']} "
                f"is scheduled to work in a shift "
                f"on date {f_start_date} "
                f"in department {record['dept_name']} (Department ID: {record['dept_id']}) "
                f"from start time {str(record['start_time'])} to end date {f_end_date} and end time {str(record['end_time'])} "
                f"and the shift schedule is uniquely identified by shift id {record['shift_id']}.  "
            )
            context_batch.append({
                "text": record_text,
                "metadata": {
                    "shift_id": record["shift_id"],
                    "first_name": record["first_name"],
                    "last_name": record["last_name"],
                    "emp_id": record["emp_id"],
                    "dept_name": record["dept_name"],
                    "dept_id": record["dept_id"],
                    "start_date": f_start_date,
                    "start_time": str(record["start_time"]),
                    "end_date": f_end_date,
                    "end_time": str(record["end_time"])
                }
            })

    logger.info("generateEmbeddings: Completed..")
    return context_batch

def updateEmbeddings(records):
        logger.info("updateEmbeddings: Started..")

        ids, documents, metadatas = [], [], []

        # Process data in batches
        for data in generateEmbeddings(records):
            documents.append(data["text"])
            metadatas.append(data["metadata"])
        
        vector_store.add_texts(texts=documents, metadatas=metadatas)

        logger.info("updateEmbeddings: Completed..")

async def updateKnowledgeBase():
    logger.info("updateKnowledgeBase: Started..")
    while True:
        last_record_id_processed = getLastRecordId()
        records = await getNextBatchOfShiftData(last_record_id_processed)
        if records and len(records) > 0:
            print(f"New data found..working on it..")
            updateEmbeddings(records)
            last_record = records[-1]
            last_record_id_fetched = last_record.get("seq_id")
            setLastRecordId(last_record_id_fetched)
        else:
            break

    logger.info("updateKnowledgeBase: Completed..")

async def main():
    logger.info("main: started..")
    if app_config is not None:
        try:
            while True:
                print("Checking for new data..")
                await updateKnowledgeBase()
                time.sleep(10)  # Wait for 10 seconds            
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