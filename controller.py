from constants import *
from game import Game
from player import HumanPlayer, RandomPlayer
from view import View

PLAYER_CLASSES = {
    HUMAN: HumanPlayer,
    RANDOM: RandomPlayer,
}


class Controller:
    """Connects the View (what the user sees) and the Model (Game, Board).
    The View tells it about clicks, it asks the Model what to do
    and then tells the View what to draw."""

    def __init__(self, root):
        self.root = root
        self.view = View(root, self)
        self.game = None
        self.selected_pos = None
        self.computer_job = None
        self.new_game()

    def new_game(self):
        if self.computer_job is not None:
            self.root.after_cancel(self.computer_job)
            self.computer_job = None

        white_type, black_type = self.view.get_player_types()
        self.game = Game(PLAYER_CLASSES[white_type], PLAYER_CLASSES[black_type])
        self.selected_pos = None
        self.refresh()
        self.continue_game()

    def refresh(self):
        self.view.update_board(self.game.board)
        self.view.clear_highlights()
        self.view.set_status(self.get_status_text())

    def get_status_text(self):
        result = self.game.get_result()
        if result is None:
            return f"{self.game.current_player.color}'s turn"
        if result == TIE:
            return "It's a tie!"
        return f"{result} won!"

    def is_human_turn(self):
        return isinstance(self.game.current_player, HumanPlayer)

    def continue_game(self):
        """If it is a computer's turn, plays it after a short delay."""
        if self.game.get_result() is not None:
            return
        if not self.is_human_turn():
            self.computer_job = self.root.after(COMPUTER_MOVE_DELAY_MS, self.computer_move)

    def computer_move(self):
        self.computer_job = None
        from_pos, to_pos = self.game.current_player.get_player_move()
        self.game.make_move(from_pos, to_pos)
        self.refresh()
        self.continue_game()

    def select(self, pos):
        color = self.game.current_player.color
        self.selected_pos = pos
        hints = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.game.board.is_move_valid(pos, [row, col], color):
                    hints.append([row, col])
        self.view.show_selection(pos, hints)

    def on_cell_click(self, row, col):
        if self.game.get_result() is not None or not self.is_human_turn():
            return

        pos = [row, col]
        color = self.game.current_player.color
        own_piece_clicked = self.game.board.get_color(pos) == color

        if own_piece_clicked:
            self.select(pos)
            return

        if self.selected_pos is None:
            return

        if self.game.make_move(self.selected_pos, pos):
            self.selected_pos = None
            self.refresh()
            self.continue_game()
