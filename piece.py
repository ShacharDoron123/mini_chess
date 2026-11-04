from abc import ABC, abstractmethod
from constants import *


class Piece(ABC):
    def __init__(self, piece_type, color, board):
        self.type = piece_type
        self.color = color
        self.board = board


    @abstractmethod
    def is_move_valid(self, from_pos, to_pos):
        pass


class Pawn(Piece):
    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
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


class Knight(Piece):
    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
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
    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
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
    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
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
    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        rook = Rook(self.type, self.color, self.board)
        bishop = Bishop(self.type, self.color, self.board)

        if rook.is_move_valid(from_pos, to_pos):
            return True

        if bishop.is_move_valid(from_pos, to_pos):
            return True

        return False


class King(Piece):
    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
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
    if str(letter).islower():
        color = BLACK
    else:
        color = WHITE
    return PIECE_CLASSES[letter](letter,color,board )







