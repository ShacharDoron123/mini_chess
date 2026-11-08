from board import Board
from player import HumanPlayer, RandomPlayer
from constants import *


class Game:

    def __init__(self, player1_type, player2_type):
        self.board = Board()

        if player1_type == HumanPlayer:
            self.player1 = HumanPlayer(WHITE, self.board)
        else:
            self.player1 = RandomPlayer(WHITE, self.board)

        if player2_type == HumanPlayer:
            self.player2 = HumanPlayer(BLACK, self.board)
        else:
            self.player2 = RandomPlayer(BLACK, self.board)

        self.current_player = self.player1

    # ---------- methods used by the GUI (one move at a time) ----------

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def make_move(self, from_pos, to_pos):
        """Performs one move for the current player and passes the turn.
        Returns False (and changes nothing) if the move is not legal."""
        if not self.board.is_move_valid(from_pos, to_pos, self.current_player.color):
            return False

        self.board.perform_move(from_pos, to_pos)
        self.switch_player()
        return True

    def get_result(self):
        """Returns None if the game goes on, otherwise WHITE, BLACK or TIE."""
        if not self.board.is_king_alive(WHITE):
            return BLACK
        if not self.board.is_king_alive(BLACK):
            return WHITE
        if len(self.board.get_legal_moves(self.current_player.color)) == 0:
            return TIE
        return None

    # ---------- the terminal version ----------

    def play_game(self):

        while self.board.is_king_alive(WHITE) and self.board.is_king_alive(BLACK):
            self.board.print_board()
            if len(self.board.get_legal_moves(self.current_player.color)) == 0:
                print("It's a tie!")
                return TIE
            move = self.current_player.get_player_move()
            from_pos, to_pos = move
            self.board.perform_move(from_pos, to_pos)
            if self.current_player == self.player1:
                self.current_player = self.player2
            else:
                self.current_player = self.player1

        if not self.board.is_king_alive(WHITE):
            self.board.print_board()
            print(f"Player {BLACK} won!")
            return BLACK
        else:
            self.board.print_board()
            print(f"Player {WHITE} won!")
            return WHITE