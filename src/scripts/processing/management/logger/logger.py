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
    def __log(target, message, custom_stack):
        Thread(
            daemon=True,
            target=target,
            args=(f"\n\tFILE: {basename(custom_stack.filename)}"
                  f"\n\tFUNC: {custom_stack.function}"
                  f"\n\tLINE: {custom_stack.lineno}"
                  f"\n\tMESSAGE: {message}\n",)
        ).start()

    @classmethod
    def debug(cls, message, custom_stack=None):
        with cls.__lock:
            if custom_stack is None:
                cls.__log(cls.__logger.debug, message, stack()[1])
            else:
                cls.__log(cls.__logger.debug, message, custom_stack)

    @classmethod
    def info(cls, message, custom_stack=None):
        with cls.__lock:
            if custom_stack is None:
                cls.__log(cls.__logger.info, message, stack()[1])
            else:
                cls.__log(cls.__logger.info, message, custom_stack)

    @classmethod
    def warning(cls, message, custom_stack=None):
        with cls.__lock:
            if custom_stack is None:
                cls.__log(cls.__logger.warning, message, stack()[1])
            else:
                cls.__log(cls.__logger.warning, message, custom_stack)

    @classmethod
    def error(cls, message, custom_stack=None):
        with cls.__lock:
            if custom_stack is None:
                cls.__log(cls.__logger.error, message, stack()[1])
            else:
                cls.__log(cls.__logger.error, message, custom_stack)

    @classmethod
    def exception(cls, message, custom_stack=None):
        with cls.__lock:
            if custom_stack is None:
                cls.__log(cls.__logger.exception, message, stack()[1])
            else:
                cls.__log(cls.__logger.exception, message, custom_stack)

    @classmethod
    def critical(cls, message, custom_stack=None):
        with cls.__lock:
            if custom_stack is None:
                cls.__log(cls.__logger.critical, message, stack()[1])
            else:
                cls.__log(cls.__logger.critical, message, custom_stack)
