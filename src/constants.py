"""
Script to define all constants used.
"""

from itertools import product


N_LETTERS = 5
EMPTY = -1
GREY = 0
YELLOW = 1
GREEN = 2
VECTORS = [
    list(combination)
    for combination in product([GREY, YELLOW, GREEN], repeat=N_LETTERS)
]
with open("data/possible_words.txt", "r", encoding="utf-8") as f:
    POSSIBLE_WORDS = [line.strip() for line in f]
