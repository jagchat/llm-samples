import asyncpg
import traceback
from logger import get_logger
from config_loader import app_config

class Db:

    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("init: Started..")
        if app_config is not None:
            db_config = app_config.get("main_db", None)
            if db_config is not None:
                self.db_config = db_config
            else:
                self.logger.error(f"ERROR at Db.init: Cannot connect to database.  Db Config is not found or parser error")
                raise Exception("Cannot connect to database.  Db Config is not found or parser error")
        self.logger.info("init: Completed..")

    async def fetch_data(self, query, params=None):
        self.logger.info("fetch_data: Started..")
        records = None
        conn = None
        try:
            # Connect to the database
            conn = await asyncpg.connect(
                host= self.db_config.get("host"),
                port= self.db_config.get("port"),
                database= self.db_config.get("dbname"),
                user= self.db_config.get("user"),
                password= self.db_config.get("password")
            )
            
            # Execute query
            records = await conn.fetch(query, *params if params else [])
            
            # Close connection
            await conn.close()
            
        except Exception as e:
            self.logger.error(f"ERROR at Db.fetch_data: {e}")
            self.logger.error(traceback.format_exc())
            raise
        finally:
            if conn:
                await conn.close()
                
        self.logger.info("fetch_data: Completed..")
        return records        
    
    async def fetch_records(self, query, params=None):
        self.logger.info("fetch_records: Started..")
        records = await self.fetch_data(query, params)
        self.logger.info("fetch_records: Completed..")
        return [dict(record) for record in records]

    async def fetch_data_return_json(self, query, params=None):
        self.logger.info("fetch_data_return_json: Started..")
        records = await self.fetch_records(query, params)
        json_list = [dict(record) for record in records]
        self.logger.info("fetch_data_return_json: Completed..")
        return json_list
        
def get_db():
    return Db()