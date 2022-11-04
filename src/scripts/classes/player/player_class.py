from processing.management.logger.logger import Log


class Player:

    def __init__(self, object_name, username, password, mark=None, score=0):

        self.__object_name = object_name
        self.__username = username
        self.__password = password
        self.__mark = mark
        self.__score = score

    def __repr__(self):
        return f"Player({self.__object_name}, {self.__username}, {self.__password}, {self.__mark}, {self.__score})"

    def __str__(self):
        return f"{self.__object_name}({self.__username}, {self.__password}, {self.__mark}, {self.__score})"

#
#   PUBLIC SECTION
#
    @property
    def object_name(self):
        return self.__object_name

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username) -> None:

        if not isinstance(username, str) or len(username) == 0:
            Log.error(f"Expected a non-empty str, got '{type(username)}' instead!")
            return

        self.__username = username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def mark(self):
        return self.__mark

    @property
    def score(self):
        return self.__score

    @mark.setter
    def mark(self, value):

        if value not in {'X', 'O'}:
            Log.error(f"value has to be a either X or O. Got '{value}' instead!")

        else:
            self.__mark = value

    @score.setter
    def score(self, value):

        if not isinstance(value, int):
            Log.error("Tried to set score to a non-int value!")

        else:
            self.__score = value

    def increment_score(self):
        self.__score += 1
