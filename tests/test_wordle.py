"""
Script to test the functionalities of the Wordle class.
"""

import pytest
import numpy as np

from src.wordle import Wordle
from src.constants import GREY, YELLOW, GREEN


@pytest.mark.run(order=1)
@pytest.mark.parametrize(
    "guess, real_word, expected_v",
    [
        ("apple", "apple", [GREEN, GREEN, GREEN, GREEN, GREEN]),  # exact coincidence
        ("apple", "brick", [GREY, GREY, GREY, GREY, GREY]),  # no coincidences
        (
            "spoon",
            "noose",
            [YELLOW, GREY, GREEN, YELLOW, YELLOW],
        ),  # exact and partial coincidences
        (
            "stone",
            "notes",
            [YELLOW, YELLOW, YELLOW, YELLOW, YELLOW],
        ),  # all partial coincidences
        (
            "eerie",
            "refer",
            [YELLOW, GREEN, YELLOW, GREY, GREY],
        ),  # repeated letters in both words
        (
            "eager",
            "anger",
            [GREY, YELLOW, GREEN, GREEN, GREEN],
        ),  # repeated letters in first word
        (
            "space",
            "peace",
            [GREY, YELLOW, GREEN, GREEN, GREEN],
        ),  # repeated letters in second word
    ],
)
def test_calculate_vector(guess: str, real_word: str, expected_v: list[int]) -> None:
    """
    Test for calculating the output vector.

    Parameters
    ----------
    guess      : Guessed word.
    real_word  : Real word.
    expected_v : Expected vector.
    """

    model = Wordle()
    result = model._calculate_vector(guess, real_word)
    assert result == expected_v, (
        f"Error with guess='{guess}', real_word='{real_word}': "
        f"Got {result}, expected {expected_v}."
    )


@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "guess, possible_words, vector, expected_prob",
    [
        (
            "apple",
            ["apple", "brick", "spoon", "stone", "space"],
            [GREEN, GREEN, GREEN, GREEN, GREEN],
            1 / 5,
        ),
        (
            "szzze",
            ["apple", "spoon", "brick", "stone", "space"],
            [GREEN, GREY, GREY, GREY, GREEN],
            2 / 5,
        ),
        (
            "apple",
            ["brick", "stone", "spoon", "space", "crane"],
            [GREEN, GREEN, GREEN, GREEN, GREEN],
            0.0,
        ),
        ("space", ["space", "crane"], [GREEN, GREEN, GREEN, GREEN, GREEN], 1 / 2),
    ],
)
def test_get_probability_of_vector(
    guess: str, possible_words: list[str], vector: list[int], expected_prob: float
) -> None:
    """
    Test for calculating the probability of a vector if we introduce the word 'guess'.

    Parameters
    ----------
    guess          : Guessed word.
    possible_words : Possible remaining words.
    vector         : Vector which we want to calculate the probability of.
    expected_prob  : Expected probability.
    """

    model = Wordle()
    model.possible_words = list(possible_words)
    result = model._get_probability_of_vector(guess, vector)
    assert result == expected_prob, f"Error: got {result}, expected {expected_prob}"


@pytest.mark.run(order=3)
@pytest.mark.parametrize("word, big_entropy", [("zzzzz", False), ("slate", True)])
def test_entropy(word: str, big_entropy: float, threshold: float = 1.0) -> None:
    """
    Test for calculating the entropy of a word.

    Parameters
    ----------
    word        : Word of which we calculate the entropy.
    big_entropy : True if the expected entropy is high, False otherwise.
    threshold   : Threshold to consider entropy big or small.
    """

    model = Wordle()
    result = model._get_entropy_of_word(word)
    assert result >= 0
    if big_entropy:
        assert result >= threshold, f"Got {result}, expected bigger entropy"
    else:
        assert result < threshold, f"Got {result}, expected smaller entropy"


@pytest.mark.run(order=4)
@pytest.mark.parametrize(
    "guess, vector, expected",
    [
        ("apple", [GREEN, GREEN, GREEN, GREEN, GREEN], ["apple"]),
        ("apple", [YELLOW, YELLOW, GREY, GREY, GREEN], ["grape", "pbane"]),
        ("apple", [YELLOW, GREEN, GREEN, GREEN, GREEN], []),
    ],
)
def test_reduce_possible_words(
    guess: str, vector: list[int], expected: list[str]
) -> None:
    """
    Test for reducing the possible words.

    Parameters
    ----------
    guess    : Guessed word.
    vector   : Vector obtained.
    expected : Expected result.
    """

    model = Wordle()
    model.possible_words = ["apple", "grape", "peach", "plumb", "pbane"]
    model._reduce_possible_words(guess, vector)
    result = list(model.possible_words)
    assert result == expected, f"Got {result}, expected {expected}"


@pytest.mark.run(order=5)
def test_choose_word() -> None:
    """
    Test for choosing the word with the highest entropy.
    """

    model = Wordle()
    model.possible_words = ["apple", "grape", "peach", "plumb", "pbane"]
    idx = np.argmax([model._get_entropy_of_word(word) for word in model.possible_words])
    assert model._choose_word() == model.possible_words[idx]
