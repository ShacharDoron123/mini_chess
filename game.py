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