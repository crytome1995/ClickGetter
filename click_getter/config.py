import os
from enum import Enum


class EnvVars(Enum):
    CLICK_TABLE_NAME = "CLICK_TABLE_NAME"
    AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"
    LOG_DIRECTORY = "LOG_DIRECTORY"


class ConfigDefaults:
    CLICKS_TABLE = "click_bags_dev"
    DEFAULT_AWS_REGION = "us-east-2"
    LOG_DIRECTORY_LOCATION = ""


class Configuration(ConfigDefaults):
    def __init__(
        self,
        click_bags_table=ConfigDefaults.CLICKS_TABLE,
        default_region=ConfigDefaults.DEFAULT_AWS_REGION,
        log_directory=ConfigDefaults.LOG_DIRECTORY_LOCATION,
    ):

        self._click_bags_table = click_bags_table
        self._default_region = default_region
        self._log_driectory = log_directory

    @property
    def default_region(self):
        env_var = os.getenv(EnvVars.AWS_DEFAULT_REGION.value)
        if env_var:
            return env_var
        else:
            return self._default_region

    @property
    def click_bags_table(self):
        env_var = os.getenv(EnvVars.CLICK_TABLE_NAME.value)
        if env_var:
            return env_var
        else:
            return self._click_bags_table

    @property
    def log_directory(self):
        env_var = os.getenv(EnvVars.LOG_DIRECTORY.value)
        if env_var:
            return env_var
        else:
            return self._log_driectory


config = Configuration()
