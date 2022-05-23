"""
This is a GUI version of the famous TicTacToe game.
It contains 3 modes to play.

    //
        1- Vs. Local: 1v1 local gameplay.
        2- Vs. Local Network: 1v1 on a local network gameplay.
        3- Vs. AI: Play vs undefeatable AI made by python using minimax algorithm.
    //

Made by: Ahmed Zaki Marei.
Last Modified Date: 23/05/2022
Version: 0.3
"""

# Custom Libs
from src.mscripts.main_class import MainClass


def main():

    """
    This is the main function, the program starts from here!
    """

    main_class = MainClass()
    main_class.run()


if __name__ == "__main__":
    main()
