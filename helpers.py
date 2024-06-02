"""
get_username
Logger
"""

import os
import logging

def get_username():
    if os.name == 'nt':  # Windows
        return os.environ.get('USERNAME')
    else:  # Unix-based systems (Linux, macOS)
        return os.environ.get('USER')

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._configure_logging()
        return cls._instance


    def _configure_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('main_logger')

    def get_logger(self, logger_name):
        return logging.getLogger(logger_name)

