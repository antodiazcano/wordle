"""
Script to create a figure of the board.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


EPSILON = 0.05
WIDTH = 1
HEIGHT = 1
COL_EMPTY = "#FFFFFF"
COL_GREY = "#B0B09C"
COL_YELLOW = "#F3F033"
COL_GREEN = "#12CB23"


def draw_board(
    matrix_nums: list[list[int]], m_letters: list[list[str]], attempt: int
) -> None:
    """
    Draws the board.

    Parameters
    ----------
    matrix_nums : Matrix of the board (numeric representation).
    m_letters   : Matrix of the board (string representation).
    attempt     : Current attempt.
    """

    fig, ax = plt.subplots()
    rows, cols = len(matrix_nums), len(matrix_nums[0])
    ax.set_xlim(0 - EPSILON, cols + EPSILON)
    ax.set_ylim(0 - EPSILON, rows + EPSILON)
    ax.set_aspect("equal")
    ax.axis("off")

    for x in range(rows):
        for y in range(cols):
            if matrix_nums[x][y] == -1:
                rect = Rectangle(
                    (y, rows - x - 1), WIDTH, HEIGHT, facecolor=COL_EMPTY, edgecolor="k"
                )
            elif matrix_nums[x][y] == 0:
                rect = Rectangle(
                    (y, rows - x - 1), WIDTH, HEIGHT, facecolor=COL_GREY, edgecolor="k"
                )
            elif matrix_nums[x][y] == 1:
                rect = Rectangle(
                    (y, rows - x - 1),
                    WIDTH,
                    HEIGHT,
                    facecolor=COL_YELLOW,
                    edgecolor="k",
                )
            else:
                rect = Rectangle(
                    (y, rows - x - 1), WIDTH, HEIGHT, facecolor=COL_GREEN, edgecolor="k"
                )
            ax.add_patch(rect)
            ax.text(
                y + WIDTH / 2,
                rows - x - 1 + HEIGHT / 2,
                m_letters[x][y],
                ha="center",
                va="center",
                fontsize=12,
            )

    fig.savefig(f"images/attempt_{attempt}.png")
    plt.close()
