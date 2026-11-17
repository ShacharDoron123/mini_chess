import numpy as np
from constants import *
from piece import create_piece_from_letter


class Board:
    """The game board: a 5x5 array of letters.

    The board knows which piece stands on every square, moves the pieces, and answers questions such as
    "is this square empty?" or "which moves are legal?". The Piece classes only check the rules of
    movement, and the Board is the only class that changes the array.
    """

    def __init__(self):
        """Create a board with the pieces in their starting places.

        The board is a numpy array of letters: an uppercase letter is a white piece, a lowercase letter is
        a black piece, and EMPTY means there is no piece. Row 0 is the black side and row 4 is the white
        side. It is called once for every game, by Game.__init__.
        """
        self.game_board = np.full((BOARD_ROWS,BOARD_COLS),EMPTY)
        self.game_board[0] = [BLACK_ROOK, BLACK_KNIGHT, BLACK_KING, BLACK_BISHOP, BLACK_QUEEN]
        self.game_board[1, :] = BLACK_PAWN
        self.game_board[3, :] = WHITE_PAWN
        self.game_board[4] = [WHITE_ROOK, WHITE_KNIGHT, WHITE_KING, WHITE_BISHOP, WHITE_QUEEN]

    def print_board(self):
        """Print the board to the screen, with a frame around it.

        The Game calls it after every move (only if show_board is True), so that the user can follow the game.
        """
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

        Why it is needed: a pawn may move forward only to an empty square, and the other pieces check if
        the target is empty before they check if it holds an enemy. Used by the Piece classes.
        """
        row,col = pos

        return self.game_board[row,col] == EMPTY

    def get_color(self, pos):
        """Find the color of the piece on a square.

        pos: the square as [row, col].
        Returns WHITE or BLACK (an uppercase letter is white and a lowercase letter is black), or EMPTY if
        there is no piece on the square.

        Why it is needed: to know if a piece belongs to the current player, and if the piece on the target
        square is an enemy (it can be captured) or a friend (it cannot). Used by the Piece classes,
        get_legal_moves and perform_move.
        """
        row, col = pos
        if self.game_board[row,col] == EMPTY:
            return EMPTY
        if str(self.game_board[row,col]).islower():
            return BLACK

        return WHITE

    def perform_move(self, from_pos, to_pos):
        """Move a piece from one square to another.

        The piece is copied to the target square and the start square becomes empty. If the target square
        held an enemy piece, it is captured (it is simply overwritten). After the move, a pawn that reached
        the last row is replaced with a queen of the same color (the pawn answers is_promotion_move).

        This function does NOT check that the move is legal, so it must be called only with a move from
        get_legal_moves. Used by Game.play_game.
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
        Returns True if the row and the column are inside the board, otherwise False.

        Why it is needed: reading a square that is outside the array (for example row 5) crashes the
        program, so it must be checked first. Every piece checks the target square with it at the start of
        is_move_valid, and Board.is_move_valid checks the start square.
        """
        row, col = pos
        return  BOARD_COLS -1 >= col >= 0 and BOARD_ROWS -1  >= row >= 0

    def is_path_clear(self, from_pos, to_pos):
        """Check that there are no pieces between two squares.

        from_pos, to_pos: the squares as [row, col].
        Only the squares between them are checked (not the start and the end squares). It works for a
        straight line (row or column) or a diagonal, so the caller must check the shape of the move first.
        Returns True if all the squares between are empty, otherwise False.

        Why it is needed: the bishop, the rook and the queen cannot jump over other pieces.
        Used by the Bishop and the Rook (the Queen uses both).
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

        Why it is needed: the game ends when a king is captured (there is no check or checkmate).
        Used by Game.play_game, which checks it before every turn and when it decides who won.
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

        from_pos, to_pos: the squares as [row, col]. color: WHITE or BLACK.
        The start square must be inside the board and hold a piece of that color, and the move must follow
        the rules of that piece (a piece object is created from the letter and asked).
        Returns True if the move is legal, otherwise False.

        Where it is used: the game loop does not use it, because Game gets all the legal moves from
        get_legal_moves and the players choose from that list. It is kept for checking a single move,
        for example in tests or in the graphical interface.
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

        color: WHITE or BLACK.
        For every piece of this color one piece object is created (once for the piece, and not once for every
        target square, which is about 3 times faster) and it is asked about every square of the board.
        Returns a list of moves, and each move is [from_pos, to_pos]. The list is empty if the player has
        no legal move.

        Where it is used: Game.play_game calls it once in every turn. An empty list means a tie, and
        otherwise the list is given to the player, who chooses a move from it.
        """
        legal_moves = []
        for from_row in range(BOARD_ROWS):
            for from_col in range(BOARD_COLS):
                if self.get_color([from_row, from_col]) == color:
                    piece = create_piece_from_letter(self.game_board[from_row,from_col],self)
                    from_pos = [from_row, from_col]
                    for to_row in range(BOARD_ROWS):
                        for to_col in  range(BOARD_COLS):
                            to_pos = [to_row,to_col]
                            if piece.is_move_valid(from_pos, to_pos):
                                legal_moves.append([from_pos,to_pos])
        return legal_moves

    def get_str(self):
        """Return a string of 25 letters that represents the board (row after row).

        It is used as a key for saving boards, because a string can be a key in a dictionary.
        """
        result = ""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                result += self.game_board[row,col]

        return result

    def copy(self):
        """Return a new Board with the same pieces in the same places.

        The new board is independent: moving a piece on the copy does not change the original board.

        Where it is used: it is not used yet. It will be needed to try a move without changing the real board,
        for example by a smart player that looks at the board after each possible move.
        """
        new_board = Board()
        new_board.game_board = self.game_board.copy()
        return new_board