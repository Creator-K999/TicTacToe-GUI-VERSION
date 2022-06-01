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
    @property
    def threads_list(cls):
        return cls.__threads_list

    @classmethod
    def debug(cls, message):
        current_stack = stack()[1]  # list of named tuples

        thread = Thread(
            target=lambda: cls.__logger_thread.debug(
                f"\n\tFILE NAME: {basename(current_stack.filename)}"
                f"\n\tFUNC NAME: {current_stack.function}"
                f"\n\tLINE NUMBER: {current_stack.lineno}"
                f"\n\tMESSAGE: {message}\n"
            ),
            args=())

        cls.__threads_list.append(thread)
        thread.start()

    @classmethod
    def info(cls, message):
        current_stack = stack()[1]

        thread = Thread(
            target=lambda: cls.__logger_thread.info(
                f"\n\tFILE NAME: {basename(current_stack.filename)}"
                f"\n\tFUNC NAME: {current_stack.function}"
                f"\n\tLINE NUMBER: {current_stack.lineno}"
                f"\n\tMESSAGE: {message}\n"
            ),
            args=())

        cls.__threads_list.append(thread)
        thread.start()

    @classmethod
    def warning(cls, message):
        current_stack = stack()[1]

        thread = Thread(
            target=lambda: cls.__logger_thread.warning(
                f"\n\tFILE NAME: {basename(current_stack.filename)}"
                f"\n\tFUNC NAME: {current_stack.function}"
                f"\n\tLINE NUMBER: {current_stack.lineno}"
                f"\n\tMESSAGE: {message}\n"
            ),
            args=())

        cls.__threads_list.append(thread)
        thread.start()

    @classmethod
    def exception(cls, message):
        current_stack = stack()[1]

        thread = Thread(
            target=lambda: cls.__logger_thread.exception(
                f"\n\tFILE NAME: {basename(current_stack.filename)}"
                f"\n\tFUNC NAME: {current_stack.function}"
                f"\n\tLINE NUMBER: {current_stack.lineno}"
                f"\n\tMESSAGE: {message}\n"
            ),
            args=())

        cls.__threads_list.append(thread)
        thread.start()

    @classmethod
    def critical(cls, message):
        current_stack = stack()[1]

        thread = Thread(
            target=lambda: cls.__logger_thread.critical(
                f"\n\tFILE NAME: {basename(current_stack.filename)}"
                f"\n\tFUNC NAME: {current_stack.function}"
                f"\n\tLINE NUMBER: {current_stack.lineno}"
                f"\n\tMESSAGE: {message}\n"
            ),
            args=())

        cls.__threads_list.append(thread)
        thread.start()
