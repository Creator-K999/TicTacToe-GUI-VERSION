from logging import config, getLogger
from os.path import basename
from inspect import stack

from threading import Lock, Thread


class Log:
    __lock = Lock()

    config.fileConfig(fname="logger.config")
    __logger = getLogger(__name__)

    def __init__(self):
        raise NotImplementedError("Log cannot be instantiated!")

    @staticmethod
    def __log(target, message):
        caller_info = stack()[2]  # list of named tuples
        Thread(
            daemon=True,
            target=target,
            args=(f"\n\tFILE: {basename(caller_info.filename)}"
                  f"\n\tFUNC: {caller_info.function}"
                  f"\n\tLINE: {caller_info.lineno}"
                  f"\n\tMESSAGE: {message}\n",)
        ).start()

    @classmethod
    def debug(cls, message):
        with cls.__lock:
            cls.__log(cls.__logger.debug, message)

    @classmethod
    def info(cls, message):
        with cls.__lock:
            cls.__log(cls.__logger.info, message)

    @classmethod
    def warning(cls, message):
        with cls.__lock:
            cls.__log(cls.__logger.warning, message)

    @classmethod
    def error(cls, message):
        with cls.__lock:
            cls.__log(cls.__logger.error, message)

    @classmethod
    def exception(cls, message):
        with cls.__lock:
            cls.__log(cls.__logger.exception, message)

    @classmethod
    def critical(cls, message):
        with cls.__lock:
            cls.__log(cls.__logger.critical, message)
