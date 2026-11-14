import random
from abc import ABC, abstractmethod
from constants import *


class Player(ABC):
    """Base class for all the players. It holds the player's color and the board."""

    def __init__(self, color, board):
        """Save the color of the player (WHITE or BLACK) and the board."""
        self.color = color
        self.board = board

    @abstractmethod
    def get_player_move(self):
        """Choose the next move.

        Every player class must write its own version.
        Returns two positions: from_pos and to_pos.
        """
        pass


class HumanPlayer(Player):
    """A player that is a person who types the moves."""

    def get_player_move(self):
        """Ask the user for a move until a legal one is typed.

        The user types the row and column of the start square and of the target square.
        Returns from_pos and to_pos.
        """
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
    """A computer player that plays a random legal move."""

    def get_player_move(self):
        """Choose a random move from all the legal moves.

        Returns from_pos and to_pos.
        """
        legal_moves = self.board.get_legal_moves(self.color)
        move = random.choice(legal_moves)
        from_pos, to_pos = move

        return from_pos, to_pos