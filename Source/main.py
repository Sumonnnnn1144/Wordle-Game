import tkinter as tk
import random
from wordle_core import WordleGame


with open("allowed.txt", "r") as f:
    words = [w.strip().upper() for w in f if len(w.strip()) == 5]

with open("secret.txt", "r") as f:
    secrets = [w.strip().upper() for w in f if len(w.strip()) == 5]


root = tk.Tk()
root.title("Wordle - Tkinter Edition")
root.configure(bg="white")

window_width, window_height = 650, 750
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
center_x, center_y = int(screen_width / 2 - window_width / 2), int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.resizable(False, False)


rows, cols = 6, 5
cells = []
current_row = 0
current_guess = ""
guessed_words = []
game = None


main_frame = tk.Frame(root, bg="white")
main_frame.pack(expand=True)


title_label = tk.Label(main_frame, text="WORDLE GAME", font=("Consolas", 24, "bold"),
                       bg="white", fg="black")
title_label.grid(row=0, column=0, columnspan=cols, pady=(10, 20))


for r in range(1, rows + 1):
    row_cells = []
    for c in range(cols):
        label = tk.Label(main_frame, text="", width=2, height=1,
                         font=("Consolas", 22, "bold"),
                         relief="solid", bd=2, bg="white", fg="black",
                         highlightthickness=1, highlightbackground="black")
        label.grid(row=r, column=c, padx=6, pady=6)
        row_cells.append(label)
    cells.append(row_cells)


message_label = tk.Label(root, text="", font=("Consolas", 16, "bold"),
                         bg="white", fg="black")
message_label.place(relx=0.5, rely=0.9, anchor="center")  


def show_message(text, color="black", duration=2000):
    message_label.config(text=text, fg=color)
    if "WIN" not in text and "LOSE" not in text:
        root.after(duration, lambda: message_label.config(text=""))



def colorize_row(row, feedback):
    for i, mark in enumerate(feedback):
        if mark in ("G", "🟩"):
            color = "#6aaa64"
        elif mark in ("Y", "🟨"):
            color = "#c9b458"
        else:
            color = "#787c7e"
        cells[row][i].config(bg=color, fg="white")


def start_new_game():
    global game, current_row, current_guess, guessed_words
    game = WordleGame(words)
    game.secret = random.choice(secrets)
    print("Secret word:", game.secret)

    current_row = 0
    current_guess = ""
    guessed_words = []

   
    for r in range(rows):
        for c in range(cols):
            cells[r][c].config(text="", bg="white", fg="black")

    message_label.config(text="")
    root.bind("<Key>", on_key_press)


def on_key_press(event):
    global current_row, current_guess

    key = event.keysym.upper()

    
    if len(key) > 1 and key not in ("BACKSPACE", "RETURN"):
        return

    
    if len(key) == 1 and key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if len(current_guess) < cols:
            cells[current_row][len(current_guess)].config(text=key)
            current_guess += key

    
    elif key == "BACKSPACE":
        if len(current_guess) > 0:
            current_guess = current_guess[:-1]
            cells[current_row][len(current_guess)].config(text="")
            
    
    elif key == "RETURN":
        if len(current_guess) == cols:
            guess = current_guess.upper()

            
            if guess in guessed_words:
                show_message("⚠️ Word already guessed!", "red")
                return

            
            if guess not in words:
                show_message("❌ Word not allowed!", "red")
                return

            feedback = game.check_guess(guess)
            guessed_words.append(guess)
            colorize_row(current_row, feedback)

            
            if feedback == ["🟩"] * cols:
                show_message("🎉 YOU WIN!", "green")
                root.unbind("<Key>")
                return
            elif current_row == rows - 1:
                show_message(f"💀 YOU LOSE! Word was {game.secret}", "red")
                root.unbind("<Key>")
                return

            current_row += 1
            current_guess = ""

menu_bar = tk.Menu(root)
game_menu = tk.Menu(menu_bar, tearoff=0)
game_menu.add_command(label="Reset Game", command=start_new_game)
game_menu.add_separator()
game_menu.add_command(label="Exit", command=root.destroy)
menu_bar.add_cascade(label="Menu", menu=game_menu)
root.config(menu=menu_bar)


start_new_game()
root.bind("<KeyPress>", on_key_press)
root.mainloop()
