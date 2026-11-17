from board import Board
from player import HumanPlayer, RandomPlayer
from constants import *


class Game:
    """One game between two players, from the start until someone wins or it is a tie.

    Game creates the board and the two players, manages the turns, and decides when the game is over.
    """

    def __init__(self, player1_type, player2_type, show_board):
        """Create a board and two players.

        player1_type, player2_type: HumanPlayer or RandomPlayer (the class itself).
        show_board: True to print the board and the result during the game, and False to play silently
        (the Tournament uses False, because it plays many games).
        Player 1 plays white and starts, and player 2 plays black.
        """
        self.board = Board()
        self.show_board = show_board

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
        """Play the whole game, move after move.

        In every turn the legal moves of the current player are calculated once. If there are none, the game
        ends in a tie. Otherwise the current player chooses a move from them, the board performs it, and the
        turn passes to the other player. The game also ends when a king is captured.
        If show_board is True, the board and the result are printed.
        Returns WHITE or BLACK (the winner), or TIE.
        """
        while self.board.is_king_alive(WHITE) and self.board.is_king_alive(BLACK):
            if self.show_board:
                self.board.print_board()
            legal_moves = self.board.get_legal_moves(self.current_player.color)
            if len(legal_moves) == 0:
                if self.show_board:
                    print("It's a tie!")
                return TIE
            move = self.current_player.get_player_move(legal_moves)
            from_pos, to_pos = move
            self.board.perform_move(from_pos, to_pos)
            if self.current_player == self.player1:
                self.current_player = self.player2
            else:
                self.current_player = self.player1

        if not self.board.is_king_alive(WHITE):
            if self.show_board:
                self.board.print_board()
                print(f"Player {BLACK} won!")
            return BLACK
        else:
            if self.show_board:
                self.board.print_board()
                print(f"Player {WHITE} won!")
            return WHITE