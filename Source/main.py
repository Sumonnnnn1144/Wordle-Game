import tkinter as tk
from tkinter import messagebox
import random
from wordle_core import WordleGame

# Load word lists
import os
base_path = os.path.dirname(__file__)
with open(os.path.join(base_path, "allowed.txt"), "r") as f:
    words = [w.strip().upper() for w in f if len(w.strip()) == 5]
with open(os.path.join(base_path, "secret.txt"), "r") as f:
    secrets = [w.strip().upper() for w in f if len(w.strip()) == 5]

# --- Main window setup ---
root = tk.Tk()
root.title("Wordle - Tkinter Edition")
root.configure(bg="white")

window_width, window_height = 850, 1000
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
center_x, center_y = int(screen_width / 2 - window_width / 2), int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.resizable(False, False)

# --- Global state ---
rows, cols = 6, 5
cells = []
current_row = 0
current_guess = ""
guessed_words = []
game = None
mode = "normal"  # "normal" or "blind"

# --- Frames ---
menu_frame = tk.Frame(root, bg="white")
mode_frame = tk.Frame(root, bg="white")
game_frame = tk.Frame(root, bg="white")

# --- Menu Frame ---
title = tk.Label(menu_frame, text="MENU", font=("Consolas", 36, "bold"), bg="white", fg="black")
title.pack(pady=100)

play_btn = tk.Button(menu_frame, text="PLAY", font=("Consolas", 20, "bold"),
                     width=10, bg="#6aaa64", fg="white", command=lambda: show_mode())
play_btn.pack(pady=20)

exit_btn = tk.Button(menu_frame, text="EXIT", font=("Consolas", 20, "bold"),
                     width=10, bg="#c94f4f", fg="white", command=root.destroy)
exit_btn.pack(pady=10)

# --- Mode selection Frame ---
mode_title = tk.Label(mode_frame, text="SELECT MODE", font=("Consolas", 28, "bold"), bg="white", fg="black")
mode_title.pack(pady=80)

normal_btn = tk.Button(mode_frame, text="NORMAL MODE", font=("Consolas", 18, "bold"),
                       width=15, bg="#6aaa64", fg="white", command=lambda: start_new_game("normal"))
normal_btn.pack(pady=20)

blind_btn = tk.Button(mode_frame, text="BLIND MODE", font=("Consolas", 18, "bold"),
                      width=15, bg="#5555aa", fg="white", command=lambda: start_new_game("blind"))
blind_btn.pack(pady=10)

back_btn = tk.Button(mode_frame, text="← BACK", font=("Consolas", 16, "bold"),
                     bg="gray", fg="white", command=lambda: show_frame(menu_frame))
back_btn.pack(pady=40)

# --- Game Frame ---
# Info button (“i”)
info_btn = tk.Button(game_frame, text="i", font=("Consolas", 14, "bold"),
                     bg="#d3d6da", fg="black", width=2, height=1, command=lambda: show_frame(rule_frame))
info_btn.place(x=10, y=10)

# Back button in game
back_in_game = tk.Button(game_frame, text="← Back", font=("Consolas", 14, "bold"),
                         bg="gray", fg="white", command=lambda: show_frame(mode_frame))
back_in_game.place(x=70, y=10)

# Title label
title_label = tk.Label(game_frame, text="WORDLE", font=("Consolas", 28, "bold"),
                       bg="white", fg="black")
title_label.pack(pady=(60, 10))

# Middle section
center_frame = tk.Frame(game_frame, bg="white")
center_frame.pack(expand=True, fill="both")

board_frame = tk.Frame(center_frame, bg="white")
board_frame.pack(pady=10)

rule_frame = tk.Frame(root, bg="white")

rule_title = tk.Label(rule_frame, text="GAME RULES", font=("Consolas", 28, "bold"), bg="white", fg="black")
rule_title.pack(pady=40)

rules_text = tk.Text(rule_frame, font=("Consolas", 16), wrap="word", bg="white", fg="black", bd=0, width=60, height=20)
rules_text.insert("1.0", 
"""
🟢 NORMAL MODE:
- You get color feedback after each guess.
- [Green] Correct letter in the correct position.
- [Yellow] Correct letter, wrong position.
- [Gray] Letter not in the word.
- You have 6 attempts to guess the secret word.

🟣 BLIND MODE:
- You do NOT get color feedback after each guess.
- All feedback will be revealed only after all 6 attempts are used.
- Plan your guesses carefully; memory and deduction are key.
- You win if you guess the word before your 6th attempt.

Press ← Back to return to your game.
""")
rules_text.config(state="disabled")
rules_text.pack(padx=20, pady=10)

