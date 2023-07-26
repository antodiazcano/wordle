from wordle import Wordle
import pickle


POSSIBLE_WORDS = [line.strip() for line in open("possible_words.txt", "r")]


count = 0
words_dict = {}
for word in POSSIBLE_WORDS:
    W = Wordle()
    attempts = W.simulate_game(word)
    words_dict[word] = attempts
    if count % 100 == 0:
        print(count)
    count += 1

# Save dict
with open("all_games.pickle", "wb") as f:
    pickle.dump(words_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
    
# Load dict
with open("all_games.pickle", "rb") as f:
    all_games = pickle.load(f)
    
