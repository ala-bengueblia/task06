import tkinter as tk
from tkinter import messagebox, Toplevel

# Constants
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'
BOARD_SIZE = 3

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = PLAYER_X
        self.user_player = None
        self.ai_player = None
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        self.choose_player()

    def choose_player(self):
        self.choice_window = Toplevel(self.root)
        self.choice_window.title("Choisissez votre joueur")
        self.choice_window.geometry("300x150")
        self.choice_window.configure(bg='lightblue')

        label = tk.Label(self.choice_window, text="Voulez-vous jouer avec X ou O ?", font=('Arial', 14), bg='lightblue')
        label.pack(pady=20)

        button_x = tk.Button(self.choice_window, text="X", font=('Arial', 14), bg='lightcoral', command=lambda: self.set_player(PLAYER_X))
        button_x.pack(side=tk.LEFT, padx=20, pady=20)

        button_o = tk.Button(self.choice_window, text="O", font=('Arial', 14), bg='lightgreen', command=lambda: self.set_player(PLAYER_O))
        button_o.pack(side=tk.RIGHT, padx=20, pady=20)

    def set_player(self, player):
        self.user_player = player
        self.ai_player = PLAYER_O if player == PLAYER_X else PLAYER_X
        self.choice_window.destroy()
        self.create_widgets()  # Initialize the game board after choosing player

    def create_widgets(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                button = tk.Button(self.root, text=EMPTY, font=('Arial', 24), width=5, height=2, 
                                   command=lambda i=i, j=j: self.player_move(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

    def player_move(self, x, y):
        if self.board[x][y] == EMPTY:
            self.board[x][y] = self.user_player
            self.buttons[x][y].config(text=self.user_player, bg='lightblue')
            if self.check_win(self.user_player):
                self.show_message("Vous avez gagné !")
                return
            if self.is_draw():
                self.show_message("Match nul !")
                return
            self.current_player = self.ai_player
            self.ai_move()
            if self.check_win(self.ai_player):
                self.show_message("L'IA a gagné !")
            if self.is_draw():
                self.show_message("Match nul !")
            self.current_player = self.user_player

    def ai_move(self):
        move = self.find_best_move()
        if move:
            x, y = move
            self.board[x][y] = self.ai_player
            self.buttons[x][y].config(text=self.ai_player, bg='lightcoral')

    def check_win(self, player):
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == player for j in range(BOARD_SIZE)) or \
               all(self.board[j][i] == player for j in range(BOARD_SIZE)):
                return True
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)) or \
           all(self.board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
            return True
        return False

    def is_draw(self):
        return all(cell != EMPTY for row in self.board for cell in row) and \
               not self.check_win(self.user_player) and not self.check_win(self.ai_player)

    def minimax(self, depth, alpha, beta, is_maximizing):
        if self.check_win(self.ai_player):
            return 10 - depth
        if self.check_win(self.user_player):
            return depth - 10
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = self.ai_player
                        score = self.minimax(depth + 1, alpha, beta, False)
                        self.board[i][j] = EMPTY
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            return best_score
            return best_score
        else:
            best_score = float('inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = self.user_player
                        score = self.minimax(depth + 1, alpha, beta, True)
                        self.board[i][j] = EMPTY
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            return best_score
            return best_score

    def find_best_move(self):
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = self.ai_player
                    score = self.minimax(0, alpha, beta, False)
                    self.board[i][j] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def show_message(self, message):
        messagebox.showinfo("Tic-Tac-Toe", message)
        self.reset_game()

    def reset_game(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].config(text=EMPTY, bg='white')

def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
