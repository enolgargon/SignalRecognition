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
        self.setup_logging()

    def get_logger(self, logger_name):
        if logger_name not in self.loggers.keys():
            self.loggers[logger_name] = logging.getLogger(logger_name)
        return self.loggers[logger_name]

    @staticmethod
    def setup_logging(path='/home/ubuntu/SignalRecognition/logs/logging.yaml', default_level=logging.INFO):
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.error('Logging configuration fails to load')
            logging.basicConfig(level=default_level)
