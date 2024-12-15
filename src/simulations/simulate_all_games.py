"""
Script to simulate all possible games and in how many attempts we would win them.
"""

import pickle
import os
import numpy as np

from src.wordle import Wordle


def main() -> None:
    """
    Simulates all games and obtains in how many attempts we would win them.
    """

    path = "data/all_games.pickle"

    if not os.path.exists(path):

        with open("possible_words.txt", "r", encoding="utf-8") as f:
            possible_words = [line.strip() for line in f]

        words_dict = {}
        for i, word in enumerate(possible_words):
            model = Wordle()
            attempts = model.simulate_game(word)
            words_dict[word] = attempts
            if i % 100 == 0:
                print(i)

        with open(path, "wb") as f:
            pickle.dump(words_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

    with open(path, "rb") as f:
        all_games = pickle.load(f)

    attempts = list(all_games.values())
    mean = np.mean(attempts)
    std = np.std(attempts)
    print(f"Mean: {mean:.2f}. Std: {std:.2f}.")


if __name__ == "__main__":
    main()
  
