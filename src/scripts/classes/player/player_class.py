from processing.management.logger.logger import Log


class Player:

    def __init__(self, game_name, name, mark=None, score=0):

        self.__game_name = game_name
        self.__name = name
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
    def name(self) -> str:
        return self.__name

    @property
    def mark(self):
        return self.__mark

    @property
    def score(self):
        return self.__score

    @mark.setter
    def mark(self, value):

        if not isinstance(value, str) or value not in frozenset({'X', 'O'}):
            Log.error("value has to be a either X or O. Got '{value}' instead!")

        else:
            self.__mark = value

    @score.setter
    def score(self, value):

        if not isinstance(value, int):
            Log.error("Tried to set score to a non-int value!")

        else:
            self.__score = value

    def increment_score(self):
        Log.info(f"Incrementing {self.__name} score by 1")
        self.__score += 1
