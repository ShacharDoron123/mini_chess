from abc import ABC, abstractmethod

from constants import *


class Piece(ABC):
    """Base class for all the pieces.

    A piece holds its letter, its color and the board it plays on. A piece only knows the rules of its
    own movement and never changes the board (the Board moves the pieces). Piece objects are created by
    create_piece_from_letter when the board needs to check a move.
    """

    def __init__(self, piece_type, color, board):
        """Save the piece letter, its color (WHITE or BLACK) and the board it plays on.

        The board is saved so that the piece can ask it questions while it checks a move,
        for example is_empty, get_color and is_inside.
        """
        self.type = piece_type
        self.color = color
        self.board = board


    @abstractmethod
    def is_move_valid(self, from_pos, to_pos):
        """Check if the move follows the rules of this piece.

        from_pos, to_pos: the squares as [row, col].
        Every piece class must write its own version (this is what makes the class abstract).
        Returns True if the move is legal, otherwise False.

        Used by Board.get_legal_moves and Board.is_move_valid.
        """
        pass

    def is_promotion_move(self,to_pos):
        """Check if this move turns the piece into a queen.

        to_pos: the target square as [row, col].
        For most pieces the answer is always False, so the Board can ask any piece after a move without
        checking its type. Only the Pawn changes this answer.

        Used by Board.perform_move.
        """
        return False


class Pawn(Piece):
    """A pawn: moves one step forward and captures one step diagonally forward.

    White moves up (the row number gets smaller) and black moves down. There is no double step and
    no en passant. A pawn that reaches the last row becomes a queen.
    """

    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        """Check a pawn move.

        from_pos, to_pos: the squares as [row, col].
        White moves up and black moves down. One step forward is allowed only to an empty square.
        A diagonal step forward is allowed only to capture an enemy piece. Any other move is not legal.
        Returns True if the move is legal, otherwise False.
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
        """Return True if the target square is in the first or the last row of the board.

        to_pos: the target square as [row, col].
        A pawn can only move forward, so a white pawn that reaches row 0 and a black pawn that reaches the
        last row must be promoted. The Board then replaces the pawn with a queen.
        """
        to_row, to_col = to_pos
        if to_row == 0 or to_row == BOARD_ROWS-1:
            return True
        return False



class Knight(Piece):
    """A knight: jumps in an L shape and can jump over other pieces."""

    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        """Check a knight move.

        from_pos, to_pos: the squares as [row, col].
        The move must be two squares in one direction and one square in the other direction. The knight
        jumps, so the squares between are not checked. The target must not hold a piece of the same color.
        Returns True if the move is legal, otherwise False.
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
        """Check a bishop move.

        from_pos, to_pos: the squares as [row, col].
        The move must be diagonal (the row and the column change by the same number of squares, and the
        piece must really move), and the path must be clear (is_path_clear). The target must not hold a
        piece of the same color.
        Returns True if the move is legal, otherwise False.
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
        """Check a rook move.

        from_pos, to_pos: the squares as [row, col].
        The move must stay in the same row or in the same column, and the path must be clear
        (is_path_clear). The target must not hold a piece of the same color.
        Returns True if the move is legal, otherwise False.
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

        from_pos, to_pos: the squares as [row, col].
        It creates a temporary Rook and a temporary Bishop of the same color and returns True if one of them
        can make the move. This way the rules of the straight and the diagonal movement are not written twice.
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
        """Check a king move.

        from_pos, to_pos: the squares as [row, col].
        The move must be one square in any direction (also diagonally), and the king must really move.
        The target must not hold a piece of the same color.
        Returns True if the move is legal, otherwise False.
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

    letter: a letter from the board, for example "N". board: the Board the piece will play on.
    The letter decides the type of the piece (for example "N" is a Knight) and its color
    (an uppercase letter is white and a lowercase letter is black).
    Returns the new piece object.

    Why it is needed: the board stores only letters, but checking a move needs an object that knows the
    rules of the piece. A separate function means that the Board does not need to know all the piece
    classes (this is called a factory function). Used by Board.get_legal_moves, Board.is_move_valid and
    Board.perform_move.
    """
    if str(letter).islower():
        color = BLACK
    else:
        color = WHITE
    return PIECE_CLASSES[letter](letter,color,board )