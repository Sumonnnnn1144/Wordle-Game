import random


class WordleGame:
    def __init__(self, wordlist, word_length=5, max_turns=6):
        self.wordlist = [w.upper() for w in wordlist if len(w) == word_length]
        self.secret = random.choice(self.wordlist)
        self.word_length = word_length
        self.max_turns = max_turns
        self.current_turn = 0
        self.history = []  

   
    def check_guess(self, guess):
        guess = guess.upper()
        secret = self.secret
        result = ["⬜"] * self.word_length  
        used = [False] * self.word_length  

        
        for i in range(self.word_length):
            if guess[i] == secret[i]:
                result[i] = "🟩"
                used[i] = True

        
        for i in range(self.word_length):
            if result[i] == "🟩":
                continue
            for j in range(self.word_length):
                if not used[j] and guess[i] == secret[j]:
                    result[i] = "🟨"
                    used[j] = True
                    break

        return result

    
    def show_board(self):
        print("\n===== WORDLE =====")
        for guess, result in self.history:
            print(" ".join(guess))
            print(" ".join(result))
            print()
        print("==================\n")


