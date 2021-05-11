"""
Main module for playing tic-tac-toe!
"""
from board import Board


class Game:
    """
    Class representing game itself.
    """

    def play(self):
        """
        Main function for playing a game.
        """
        board = Board()
        print("Let's play tic-tac-toe against computer!")
        print("Here is your board!")
        count = 1
        print(board)
        while True:
            board.person_move()
            status = board.get_status()
            if status == 'x' or status == '0':
                return(f"Winner is {status}")
            elif status == 'draw':
                return("Friendship won!")
            board.make_computer_move()
            status = board.get_status()
            if status == 'x' or status == '0':
                return(f"Winner is {status}")
            elif status == 'draw':
                return("Friendship won!")
            print(f"Board after {count} action.")
            count += 1
            print(board)


if __name__ == '__main__':
    game = Game()
    print(game.play())
