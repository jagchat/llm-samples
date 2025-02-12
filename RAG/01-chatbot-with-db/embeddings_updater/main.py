import asyncio
import traceback
from logger import get_logger
from config_loader import app_config
from db import get_db
import time

logger = get_logger(__name__)

async def getShiftData(payload):
    logger.info("getShiftData: Started..")
    # last_record_id_processed = payload["last_record_id_processed"]
    # if not last_record_id_processed:
    #     raise Exception("last_record_id_processed is required")
    
    sql = f"""
            SELECT 
                s.shift_id, s.emp_id, s.dept_id, s.start_date, s.start_time, s.end_date, s.end_time
            FROM shifts.shift_info s                        
            ORDER BY seq_id ASC
            LIMIT 1;
    """

    result = await get_db().fetch_data_return_json(sql)

    logger.info("getShiftData: Completed..")
    #return {"isError": "false", "data": result} 
    print(result)
    return result

async def main():
    logger.info("main: started..")
    if app_config is not None:
        try:
            logger.info("main: Starting Server..")
            while True:
                result = await getShiftData(None)
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