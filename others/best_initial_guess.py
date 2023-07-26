from wordle import Wordle
import pickle


POSSIBLE_WORDS = [line.strip() for line in open("possible_words.txt", "r")]


count = 0
W = Wordle()
words_dict = {}
for word in POSSIBLE_WORDS:
    E = W._get_entropy_of_word(word)
    words_dict[word] = E
    if count % 100 == 0:
        print(count)
    count += 1
    
# Save dict
with open("initial_guess.pickle", "wb") as f:
    pickle.dump(words_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
    
# Load dict
with open("initial_guess.pickle", "rb") as f:
    initial_guess = pickle.load(f)
    