back_from_rule = tk.Button(rule_frame, text="← BACK", font=("Consolas", 16, "bold"),
                           bg="gray", fg="white", command=lambda: show_frame(game_frame))
back_from_rule.pack(pady=30)

# Create cells
cells = []
for r in range(rows):
    row_cells = []
    for c in range(cols):
        label = tk.Label(board_frame, text="", width=3, height=1,
                         font=("Consolas", 28, "bold"),
                         relief="solid", bd=2, bg="white", fg="black",
                         highlightthickness=1, highlightbackground="black")
        label.grid(row=r, column=c, padx=6, pady=6)
        row_cells.append(label)
    cells.append(row_cells)

# Message label
message_label = tk.Label(center_frame, text="", font=("Consolas", 18, "bold"),
                         bg="white", fg="black")
message_label.pack(pady=(10, 5))

# Keyboard section
keyboard_frame = tk.Frame(game_frame, bg="white")
keyboard_frame.pack(side="bottom", pady=(10, 20))

keyboard_rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
key_buttons = {}

def on_virtual_key_press(letter):
    event = type("Event", (object,), {"keysym": letter})()
    on_key_press(event)

def update_keyboard_colors(guess, feedback):
    if mode == "blind":
        return  # Don't color keyboard in blind mode
    for i, letter in enumerate(guess):
        btn = key_buttons.get(letter)
        if not btn:
            continue
        if feedback[i] in ("G", "🟩"):
            btn.config(bg="#6aaa64", fg="white")
        elif feedback[i] in ("Y", "🟨") and btn.cget("bg") != "#6aaa64":
            btn.config(bg="#c9b458", fg="white")
        elif feedback[i] == "⬜" and btn.cget("bg") not in ("#6aaa64", "#c9b458"):
            btn.config(bg="#787c7e", fg="white")

for row in keyboard_rows:
    frame = tk.Frame(keyboard_frame, bg="white")
    frame.pack(pady=5)
    for letter in row:
        btn = tk.Button(frame, text=letter, width=4, height=2,
                        font=("Consolas", 14, "bold"),
                        bg="#d3d6da", fg="black",
                        command=lambda l=letter: on_virtual_key_press(l))
        btn.pack(side="left", padx=3, pady=3)
        key_buttons[letter] = btn

# --- Logic ---

def show_frame(frame):
    for f in (menu_frame, mode_frame, game_frame, rule_frame):
        f.pack_forget()
    frame.pack(expand=True, fill="both")


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


def start_new_game(selected_mode="normal"):
    global game, current_row, current_guess, guessed_words, mode
    mode = selected_mode
    game = WordleGame(words)
    game.secret = random.choice(secrets)
    print("Secret word:", game.secret)

    current_row = 0
    current_guess = ""
    guessed_words = []

    # Reset board
    for r in range(rows):
        for c in range(cols):
            cells[r][c].config(text="", bg="white", fg="black")
    message_label.config(text="")

    # Reset keyboard
    for btn in key_buttons.values():
        btn.config(bg="#d3d6da", fg="black")

    root.bind("<Key>", on_key_press)
    show_frame(game_frame)


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

            # In blind mode, hide feedback until the end
            if mode == "normal":
                colorize_row(current_row, feedback)
            update_keyboard_colors(guess, feedback)

            # Check win or lose
            if feedback == ["🟩"] * cols:
                show_message("🎉 YOU WIN!", "green", duration=999999)
                root.unbind("<Key>")
                return
            elif current_row == rows - 1:
                if mode == "blind":
                    # Reveal all feedback at the end
                    for i, g in enumerate(guessed_words):
                        colorize_row(i, game.check_guess(g))
                show_message(f"💀 YOU LOSE!\nWord was: {game.secret}", "red", duration=999999)
                root.unbind("<Key>")
                return

            current_row += 1
            current_guess = ""


# def show_frame(frame):
#     for f in (menu_frame, mode_frame, game_frame):
#         f.pack_forget()
#     frame.pack(expand=True, fill="both")


def show_mode():
    show_frame(mode_frame)


show_frame(menu_frame)
root.mainloop()
