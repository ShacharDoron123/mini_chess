from abc import ABC, abstractmethod

from constants import *


class Piece(ABC):
    """Base class for all the pieces. It holds the piece letter, its color and the board."""

    def __init__(self, piece_type, color, board):
        """Save the piece letter, its color (WHITE or BLACK) and the board it plays on."""
        self.type = piece_type
        self.color = color
        self.board = board


    @abstractmethod
    def is_move_valid(self, from_pos, to_pos):
        """Check if the move follows the rules of this piece.

        Every piece class must write its own version.
        Returns True if the move is legal, otherwise False.
        """
        pass

    def is_promotion_move(self,to_pos):
        """Check if this move turns the piece into a queen.

        For most pieces the answer is always False. Only the Pawn changes it.
        """
        return False


class Pawn(Piece):
    """A pawn: moves one step forward and captures one step diagonally forward."""

    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        """Check a pawn move.

        White moves up and black moves down.
        One step forward is allowed only to an empty square.
        A diagonal step forward is allowed only to capture an enemy piece.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        if not self.board.is_inside(to_pos):
            return False

        if self.color == WHITE:
            if row_diff == -1 and col_diff == 0 and self.board.is_empty(to_pos):
                return True

            if (row_diff == -1 and col_diff == -1 or row_diff == -1 and col_diff == 1) and not self.board.is_empty(to_pos) and self.board.get_color(to_pos) != self.color:
                return True

            return False

        else:
            if row_diff == 1 and col_diff == 0 and self.board.is_empty(to_pos):
                return True

            if (row_diff == 1 and col_diff == -1 or row_diff == 1 and col_diff == 1) and not self.board.is_empty(to_pos) and  self.board.get_color(to_pos) != self.color:
                return True

            return False

    def is_promotion_move(self, to_pos):
        """Return True if the target square is in the first or the last row of the board."""
        to_row, to_col = to_pos
        if to_row == 0 or to_row == BOARD_ROWS-1:
            return True
        return False



class Knight(Piece):
    """A knight: jumps in an L shape and can jump over other pieces."""

    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        """Check a knight move: two squares in one direction and one in the other.

        The target must not hold a piece of the same color.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        if not self.board.is_inside(to_pos):
            return False

        if not self.board.is_empty(to_pos) and self.board.get_color(to_pos) == self.color:
            return False

        if abs(row_diff) == 1 and abs(col_diff) == 2 or abs(row_diff) == 2 and abs(col_diff) == 1:
            return True

        return False


class Bishop(Piece):
    """A bishop: moves diagonally."""

    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        """Check a bishop move: any number of squares diagonally with a clear path.

        The target must not hold a piece of the same color.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        if not self.board.is_inside(to_pos):
            return False

        if row_diff == 0 or col_diff == 0:
            return False

        if abs(row_diff) != abs(col_diff):
            return False

        if not self.board.is_path_clear(from_pos,to_pos):
            return False

        if not self.board.is_empty(to_pos) and self.board.get_color(to_pos) == self.color:
            return False

        return True


class Rook(Piece):
    """A rook: moves in a straight line (a row or a column)."""

    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        """Check a rook move: any number of squares in a row or a column with a clear path.

        The target must not hold a piece of the same color.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        if not self.board.is_inside(to_pos):
            return False

        if abs(row_diff) > 0 and col_diff == 0 and (self.board.is_empty(to_pos) or self.board.get_color(to_pos) != self.color) and self.board.is_path_clear(from_pos,to_pos):
            return True

        if row_diff == 0 and abs(col_diff) > 0 and (self.board.is_empty(to_pos) or self.board.get_color(to_pos) != self.color) and self.board.is_path_clear(from_pos,to_pos):
            return True

        return False


class Queen(Piece):
    """A queen: moves like a rook and like a bishop."""

    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        """Check a queen move.

        It creates a temporary rook and bishop of the same color
        and returns True if one of them can make the move.
        """
        rook = Rook(self.type, self.color, self.board)
        bishop = Bishop(self.type, self.color, self.board)

        if rook.is_move_valid(from_pos, to_pos):
            return True

        if bishop.is_move_valid(from_pos, to_pos):
            return True

        return False


class King(Piece):
    """A king: moves one step in any direction."""

    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        """Check a king move: one square in any direction.

        The target must not hold a piece of the same color.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        if not self.board.is_inside(to_pos):
            return False

        if not (abs(row_diff) <= 1 and abs(col_diff) <= 1 and (row_diff != 0 or col_diff != 0)):
            return False

        if self.board.is_empty(to_pos) or self.board.get_color(to_pos) != self.color:
            return True

        return False


PIECE_CLASSES = {
    WHITE_PAWN: Pawn,
    BLACK_PAWN: Pawn,
    WHITE_KNIGHT: Knight,
    BLACK_KNIGHT: Knight,
    WHITE_BISHOP: Bishop,
    BLACK_BISHOP: Bishop,
    WHITE_ROOK: Rook,
    BLACK_ROOK: Rook,
    WHITE_QUEEN: Queen,
    BLACK_QUEEN: Queen,
    WHITE_KING: King,
    BLACK_KING: King,
}

def create_piece_from_letter(letter, board):
    """Create the piece object that matches a letter on the board.

    The letter decides the type (for example "N" is a Knight)
    and the color (uppercase = white, lowercase = black).
    Returns the new piece object.
    """
    if str(letter).islower():
        color = BLACK
    else:
        color = WHITE
    return PIECE_CLASSES[letter](letter,color,board )