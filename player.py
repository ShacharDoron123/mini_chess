import random
from abc import ABC, abstractmethod
from constants import *


class Player(ABC):
    """Base class for all the players. It holds the player's color and the board.

    Game uses every player in the same way (it asks for a move), so it does not need to know which
    kind of player it is. This is why Player is an abstract class.
    """

    def __init__(self, color, board):
        """Save the color of the player (WHITE or BLACK) and the board.

        The color is needed to know which pieces belong to the player.
        """
        self.color = color
        self.board = board

    @abstractmethod
    def get_player_move(self, legal_moves):
        """Choose the next move.

        legal_moves: the list of all the legal moves of this player (each move is [from_pos, to_pos]).
        Game calculates it once in every turn and gives it to the player.
        Every player class must write its own version.
        Returns two positions: from_pos and to_pos.
        """
        pass


class HumanPlayer(Player):
    """A player that is a person who types the moves."""

    def get_player_move(self, legal_moves):
        """Ask the user for a move until a legal one is typed.

        legal_moves: the list of the legal moves, used to check the move that the user typed.
        The user types the row and the column of the start square and of the target square. If the move is
        not in the list, an error message is printed and the user is asked again.
        Returns from_pos and to_pos.
        """
        while True:
            from_row = int(input(f"Enter from row (0-{BOARD_ROWS - 1}): "))
            from_col = int(input(f"Enter from col (0-{BOARD_COLS - 1}): "))

            to_row = int(input(f"Enter to row (0-{BOARD_ROWS-1}): "))
            to_col = int(input(f"Enter to col (0-{BOARD_COLS-1}): "))

            from_pos = [from_row,from_col]
            to_pos = [to_row,to_col]

            if [from_pos,to_pos] in legal_moves:
                return from_pos, to_pos

            print("Invalid move. Try again!")


class RandomPlayer(Player):
    """A computer player that plays a random legal move."""

    def get_player_move(self, legal_moves):
        """Choose a random move from the legal moves.

        legal_moves: the list of the legal moves (calculated by Game). Every legal move has the same chance.
        The list must not be empty, and Game makes sure of that (an empty list is a tie) before it calls
        this function.
        Returns from_pos and to_pos.
        """
        move = random.choice(legal_moves)
        from_pos, to_pos = move

        return from_pos, to_pos