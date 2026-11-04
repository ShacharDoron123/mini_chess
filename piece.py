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





class Bishop(Piece):
    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        pass


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
        pass


class King(Piece):
    def __init__(self, piece_type, color, board):
        super().__init__(piece_type, color, board)

    def is_move_valid(self, from_pos, to_pos):
        pass







