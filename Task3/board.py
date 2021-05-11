"""
Module for board for playing tic-tac-toe!
"""
from copy import deepcopy
from btree import LinkedBinaryTree


class Board:
    """
    Class for representing a board for playing tic-tac-toe.
    """
    COMPUTER_MOVE = '0'
    PLAYER_MOVE = 'x'

    def __init__(self):
        """
        Initialize a board for game.
        """
        self._positions = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self._last_move = None

    def __str__(self):
        """
        Print a board.
        """
        info = ''
        for row in self._positions:
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
        for player in [self.COMPUTER_MOVE, self.PLAYER_MOVE]:
            if self.check_win(self._positions, player):
                return player
        for row in self._positions:
            if ' ' in row:
                return 'continue'
        return 'draw'

    def make_move(self, position: tuple, turn: str):
        """
        Checks if it is possible to make a move and makes it (if not, raises IndexError).
        """
        if turn != self.COMPUTER_MOVE and turn != self.PLAYER_MOVE:
            raise IndexError
        if position[0] > 2 or position[0] < 0 or position[1] > 2 or position[1] < 0:
            raise IndexError
        if self._positions[position[0]][position[1]] != ' ':
            raise IndexError
        self._positions[position[0]][position[1]] = turn
        self._last_move = turn

    def person_move(self):
        """
        Additional method for managing person's moves.
        """
        move = input(
            "Please enter your next move (row and column, separated by space): ")
        good_move = False
        move = move.split(' ')
        while not good_move:
            try:
                self.make_move((int(move[0]), int(move[1])), self.PLAYER_MOVE)
                good_move = True
            except IndexError:
                move = input("Incorrect move! Try again: ")
                move = move.split(' ')

    def possibilities(self):
        """
        Return list of possible moves on board (each is a tuple of indexes).
        """
        possible_list = []
        for itr, row in enumerate(self._positions):
            for itrr, elem in enumerate(row):
                if elem == ' ':
                    possible_list.append((itr, itrr))
        return possible_list

    @staticmethod
    def _row_win(board: list, player: str):
        """
        Check if given player won a game by row-rule.
        """
        for i in range(len(board)):
            if board[i][0] == board[i][1] == board[i][2] == player:
                return True
        return False

    @staticmethod
    def _col_win(board: list, player: str):
        """
        Check if given player won a game by column-rule.
        """
        for i in range(len(board)):
            if board[0][i] == board[1][i] == board[2][i] == player:
                return True
        return False

    @staticmethod
    def _diag_win(board: list, player: str):
        """
        Check if given player won a game by diagonal-rule.
        """
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[2][0] == board[1][1] == board[0][2] == player:
            return True
        return False

    def check_win(self, board: list, player: str):
        """
        Check if given player won a game.
        """
        if self._row_win(board, player) or self._col_win(board, player) or\
                self._diag_win(board, player):
            return True
        return False

    def make_computer_move(self):
        """
        Make move for computer.
        """
        self._positions = self.build_tree(self)._positions
        self._last_move = self.COMPUTER_MOVE

    def build_tree(self, board):
        """
        Building trees with boards, finding the best option.
        """
        tree = LinkedBinaryTree(board)

        def recurse(board, tree):
            """
            Recursive function for building a tree.
            """
            possible_moves = board.possibilities()
            if len(possible_moves) == 1:
                position = possible_moves[0]
                left_board = deepcopy(board)
                right_board = deepcopy(board)
                if board._last_move == self.PLAYER_MOVE:
                    left_board._positions[position[0]
                                          ][position[1]] = self.COMPUTER_MOVE
                    right_board._positions[position[0]
                                           ][position[1]] = self.COMPUTER_MOVE
                if board._last_move == self.COMPUTER_MOVE:
                    left_board._positions[position[0]
                                          ][position[1]] = self.PLAYER_MOVE
                    right_board._positions[position[0]
                                           ][position[1]] = self.PLAYER_MOVE
                tree.insert_left(left_board)
                tree.insert_right(right_board)
                return
            else:
                left_position = possible_moves[0]
                right_position = possible_moves[1]
                left_board = deepcopy(board)
                right_board = deepcopy(board)
                if board._last_move == self.PLAYER_MOVE:
                    new_move = self.COMPUTER_MOVE
                else:
                    new_move = self.PLAYER_MOVE
                left_board._positions[left_position[0]
                                      ][left_position[1]] = new_move
                right_board._positions[right_position[0]
                                       ][right_position[1]] = new_move
                left_board._last_move = new_move
                right_board._last_move = new_move
                tree.insert_left(left_board)
                tree.insert_right(right_board)
                recurse(left_board, tree.get_left())
                recurse(right_board, tree.get_right())

        recurse(board, tree)
        left_points = self.get_points(tree.get_left())
        right_points = self.get_points(tree.get_right())
        if left_points > right_points:
            return tree.get_left().data
        return tree.get_right().data

    def get_points(self, tree):
        """
        Count points in subtrees.
        """
        count = 0

        def points_recurse(tree, count):
            """
            Recursively count points in tree.
            """
            board = tree.data
            if board.get_status() == 'continue':
                count += points_recurse(tree.left, count)
                count += points_recurse(tree.right, count)
                return count
            elif board.get_status() == self.COMPUTER_MOVE:
                count += 1
                return count
            elif board.get_status() == self.PLAYER_MOVE:
                count -= 1
                return count
            else:
                return count

        return points_recurse(tree, count)
