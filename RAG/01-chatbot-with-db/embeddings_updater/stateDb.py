import traceback
from logger import get_logger
from config_loader import app_config
from pymemcache.client import base

class StateDb:

    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("init: Started..")
        if app_config is not None:
            db_config = app_config.get("state_db", None)
            if db_config is not None:
                self.db_config = db_config
            else:
                self.logger.error(f"ERROR at StateDb.init: Cannot connect to database.  State Db Config is not found or parser error")
                raise Exception("Cannot connect to database.  State Db Config is not found or parser error")
        self.logger.info("init: Completed..")

    def getValue(self, key):
        self.logger.info("StateDb.getValue: Started..")
        result = None
        client = None
        try:
            client = base.Client((self.db_config.get("host"), self.db_config.get("port")))
            result = client.get(key)
        except Exception as e:
            self.logger.error(f"ERROR at StateDb.getValue: {e}")
            self.logger.error(traceback.format_exc())
            raise
        finally:
            if client:
                client.close()
                
        self.logger.info("StateDb.getValue: Completed..")
        return result        

    def setValue(self, key, value):
        self.logger.info("StateDb.setValue: Started..")
        client = None
        try:
            client = base.Client((self.db_config.get("host"), self.db_config.get("port")))
            client.set(key, value)
        except Exception as e:
            self.logger.error(f"ERROR at StateDb.setValue: {e}")
            self.logger.error(traceback.format_exc())
            raise
        finally:
            if client:
                client.close()
        self.logger.info("StateDb.setValue: Completed..")
            
def get_state():
    return StateDb()