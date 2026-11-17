import time

from player import RandomPlayer
from tournament import Tournament


def main():
    """Run a tournament between two random players and print the results and the running time."""
    start = time.perf_counter()
    tournament = Tournament(RandomPlayer, RandomPlayer, 100, False)
    tournament.start_a_tournament()
    print(f"Execution time: {time.perf_counter() - start:.2f} seconds")


if __name__ == "__main__":
    main()