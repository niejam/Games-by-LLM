import tkinter as tk
from tkinter import messagebox
import random

# Constants
WIDTH = 10
HEIGHT = 10
MINES = 10

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        
        self.board = [[{'mine': False, 'revealed': False, 'flagged': False, 'adjacent_mines': 0} 
                       for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.mine_positions = set()
        self.create_board()
        self.place_mines()
        self.calculate_adjacent_mines()

        self.buttons = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.create_buttons()

    def create_board(self):
        # Place mines randomly
        self.mine_positions = set(random.sample(range(WIDTH * HEIGHT), MINES))
    
    def place_mines(self):
        for pos in self.mine_positions:
            x = pos % WIDTH
            y = pos // WIDTH
            self.board[y][x]['mine'] = True

    def calculate_adjacent_mines(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if not self.board[y][x]['mine']:
                    self.board[y][x]['adjacent_mines'] = sum(
                        self.board[ny][nx]['mine']
                        for dx in (-1, 0, 1) if 0 <= x + dx < WIDTH
                        for dy in (-1, 0, 1) if 0 <= y + dy < HEIGHT
                        if (dx, dy) != (0, 0)
                        for nx, ny in [(x + dx, y + dy)]
                    )

    def create_buttons(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                button = tk.Button(self.root, width=2, height=1, command=lambda x=x, y=y: self.reveal(x, y))
                button.bind("<Button-3>", lambda event, x=x, y=y: self.toggle_flag(x, y))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def reveal(self, x, y):
        cell = self.board[y][x]
        if cell['flagged']:
            return
        
        cell['revealed'] = True
        button = self.buttons[y][x]
        if cell['mine']:
            button.config(text="M", bg='red')
            self.game_over(False)
        else:
            button.config(text=str(cell['adjacent_mines']) if cell['adjacent_mines'] > 0 else "", bg='lightgray')
            if cell['adjacent_mines'] == 0:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if (dx, dy) != (0, 0):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and not self.board[ny][nx]['revealed']:
                                self.reveal(nx, ny)
        
        if self.check_win():
            self.game_over(True)

    def toggle_flag(self, x, y):
        cell = self.board[y][x]
        button = self.buttons[y][x]
        if not cell['revealed']:
            cell['flagged'] = not cell['flagged']
            button.config(text='F' if cell['flagged'] else '')

    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell['mine'] and not cell['revealed']:
                    return False
        return True

    def game_over(self, win):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.buttons[y][x].config(state=tk.DISABLED)
                if self.board[y][x]['mine']:
                    self.buttons[y][x].config(text='M', bg='orange' if win else 'red')
        if win:
            messagebox.showinfo("Congratulations!", "You've won!")
        else:
            messagebox.showinfo("Game Over", "You hit a mine!")

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()