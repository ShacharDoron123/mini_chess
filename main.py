from game import Game
from player import RandomPlayer


def main():
    game = Game(RandomPlayer, RandomPlayer)
    result = game.play_game()
    print(f"Result: {result}")


main()