
from constants import *
from game import Game


class Tournament:
    """Runs many games between two types of players and counts the results.

    It is used to see how well a type of player plays, by playing a lot of games.
    """

    def __init__(self, player1_type, player2_type, num_games, show_board=True):
        """Save the player types, the number of games and whether to print the games.

        player1_type, player2_type: HumanPlayer or RandomPlayer (the class itself).
        Player 1 always plays white and player 2 plays black.
        num_games: how many games to play.
        show_board: True to print every game, and False to play silently (better for many games).
        """
        self.player1_type = player1_type
        self.player2_type = player2_type
        self.num_games = num_games
        self.show_board = show_board

        self.white_wins = 0
        self.black_wins = 0
        self.ties = 0

    def start_a_tournament(self):
        """Play all the games and count the results.

        For every game a new Game is created and played. The result (WHITE, BLACK or TIE) is added to the
        matching counter. At the end, print_results prints the summary.
        """
        for i in range(self.num_games):
            game = Game(self.player1_type, self.player2_type, self.show_board)
            result = game.play_game()
            if result == WHITE:
                self.white_wins += 1
            elif result == BLACK:
                self.black_wins += 1
            else:
                self.ties += 1
        self.print_results()

    def print_results(self):
        """Print how many games each side won and how many ended in a tie.

        Called at the end of start_a_tournament.
        """
        print("=========================")
        print("    TOURNAMENT RESULTS   ")
        print("=========================")
        print(f"Games played:          {self.num_games}")
        print(f"White (player 1) wins: {self.white_wins}")
        print(f"Black (player 2) wins: {self.black_wins}")
        print(f"Ties:                  {self.ties}")
        print("=========================")