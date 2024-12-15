"""
Script to play Wodle using Information Theory.
"""

import numpy as np

from src.constants import POSSIBLE_WORDS, VECTORS, GREY, YELLOW, GREEN, N_LETTERS, EMPTY
from src.draw import draw_board


class Wordle:
    """
    Class to represent a Wordle game and obtain the necessary calculations.
    """

    def __init__(self) -> None:
        """
        Constructor of the class.
        """

        self.possible_words = list(POSSIBLE_WORDS)

    @staticmethod
    def _calculate_vector(guess: str, real_word: str) -> list[int]:
        """
        Calculates the output vector.

        Parameters
        ----------
        guess     : Introduced word.
        real_word : Real word.

        Returns
        -------
        Response vector.
        """

        v = [GREY for _ in range(N_LETTERS)]
        count = [real_word.count(letter) for letter in real_word]

        for i, letter in enumerate(guess):
            if letter == real_word[i]:
                v[i] = GREEN
                # Substract everywhere it corresponds (a letter can appear
                # more than once in the real word)
                for j, ll in enumerate(real_word):
                    if letter == ll:
                        count[j] -= 1

        for i, letter in enumerate(guess):
            if v[i] != GREEN and letter in real_word:
                # Does not mind if there is more than one index, so this is ok
                idx = real_word.index(letter)
                if count[idx] > 0:
                    v[i] = YELLOW
                    # As in the previous "for" loop
                    for j, ll in enumerate(real_word):
                        if letter == ll:
                            count[j] -= 1

        return v

    def _get_probability_of_vector(self, guess: str, v: list[int]) -> float:
        """
        Calculates the probability of a specific resulting vector if we
        introduce the word guess.

        Parameters
        ----------
        guess  : Word we would write.
        v      : Resulting vector we would have introducing that word.

        Returns
        -------
        Probability of obtaining that vector introducing guess.
        """

        count = 0

        for word in self.possible_words:
            if self._calculate_vector(word, guess) == v:
                count += 1

        return count / len(self.possible_words)

    def _get_entropy_of_word(self, guess: str) -> float:
        """
        Calculates the entropy of word.

        Parameters
        ----------
        guess : Word we introduce.

        Returns
        -------
        Entropy of the word.
        """

        entropy = 0

        for vector in VECTORS:
            p = self._get_probability_of_vector(guess, vector)
            if p > 0:  # limit when p -> 0 is 0
                entropy -= p * np.log2(p)

        return entropy

    def _reduce_possible_words(self, guess: str, v: list[int]) -> None:
        """
        Updates the list of possible words when we introduce a guess and
        obtain a vector.

        Parameters
        ----------
        guess : Word we introduced.
        v     : Vector we obtained.
        """

        self.possible_words = [
            word
            for word in self.possible_words
            if self._calculate_vector(guess, word) == v
        ]

    def _choose_word(self) -> str:
        """
        Obtains the word with highest entropy.

        Returns
        -------
        Word with highest entropy.
        """

        aux = -1.0  # it would be valid any number < 0 as entropy is always >= 0
        choosen_word = ""

        for word in self.possible_words:
            temp = self._get_entropy_of_word(word)
            if temp > aux:
                aux = temp
                choosen_word = word

        return choosen_word

    def simulate_game(self, real_word: str, first_guess: str = "slate") -> int:
        """
        Plays automatically a game.

        Parameters
        ----------
        real_word   : Solution.
        first_guess : First guess we introduce.

        Returns
        -------
        Attempts that takes us to succeed.
        """

        attempts = 1
        if first_guess == real_word:
            return attempts
        vector = self._calculate_vector(first_guess, real_word)
        self._reduce_possible_words(first_guess, vector)

        while True:
            guess = self._choose_word()
            attempts += 1
            if guess == real_word:
                return attempts
            vector = self._calculate_vector(guess, real_word)
            self._reduce_possible_words(guess, vector)

    def play_game(self, first_guess: str = "slate") -> None:
        """
        Plays a real game. You have to answer 0 if you have not won and 1 if you have
        won. When asked for a vector write a string of N_LETTERS (5) numbers where a 0
        corresponds to grey, 1 to yellow and 2 to green.

        Parameters
        ----------
        first_guess : First guess we introduce.
        """

        # Matrixes to create the figures
        matrix_nums = [[EMPTY for _ in range(N_LETTERS)] for _ in range(6)]
        matrix_letters = [["" for _ in range(N_LETTERS)] for _ in range(6)]

        turn = 0

        print(f"\n{first_guess}\n")
        matrix_letters[turn] = [letter.upper() for letter in first_guess]
        sw = int(input("Have you won? "))
        if sw == 1:
            matrix_nums[turn] = [GREEN for _ in range(N_LETTERS)]
            draw_board(matrix_nums, matrix_letters, turn + 1)
            print("\nCongratulations!")
            return
        v = [int(number) for number in str(input("\nVector: "))]
        matrix_nums[turn] = v.copy()
        self._reduce_possible_words(first_guess, v)
        draw_board(matrix_nums, matrix_letters, turn + 1)

        while True:
            turn += 1
            guess = self._choose_word()
            print("\n" + guess + "\n")
            matrix_letters[turn] = [letter.upper() for letter in guess]
            sw = int(input("Have you won? "))
            if sw == 1:
                matrix_nums[turn] = [GREEN for _ in range(N_LETTERS)]
                draw_board(matrix_nums, matrix_letters, turn + 1)
                print("\nCongratulations!")
                return
            v = [int(number) for number in str(input("\nVector: "))]
            matrix_nums[turn] = v.copy()
            self._reduce_possible_words(guess, v)
            draw_board(matrix_nums, matrix_letters, turn + 1)


if __name__ == "__main__":
    model = Wordle()
    model.play_game()
