import logging
import logging.config
import os

import yaml


class LoggerControl:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LoggerControl, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.loggers = {}

    def get_logger(self, logger_name):
        if logger_name not in self.loggers.keys():
            self.loggers[logger_name] = logging.getLogger(logger_name)
        return self.loggers[logger_name]

    @staticmethod
    def setup_logging(path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
