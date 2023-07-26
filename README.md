# Introduction

This repo contains the code for playing **Wordle** with a heuristic that consists on selecting the word that gives us more **information**. It is based on this [video](https://www.youtube.com/watch?v=v68zYyaEmEA) of 3Blue1Brown, which explains all the maths behind.

After simulating all possible games (2315), it resolves them with a mean of 3.58 attempts and a standard deviation of 0.82 attempts. More precisely, in the following table the first row represents the number of attempts and the second row how many games have been won in that attempts.

| 1 |  2  |  3  |  4  |  5  | 6  | 7 | 8 |
| - | --- | --- | --- | --- | -- | - | - |
| 1 | 146 | 959 | 978 | 188 | 34 | 6 | 3 |

In the file ***wordle.py*** is the main code, ***_draw.py*** is for drawing the board and ***possible_words.txt*** contains all possible words that have appeared in the game. The folder ***others*** contains the code for simulating all games and for selecting the first word which gives us more information (note that the first word is always the same and after this the game changes in function of the response vector we obtain).

# How to play

To play a game we just have to create the object and write 1 if we have won and 0 otherwise and tell the response vector we obtain (0 means grey, 1 yellow and 2 green). One example is the following:


![image](https://github.com/antodiazcano/wordle/assets/114878742/bbe3651c-bf6a-43f7-8310-9fe85207e512)

