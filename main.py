from board import Board
from piece import Pawn
from constants import *


def check(name, result, expected):
    if result == expected:
        print("OK  ", name)
    else:
        print("FAIL", name, "- got", result, "expected", expected)


def main():
    board = Board()
    board.print_board()

    print("--- is_empty ---")
    check("empty square [2, 2]", board.is_empty([2, 2]), True)
    check("square with a pawn [3, 1]", board.is_empty([3, 1]), False)

    print("--- get_color ---")
    check("white pawn [3, 1]", board.get_color([3, 1]), WHITE)
    check("black pawn [1, 1]", board.get_color([1, 1]), BLACK)
    check("empty square [2, 2]", board.get_color([2, 2]), EMPTY)

    white_pawn = Pawn("pawn", WHITE, board)
    black_pawn = Pawn("pawn", BLACK, board)

    print("--- white pawn: regular moves ---")
    check("forward", white_pawn.is_move_valid([3, 1], [2, 1]), True)
    check("backward", white_pawn.is_move_valid([3, 1], [4, 1]), False)
    check("two forward", white_pawn.is_move_valid([3, 1], [1, 1]), False)
    check("diagonal to empty square", white_pawn.is_move_valid([3, 1], [2, 0]), False)

    print("--- black pawn: regular moves ---")
    check("forward", black_pawn.is_move_valid([1, 1], [2, 1]), True)
    check("backward", black_pawn.is_move_valid([1, 1], [0, 1]), False)
    check("diagonal to empty square", black_pawn.is_move_valid([1, 1], [2, 0]), False)

    print("--- perform_move ---")
    board.perform_move([1, 2], [2, 2])
    check("source is empty", board.is_empty([1, 2]), True)
    check("target has black pawn", board.get_color([2, 2]), BLACK)
    board.perform_move([3, 0], [2, 0])
    check("target has white pawn", board.get_color([2, 0]), WHITE)
    board.print_board()

    print("--- captures ---")
    check("white captures black", white_pawn.is_move_valid([3, 1], [2, 2]), True)
    check("white captures white", white_pawn.is_move_valid([3, 1], [2, 0]), False)
    check("black captures white", black_pawn.is_move_valid([1, 1], [2, 0]), True)
    check("black captures black", black_pawn.is_move_valid([1, 1], [2, 2]), False)


if __name__ == "__main__":
    main()