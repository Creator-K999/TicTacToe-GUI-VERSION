class Player:

    def __init__(self, name, mark, score=0):

        self.__name = name
        self.__mark = mark
        self.__score = score

    def __str__(self):

        return f"Player({self.__name}, {self.__mark}, {self.__score})"

#
#   PUBLIC SECTION
#
    @property
    def name(self):
        return self.__name

    @property
    def mark(self):
        return self.__mark

    @property
    def score(self):
        return self.__score

    def increment_score(self):
        self.__score += 1
