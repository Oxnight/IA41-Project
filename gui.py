import tkinter as tk
from teeko_logique import TeekoGame


class TeekoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Teeko - Jeu à deux joueurs")
        self.game = TeekoGame()
        self.cell_size = 100
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()
        self.status_label = tk.Label(root, text="Tour du joueur 1 (X)", font=("Arial", 16))
        self.status_label.pack()

        self.piece_selected_row = -1
        self.piece_selected_col = -1
        self.game_over = False

        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        """Draw the game board grid."""
        for row in range(6):
            y = row * self.cell_size
            self.canvas.create_line(0, y, 500, y, fill="black", width=3)
        for col in range(6):
            x = col * self.cell_size
            self.canvas.create_line(x, 0, x, 500, fill="black", width=3)

    def draw_pieces(self):
        """Draw the game pieces."""
        self.canvas.delete("piece")
        for x in range(5):
            for y in range(5):
                piece = self.game.board[x][y]
                if piece != ' ':
                    color = "black" if piece == "X" else "white"
                    self.canvas.create_oval(
                        y * self.cell_size + 10,
                        x * self.cell_size + 10,
                        (y + 1) * self.cell_size - 10,
                        (x + 1) * self.cell_size - 10,
                        fill=color,
                        outline="grey",
                        tags="piece"
                    )

    def handle_click(self, event):
        """Handle user click events."""
        if self.game_over:
            return

        row = event.y // self.cell_size
        col = event.x // self.cell_size

        if self.game.phase == "placement":
            self.game.place_piece(row, col)
            self.update_gui()

            if self.game.is_game_over():
                self.end_game()

        elif self.game.phase == "déplacement":
            if self.piece_selected_row == -1:
                self.select_piece(row, col)
            else:
                self.gui_move_piece(row, col)

            if self.game.is_game_over():
                self.end_game()

    def select_piece(self, row, col):
        """Select a piece to move."""
        if self.game.board[row][col] == self.game.players[self.game.current_player]:
            self.piece_selected_row = row
            self.piece_selected_col = col
            self.status_label.config(
                text=f"Joueur : {self.game.players[self.game.current_player]}  ||  Pion sélectionné : ligne {row}, colonne {col}"
            )

    def gui_move_piece(self, row, col):
        """Move a selected piece."""
        if self.piece_selected_row != -1:
            self.game.move_piece(row, col, self.piece_selected_row, self.piece_selected_col)
            self.piece_selected_row = -1
            self.piece_selected_col = -1
            self.update_gui()

    def update_gui(self):
        """Update the GUI after each move."""
        self.draw_pieces()
        if not self.game_over:
            status_text = f"Tour du joueur {self.game.current_player + 1} ({self.game.players[self.game.current_player]})"
            if self.game.phase == "déplacement":
                status_text = f"Déplacement - {status_text}"
            self.status_label.config(text=status_text)

    def end_game(self):
        """Handle game over state."""
        self.game_over = True
        winner = self.game.players[self.game.current_player]
        self.status_label.config(text=f"Le joueur {self.game.current_player + 1} ({winner}) a gagné !")
        self.canvas.unbind("<Button-1>")


if __name__ == "__main__":
    root = tk.Tk()
    app = TeekoGUI(root)
    root.mainloop()
