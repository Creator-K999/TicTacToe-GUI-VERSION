from os import chdir, getcwd
from threading import Lock
from logging import getLogger, config, basicConfig


class Logger:

    __instance = None

    def __init__(self):
        self.__lock = Lock()

        print("Called!")
        cwd = getcwd()
        chdir("..\\..")

        config.fileConfig(fname=f"logger.config")
        print("Reached!")
        self.__logger = getLogger(__name__)

        chdir(cwd)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)

        return cls.__instance

    @staticmethod
    def set_level(level_name) -> None:
        basicConfig(level=level_name)

    @property
    def debug(self):
        print("Debug Called")
        with self.__lock:
            print("Debug Acquired!")
            return self.__logger.debug

    @property
    def info(self):
        print("Info Called")
        with self.__lock:
            print("Info Acquired!")
            return self.__logger.info

    @property
    def warning(self):
        with self.__lock:
            return self.__logger.warning

    @property
    def exception(self):
        with self.__lock:
            return self.__logger.exception

    @property
    def critical(self):
        with self.__lock:
            return self.__logger.critical
