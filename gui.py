import tkinter as tk
from teeko_logique import TeekoGame


class TeekoGUI:
    def __init__(self, root):
        self.root = root  # Fenêtre principale
        self.root.title("Teeko - Jeu à deux joueurs")
        self.game = TeekoGame()
        self.cell_size = 100  # Taille des cellules du plateau
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()
        self.status_label = tk.Label(root, text="Tour du joueur 1 (X)", font=("Arial", 16))
        self.status_label.pack()
        self.draw_board()

        # Indicateur de fin de jeu
        self.game_over = False

        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        """Dessine le plateau de jeu."""
        for ligne in range(6):  # Lignes et colonnes (5x5 + lignes de bordure)
            position_y = ligne * self.cell_size
            self.canvas.create_line(0, position_y, 500, position_y, fill="black", width=3)

        for colonne in range(6):
            position_x = colonne * self.cell_size
            self.canvas.create_line(position_x, 0, position_x, 500, fill="black", width=3)

    def draw_pieces(self):
        """Dessine les pions sur le plateau."""
        self.canvas.delete("piece")  # Supprime les anciens pions
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
        """Gère les clics de l'utilisateur."""
        if self.game_over:  # Si le jeu est terminé, ignore les clics
            return

        x = event.y // self.cell_size
        y = event.x // self.cell_size

        try:
            if self.game.phase == "placement":
                self.game.place_piece(x, y)
                self.draw_pieces()  # Dessiner le dernier pion avant la vérification

                # Vérifier si un joueur a gagné après le placement
                if self.game.is_game_over():
                    self.end_game()
                    return  # Stoppe l'exécution après la victoire

            elif self.game.phase == "déplacement":
                if not hasattr(self, "selected_piece"):
                    # Sélection d'un pion
                    if self.game.board[x][y] == self.game.players[self.game.current_player]:
                        self.selected_piece = (x, y)
                        self.status_label.config(text=f"Pion sélectionné en ({x}, {y})")
                    else:
                        self.status_label.config(text="Sélection invalide, choisissez un de vos pions.")
                else:
                    # Déplacement d'un pion
                    x1, y1 = self.selected_piece
                    self.game.move_piece(x1, y1, x, y)
                    self.selected_piece = None
                    self.draw_pieces()  # Dessiner le pion déplacé avant la vérification

                    # Vérification de la victoire après le déplacement
                    if self.game.is_game_over():
                        self.end_game()
                        return  # Stoppe l'exécution après la victoire

            self.update_gui()

        except ValueError as e:
            self.status_label.config(text=str(e))
        except Exception as e:
            self.status_label.config(text="Erreur : " + str(e))

    def update_gui(self):
        """Met à jour l'interface après chaque action."""
        self.draw_pieces()
        if not self.game_over:  # Ne met à jour le statut que si le jeu n'est pas terminé
            if self.game.phase == "placement":
                self.status_label.config(
                    text=f"Tour du joueur {self.game.current_player + 1} ({self.game.players[self.game.current_player]})")
            else:
                self.status_label.config(
                    text=f"Déplacement - Tour du joueur {self.game.current_player + 1} ({self.game.players[self.game.current_player]})")

    def end_game(self):
        """Affiche un message lorsque le jeu se termine."""
        self.game_over = True  # Marquer la fin du jeu
        winner = self.game.players[self.game.current_player]
        print(f"Winner detected: Player {self.game.current_player + 1} ({winner})")
        self.status_label.config(text=f"Le joueur {self.game.current_player + 1} ({winner}) a gagné !")
        self.root.update_idletasks()  # Force la mise à jour de l'interface
        self.canvas.unbind("<Button-1>")  # Désactive les clics sur le plateau


# Lancement de l'interface graphique
if __name__ == "__main__":
    root = tk.Tk()
    app = TeekoGUI(root)
    root.mainloop()
