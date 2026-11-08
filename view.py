import tkinter as tk
from constants import *


class View:
    """Only draws things. It does not know any chess rules.
    When the user clicks a square it tells the controller."""

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        master.title(WINDOW_TITLE)

        self.create_top_bar()

        self.label_status = tk.Label(master, text="", font=("Arial", 14))
        self.label_status.pack(pady=5)

        self.frame_board = tk.Frame(master)
        self.frame_board.pack(padx=10, pady=10)
        self.cells = []
        self.create_board_cells()

    def create_top_bar(self):
        frame_top = tk.Frame(self.master)
        frame_top.pack(pady=5)

        self.white_type = tk.StringVar(value=HUMAN)
        self.black_type = tk.StringVar(value=RANDOM)

        tk.Label(frame_top, text="White:").grid(row=0, column=0)
        tk.OptionMenu(frame_top, self.white_type, HUMAN, RANDOM).grid(row=0, column=1)

        tk.Label(frame_top, text="Black:").grid(row=0, column=2)
        tk.OptionMenu(frame_top, self.black_type, HUMAN, RANDOM).grid(row=0, column=3)

        button_new = tk.Button(frame_top, text="New game", command=self.controller.new_game)
        button_new.grid(row=0, column=4, padx=10)

    def create_board_cells(self):
        for row in range(BOARD_ROWS):
            new_line = []
            for col in range(BOARD_COLS):
                cell = tk.Button(self.frame_board,
                                 font=PIECE_FONT,
                                 width=SYMBOL_BUTTON_WIDTH,
                                 height=SYMBOL_BUTTON_HEIGHT,
                                 relief=tk.FLAT,
                                 command=lambda r=row, c=col: self.controller.on_cell_click(r, c))
                cell.grid(row=row, column=col)
                new_line.append(cell)
            self.cells.append(new_line)
        self.clear_highlights()

    def get_player_types(self):
        return self.white_type.get(), self.black_type.get()

    def get_square_color(self, row, col):
        if (row + col) % 2 == 0:
            return LIGHT_SQUARE_COLOR
        return DARK_SQUARE_COLOR

    def set_cell_color(self, row, col, color):
        self.cells[row][col].config(bg=color, activebackground=color)

    def update_board(self, board):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                letter = board.game_board[row, col]
                if letter == EMPTY:
                    self.cells[row][col].config(text="")
                else:
                    self.cells[row][col].config(text=PIECE_SYMBOLS[letter], fg="black")

    def clear_highlights(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.set_cell_color(row, col, self.get_square_color(row, col))

    def show_selection(self, selected_pos, hint_positions):
        self.clear_highlights()
        self.set_cell_color(selected_pos[0], selected_pos[1], SELECTED_COLOR)
        for row, col in hint_positions:
            self.set_cell_color(row, col, HINT_COLOR)

    def set_status(self, text):
        self.label_status.config(text=text)
