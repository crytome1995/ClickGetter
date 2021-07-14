import logging
from logging.handlers import RotatingFileHandler
from config import config


class Logger(object):
    def __init__(self):
        self.error_logger = logging.getLogger("error")
        self.error_logger.setLevel(logging.ERROR)
        self.error_logger.propagate = False
        self.error_logger.addHandler(self._get_handler("error"))
        self.info_logger = logging.getLogger("info")
        self.info_logger.setLevel(logging.INFO)
        self.info_logger.propagate = False
        self.info_logger.addHandler(self._get_handler("info"))
        self.warn_logger = logging.getLogger("warn")
        self.warn_logger.setLevel(logging.WARN)
        self.warn_logger.propagate = False
        self.warn_logger.addHandler(self._get_handler("warn"))

    def _get_handler(self, level):
        rhandler = RotatingFileHandler(
            config.log_directory + "%s.log" % (level), maxBytes=50000, backupCount=5
        )
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
        rhandler.setFormatter(formatter)
        return rhandler

    def warn(self, message):
        self.warn_logger.log(logging.WARN, message)

    def error(self, message):
        self.error_logger.log(logging.ERROR, message)

    def info(self, message):
        self.info_logger.log(logging.INFO, message)


logger = Logger()
