"""
Module for board for playing tic-tac-toe!
"""


class Board:
    """
    Class for representing a board for playing tic-tac-toe.
    """
    COMPUTER_MOVE = 'x'
    PLAYER_MOVE = '0'

    def __init__(self):
        """
        Initialize a board for game.
        """
        self._board = [['', '', ''], ['', '', ''], ['', '', '']]
        self._last_move = None

    def __str__(self):
        """
        Print a board.
        """
        info = ''
        for row in self._board:
            info += '['
            for elem in row:
                info += f"'{elem}', "
            info = info[:-2]
            info += ']\n'
        info = info[:-1]
        return info

    def get_status(self):
        """
        Return info about state on board: draw, win or continuing of game.
        """
        pass

    def make_move(self, position: tuple, turn: str):
        """
        Checks if it possible to make a move and makes it (if not, raises IndexError).
        """
        if turn != self.COMPUTER_MOVE and turn != self.PLAYER_MOVE:
            raise IndexError
        if position[0] > 2 or position[0] < 0 or position[1] > 2 or position[1] < 0:
            raise IndexError
        if self._board[position[0]][position[1]] != ' ':
            raise IndexError
        self._board[position[0]][position[1]] = turn

    def check_win

    def make_computer_move(self):
        """
        """
        pass
