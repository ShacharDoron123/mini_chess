import random
from abc import ABC, abstractmethod
from constants import *


class Player(ABC):
    def __init__(self, color, board):
        self.color = color
        self.board = board

    @abstractmethod
    def get_player_move(self):
        pass


class HumanPlayer(Player):
    def get_player_move(self):
        while True:
            from_row = int(input(f"Enter from row (0-{BOARD_ROWS - 1}): "))
            from_col = int(input(f"Enter from col (0-{BOARD_COLS - 1}): "))

            to_row = int(input(f"Enter to row (0-{BOARD_ROWS-1}): "))
            to_col = int(input(f"Enter to col (0-{BOARD_COLS-1}): "))

            from_pos = [from_row,from_col]
            to_pos = [to_row,to_col]

            if self.board.is_move_valid(from_pos, to_pos, self.color):
                return from_pos, to_pos

            print("Invalid move. Try again!")


class RandomPlayer(Player):
    def get_player_move(self):
        legal_moves = self.board.get_legal_moves(self.color)
        move = random.choice(legal_moves)
        from_pos, to_pos = move

        return from_pos, to_pos