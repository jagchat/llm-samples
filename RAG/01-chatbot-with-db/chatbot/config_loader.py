import json
import os
from pathlib import Path
from logger import get_logger  

class ConfigLoader:
    def __init__(self, config_file_path=None):
        self.logger = get_logger(__name__)
        self.logger.info("init: Started..")

        # Default to root config.json if no path is specified
        if config_file_path is None:
            root_dir = Path(__file__).resolve().parent  # Adjust if needed
            config_file_path = root_dir / "config.json"
            self.logger.info(f"init: computed config.json path: {config_file_path}")

        self.config_file_path = config_file_path
        self.config = None
        self.load_config()
        self.logger.info("init: Completed.")

    def load_config(self):
        self.logger.info("load_config: Started..")
        try:
            with open(self.config_file_path, "r") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            print(f"Error: Config file not found at {self.config_file_path}")
            self.logger.error(f"Error: Config file not found at {self.config_file_path}")
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON - {e}")
            self.logger.error(f"Error: Failed to parse JSON - {e}")

        self.logger.info("load_config: Completed.")

    def get_config(self):
        self.logger.info("get_config: Started..")
        if self.config is None:
            self.load_config()
        self.logger.info("get_config: Completed..")
        return self.config

    def override_with_env_vars(self):
        self.logger.info("override_with_env_vars: Started..")
        if self.config is None:
            self.logger.warning("override_with_env_vars: Config is None!")
            return

        for key, value in os.environ.items():
            if "_" in key:
                section_name, param_name = key.split("_", 1)
                if section_name.lower() in self.config and self.config[section_name.lower()]:
                    self.config[section_name.lower()][param_name.lower()] = value
                    print(f"Overriding config value: {section_name.lower()}.{param_name.lower()} with environment variable value: {value}")
                    self.logger.info(f"Overriding config value: {section_name.lower()}.{param_name.lower()} with environment variable value: {value}")
        self.logger.info("override_with_env_vars: Completed..")


config_loader = ConfigLoader()
config_loader.override_with_env_vars()  # Override config with env vars before loading
app_config = config_loader.get_config()