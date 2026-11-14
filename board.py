import numpy as np
from constants import *
from piece import create_piece_from_letter


class Board:
    """The game board: a 5x5 array of letters. It knows where the pieces are and moves them."""

    def __init__(self):
        """Create a board with the pieces in their starting places."""
        self.game_board = np.full((BOARD_ROWS,BOARD_COLS),EMPTY)
        self.game_board[0] = [BLACK_ROOK, BLACK_KNIGHT, BLACK_KING, BLACK_BISHOP, BLACK_QUEEN]
        self.game_board[1, :] = BLACK_PAWN
        self.game_board[3, :] = WHITE_PAWN
        self.game_board[4] = [WHITE_ROOK, WHITE_KNIGHT, WHITE_KING, WHITE_BISHOP, WHITE_QUEEN]

    def print_board(self):
        """Print the board to the screen."""
        print(" "+" ---"*BOARD_COLS)
        for row in range(BOARD_ROWS):
            print(" | ", end="")
            for col in range(BOARD_COLS):
                print(self.game_board[row,col], end="")
                print(" | ", end="")
            print()

        print(" "+" ---"*BOARD_COLS)

    def is_empty(self,pos):
        """Check if a square is empty.

        pos: the square as [row, col].
        Returns True if there is no piece on it, otherwise False.
        """
        row,col = pos

        return self.game_board[row,col] == EMPTY

    def get_color(self, pos):
        """Find the color of the piece on a square.

        pos: the square as [row, col].
        Returns WHITE or BLACK (uppercase letter = white, lowercase = black),
        or EMPTY if the square has no piece.
        """
        row, col = pos
        if self.game_board[row,col] == EMPTY:
            return EMPTY
        if str(self.game_board[row,col]).islower():
            return BLACK

        return WHITE

    def perform_move(self, from_pos, to_pos):
        """Move a piece from one square to another.

        If there is an enemy piece on the target square, it is captured.
        A pawn that reaches the last row becomes a queen.
        Note: this function does NOT check the move, so call is_move_valid first.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        self.game_board[to_row,to_col] = self.game_board[from_row,from_col]
        self.game_board[from_row,from_col] = EMPTY

        piece = create_piece_from_letter(self.game_board[to_row,to_col],self)

        if piece.is_promotion_move(to_pos):
            if self.get_color(to_pos) == WHITE:
                self.game_board[to_row,to_col] = WHITE_QUEEN
            else:
                self.game_board[to_row,to_col] = BLACK_QUEEN


    def is_inside(self, pos):
        """Check if a square is on the board.

        pos: the square as [row, col].
        Returns True if it is inside the board, otherwise False.
        """
        row, col = pos
        return  BOARD_COLS -1 >= col >= 0 and BOARD_ROWS -1  >= row >= 0

    def is_path_clear(self, from_pos, to_pos):
        """Check that there are no pieces between two squares.

        Only the squares between them are checked (not the start and end squares).
        Works for a straight line or a diagonal.
        Returns True if the path is clear, otherwise False.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        if row_diff > 0:
            row_step = 1
        elif row_diff < 0:
            row_step = -1
        else:
            row_step = 0

        if col_diff > 0:
            col_step = 1
        elif col_diff < 0:
            col_step = -1
        else:
            col_step = 0

        row = from_row + row_step
        col = from_col + col_step

        while row != to_row or col != to_col:
            if self.game_board[row, col] != EMPTY:
                return False
            row += row_step
            col += col_step

        return True

    def is_king_alive(self, color):
        """Check if the king of a color is still on the board.

        color: WHITE or BLACK.
        Returns True if the king is on the board, otherwise False.
        """
        if color == WHITE:
            king = WHITE_KING
        else:
            king = BLACK_KING

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.game_board[row,col] == king:
                    return True
        return False

    def is_move_valid(self, from_pos, to_pos, color):
        """Check if a player of the given color can make this move.

        The start square must be inside the board and hold a piece of that color,
        and the move must follow the rules of that piece.
        Returns True if the move is legal, otherwise False.
        """
        from_row, from_col = from_pos

        if not self.is_inside(from_pos):
            return False

        if self.get_color(from_pos) != color:
            return False

        letter = self.game_board[from_row, from_col]
        piece = create_piece_from_letter(letter, self)

        return piece.is_move_valid(from_pos, to_pos)

    def get_legal_moves(self, color):
        """Find all the legal moves of a color.

        Returns a list of moves, and each move is [from_pos, to_pos].
        The list is empty if the player has no legal move.
        """
        legal_moves = []
        for from_row in range(BOARD_ROWS):
            for from_col in range(BOARD_COLS):
                if self.get_color([from_row, from_col]) == color:
                    from_pos = [from_row, from_col]
                    for to_row in range(BOARD_ROWS):
                        for to_col in range(BOARD_COLS):
                            to_pos = [to_row,to_col]
                            if self.is_move_valid(from_pos,to_pos, color):
                                legal_moves.append([from_pos,to_pos])
        return legal_moves

    def copy(self):
        """Return a new Board with the same pieces in the same places."""
        new_board = Board()
        new_board.game_board = self.game_board.copy()
        return new_board