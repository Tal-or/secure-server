import inspect
import logging
from enum import Enum

LOG_FILE_PATH = ' '


class ResCode(Enum):
    OK = 0
    ERROR = 1
    ERR_NO_MD5SUM = 4
    ERR_DIFF_MD5SUM = 5


class SecureServerLogger:
    logging.basicConfig(filename=LOG_FILE_PATH,
                        level=logging.INFO,
                        format=str("%(asctime)s - %(message)s"),
                        datefmt='%d/%m %I:%M:%S %p')

    @staticmethod
    def lineno():
        """Returns the current line number in our program."""
        return inspect.currentframe().f_back.f_lineno

    @staticmethod
    def set_log_level(level: str):
        logging.getLogger().setLevel(level)

    @staticmethod
    def debug(header, msg):
        logging.debug(_(metadata=header, debug=msg))

    @staticmethod
    def info(header, msg):
        logging.info(_(metadata=header, info=msg))

    @staticmethod
    def error(header, msg):
        logging.error(_(metadata=header, error=msg))