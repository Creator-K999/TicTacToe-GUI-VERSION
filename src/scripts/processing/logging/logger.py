from queue import Queue
from threading import Lock, Thread
from logging import getLogger, config


class Logger:

    __instance = None
    __log_queue = Queue()

    def __init__(self):
        self.__lock = Lock()

        config.fileConfig(fname="logger.config")
        self.__logger = getLogger(__name__)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)

        return cls.__instance

    @property
    def log_queue(self):
        with self.__lock:
            return self.__log_queue

    def debug(self, **kwargs):
        thread = Thread(
            name=f"{kwargs['function']} - Thread from {kwargs['filename']} - line No. {kwargs['line']}",
            target=lambda: self.__logger.debug(
                f"\n\tFILE NAME: {kwargs['filename']}"
                f"\n\tFUNC NAME: {kwargs['function']}"
                f"\n\tLINE NUMBER: {kwargs['line']}"
                f"\n\tMESSAGE: {kwargs['message']}\n"
            ),
            args=())

        thread.daemon = True
        self.__log_queue.put(thread)

    def info(self, **kwargs):
        thread = Thread(
            name=f"{kwargs['function']} - Thread from {kwargs['filename']} - line No. {kwargs['line']}",
            target=lambda: self.__logger.info(
                f"\n\tFILE NAME: {kwargs['filename']}"
                f"\n\tFUNC NAME: {kwargs['function']}"
                f"\n\tLINE NUMBER: {kwargs['line']}"
                f"\n\tMESSAGE: {kwargs['message']}\n"
            ),
            args=())

        thread.daemon = True
        self.__log_queue.put(thread)

    def warning(self, **kwargs):
        thread = Thread(
            name=f"{kwargs['function']} - Thread from {kwargs['filename']} - line No. {kwargs['line']}",
            target=lambda: self.__logger.warning(
                f"\n\tFILE NAME: {kwargs['filename']}"
                f"\n\tFUNC NAME: {kwargs['function']}"
                f"\n\tLINE NUMBER: {kwargs['line']}"
                f"\n\tMESSAGE: {kwargs['message']}\n"
            ),
            args=())

        thread.daemon = True
        self.__log_queue.put(thread)

    def error(self, **kwargs):
        thread = Thread(
            name=f"{kwargs['function']} - Thread from {kwargs['filename']} - line No. {kwargs['line']}",
            target=lambda: self.__logger.error(
                f"\n\tFILE NAME: {kwargs['filename']}"
                f"\n\tFUNC NAME: {kwargs['function']}"
                f"\n\tLINE NUMBER: {kwargs['line']}"
                f"\n\tMESSAGE: {kwargs['message']}\n"
            ),
            args=())

        thread.daemon = True
        self.__log_queue.put(thread)

    def exception(self, **kwargs):
        thread = Thread(
            name=f"{kwargs['function']} - Thread from {kwargs['filename']} - line No. {kwargs['line']}",
            target=lambda: self.__logger.exception(
                f"\n\tFILE NAME: {kwargs['filename']}"
                f"\n\tFUNC NAME: {kwargs['function']}"
                f"\n\tLINE NUMBER: {kwargs['line']}"
                f"\n\tMESSAGE: {kwargs['message']}\n"
            ),
            args=())

        thread.daemon = True
        self.__log_queue.put(thread)

    def critical(self, **kwargs):
        thread = Thread(
            name=f"{kwargs['function']} - Thread from {kwargs['filename']} - line No. {kwargs['line']}",
            target=lambda: self.__logger.critical(
                f"\n\tFILE NAME: {kwargs['filename']}"
                f"\n\tFUNC NAME: {kwargs['function']}"
                f"\n\tLINE NUMBER: {kwargs['line']}"
                f"\n\tMESSAGE: {kwargs['message']}\n"
            ),
            args=())

        thread.daemon = True
        self.__log_queue.put(thread)
