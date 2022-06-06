from processing.management.logger.logger_threads_manager import LoggerThreadManager


class Player2:

    def __init__(self, game_name, name, _pass, mark, score=0):

        self.__game_name = game_name
        self.__name = name
        self.__pass = _pass
        self.__mark = mark
        self.__score = score

    def __str__(self):

        return f"Player({self.__name}, {self.__mark}, {self.__score})"

#
#   PUBLIC SECTION
#
    @property
    def game_name(self):
        return self.__game_name

    @property
    def name(self):
        return self.__name

    @property
    def mark(self):
        return self.__mark

    @property
    def score(self):
        return self.__score

    @mark.setter
    def mark(self, value):

        try:
            if not isinstance(value, str) or value not in frozenset({'X', 'O'}):
                raise ValueError(f"value has to be a either X or O. Got {value!r} instead!")

        except ValueError:
            LoggerThreadManager.exception("Error!")

        else:
            self.__mark = value

    def increment_score(self):
        self.__score += 1
