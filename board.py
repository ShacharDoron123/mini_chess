import numpy as np
from constants import *
from piece import create_piece_from_letter


class Board:

    def __init__(self):
        self.game_board = np.full((BOARD_ROWS,BOARD_COLS),EMPTY)
        self.game_board[0] = [BLACK_ROOK, BLACK_KNIGHT, BLACK_KING, BLACK_BISHOP, BLACK_QUEEN]
        self.game_board[1, :] = BLACK_PAWN
        self.game_board[3, :] = WHITE_PAWN
        self.game_board[4] = [WHITE_ROOK, WHITE_KNIGHT, WHITE_KING, WHITE_BISHOP, WHITE_QUEEN]

    def print_board(self):
        print(" "+" ---"*BOARD_COLS)
        for row in range(BOARD_ROWS):
            print(" | ", end="")
            for col in range(BOARD_COLS):
                print(self.game_board[row,col], end="")
                print(" | ", end="")
            print()

        print(" "+" ---"*BOARD_COLS)

    def is_empty(self,pos):
        row,col = pos

        return self.game_board[row,col] == EMPTY

    def get_color(self, pos):
        row, col = pos
        if self.game_board[row,col] == EMPTY:
            return EMPTY
        if str(self.game_board[row,col]).islower():
            return BLACK

        return WHITE

    def perform_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if not self.game_board[from_row,from_col] == EMPTY:
            letter = self.game_board[from_row, from_col]
            piece = create_piece_from_letter(letter,self)
            if not piece.is_move_valid(from_pos, to_pos):
                return False
        else:
            return False

        self.game_board[to_row,to_col] = self.game_board[from_row,from_col]
        self.game_board[from_row,from_col] = EMPTY

        return True

    def is_inside(self, pos):
        row, col = pos
        return  BOARD_COLS -1 >= col >= 0 and BOARD_ROWS -1  >= row >= 0

    def is_path_clear(self, from_pos, to_pos):
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
        if color == WHITE:
            king = WHITE_KING
        else:
            king = BLACK_KING

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.game_board[row,col] == king:
                    return True
        return False

    def copy(self):
        new_board = Board()
        new_board.game_board = self.game_board.copy()
        return new_board








