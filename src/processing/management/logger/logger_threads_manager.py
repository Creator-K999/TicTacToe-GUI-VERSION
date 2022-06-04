from os.path import basename
from threading import Thread
from inspect import stack
from processing.logging.logger import Logger


class LoggerThreadManager:
    __instance = None
    __logger_thread = Logger()
    __threads_list = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(LoggerThreadManager, cls).__new__(cls)

        return cls.__instance

    @classmethod
    def get_threads_list(cls):
        return cls.__threads_list

    @classmethod
    def debug(cls, message):
        current_stack = stack()[1]  # list of named tuples

        cls.__logger_thread.debug(
            filename=basename(current_stack.filename),
            function=current_stack.function,
            line=current_stack.lineno,
            message=message)

        cls.__logger_thread.log_queue.get(True).start()

    @classmethod
    def info(cls, message):
        current_stack = stack()[1]  # list of named tuples

        cls.__logger_thread.info(
            filename=basename(current_stack.filename),
            function=current_stack.function,
            line=current_stack.lineno,
            message=message)

        cls.__logger_thread.log_queue.get(True).start()

    @classmethod
    def warning(cls, message):
        current_stack = stack()[1]  # list of named tuples

        cls.__logger_thread.warning(
            filename=basename(current_stack.filename),
            function=current_stack.function,
            line=current_stack.lineno,
            message=message)

        cls.__logger_thread.log_queue.get(True).start()

    @classmethod
    def error(cls, message):
        current_stack = stack()[1]  # list of named tuples

        cls.__logger_thread.error(
            filename=basename(current_stack.filename),
            function=current_stack.function,
            line=current_stack.lineno,
            message=message)

        cls.__logger_thread.log_queue.get(True).start()

    @classmethod
    def exception(cls, message):
        current_stack = stack()[1]  # list of named tuples

        cls.__logger_thread.exception(
            filename=basename(current_stack.filename),
            function=current_stack.function,
            line=current_stack.lineno,
            message=message)

        cls.__logger_thread.log_queue.get(True).start()

    @classmethod
    def critical(cls, message):
        current_stack = stack()[1]  # list of named tuples

        cls.__logger_thread.critical(
            filename=basename(current_stack.filename),
            function=current_stack.function,
            line=current_stack.lineno,
            message=message)

        cls.__logger_thread.log_queue.get(True).start()
