"""
Script to calculate the best initial guess, that is, the word with the highest initial
entropy. This is not necessary, but if the first initial guess is precalculated we save
a lot of time. Note that the first guess can be precalculated but the second and so on
no (in practice), because we can obtain a lot of different output vectors.
"""

import pickle
import os

from src.wordle import Wordle


def main() -> None:
    """
    Calculates the initial entropy for all words.
    """

    path = "data/initial_guess.pickle"

    if not os.path.exists(path):

        with open("data/possible_words.txt", "r", encoding="utf-8") as f:
            possible_words = [line.strip() for line in f]

        model = Wordle()
        words_dict = {}
        for i, word in enumerate(possible_words):
            entropy = model._get_entropy_of_word(word)
            words_dict[word] = entropy
            if i % 100 == 0:
                print(i)

        with open(path, "wb") as f:
            pickle.dump(words_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

    with open(path, "rb") as f:
        initial_guess = pickle.load(f)

    top_word = max(initial_guess, key=initial_guess.get)
    print(f"Best initial guess: {top_word}. Entropy: {initial_guess[top_word]:.2f}.")


if __name__ == "__main__":
    main()
  
