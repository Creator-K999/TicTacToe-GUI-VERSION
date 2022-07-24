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
    def __log(target, message, stack_info):
        Thread(
            daemon=True,
            target=target,
            args=(
                f"""
    FILE: {basename(stack_info.filename)}
    FUNC: {stack_info.function}
    LINE: {stack_info.lineno}
    MASG: {message}
""",)
        ).start()

    @classmethod
    def debug(cls, message, custom_stack=None):
        with cls.__lock:
            cls.__log(cls.__logger.debug, message, custom_stack or stack()[1])

    @classmethod
    def info(cls, message, custom_stack=None):
        with cls.__lock:
            cls.__log(cls.__logger.debug, message, custom_stack or stack()[1])

    @classmethod
    def warning(cls, message, custom_stack=None):
        with cls.__lock:
            cls.__log(cls.__logger.debug, message, custom_stack or stack()[1])

    @classmethod
    def error(cls, message, custom_stack=None):
        with cls.__lock:
            cls.__log(cls.__logger.debug, message, custom_stack or stack()[1])

    @classmethod
    def exception(cls, message, custom_stack=None):
        with cls.__lock:
            cls.__log(cls.__logger.debug, message, custom_stack or stack()[1])

    @classmethod
    def critical(cls, message, custom_stack=None):
        with cls.__lock:
            cls.__log(cls.__logger.debug, message, custom_stack or stack()[1])
