import tkinter as tk
import random
from functools import partial

class MemoryPuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Puzzle Game")
        self.root.resizable(False, False)

        # Game variables
        self.tiles = list(range(1, 9)) * 2   # 8 pairs
        random.shuffle(self.tiles)

        self.buttons = []
        self.first_choice = None
        self.second_choice = None
        self.matched = []
        self.moves = 0

        self.create_ui()

    def create_ui(self):
        title = tk.Label(self.root, text="Memory Puzzle Game",
                         font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        self.move_label = tk.Label(self.root, text="Moves: 0",
                                   font=("Arial", 12))
        self.move_label.grid(row=1, column=0, columnspan=4)

        index = 0
        for row in range(2, 6):
            for col in range(4):
                btn = tk.Button(self.root,
                                text="?",
                                font=("Arial", 14, "bold"),
                                width=6,
                                height=3,
                                command=partial(self.flip_tile, index))
                btn.grid(row=row, column=col, padx=5, pady=5)
                self.buttons.append(btn)
                index += 1

        reset_btn = tk.Button(self.root, text="Restart Game",
                              font=("Arial", 12),
                              command=self.reset_game)
        reset_btn.grid(row=6, column=0, columnspan=4, pady=10)

    def flip_tile(self, index):
        if index in self.matched:
            return
        if self.second_choice is not None:
            return

        self.buttons[index]["text"] = str(self.tiles[index])
        self.buttons[index]["state"] = "disabled"

        if self.first_choice is None:
            self.first_choice = index
        else:
            self.second_choice = index
            self.root.after(700, self.check_match)

    def check_match(self):
        self.moves += 1
        self.move_label.config(text=f"Moves: {self.moves}")

        i = self.first_choice
        j = self.second_choice

        if self.tiles[i] == self.tiles[j]:
            self.matched.extend([i, j])
            if len(self.matched) == len(self.tiles):
                self.show_win_message()
        else:
            self.buttons[i]["text"] = "?"
            self.buttons[j]["text"] = "?"
            self.buttons[i]["state"] = "normal"
            self.buttons[j]["state"] = "normal"

        self.first_choice = None
        self.second_choice = None

    def show_win_message(self):
        win_label = tk.Label(self.root,
                             text="🎉 You Won the Game! 🎉",
                             font=("Arial", 14, "bold"),
                             fg="green")
        win_label.grid(row=7, column=0, columnspan=4, pady=5)

    def reset_game(self):
        random.shuffle(self.tiles)
        self.first_choice = None
        self.second_choice = None
        self.matched = []
        self.moves = 0
        self.move_label.config(text="Moves: 0")

        for btn in self.buttons:
            btn.config(text="?", state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryPuzzleGame(root)
    root.mainloop()