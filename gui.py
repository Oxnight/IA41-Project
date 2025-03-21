import tkinter as tk
from tkinter import ttk

import teeko_node
from teeko_logique import TeekoGame
from teeko_node import Teeko_node
from graph_builder import grille_complete, best_move
from node_storage import Tekko_Node_Storage

class TeekoMenu:
    """
    Classe représentant le menu principal de configuration du jeu Teeko.
    Permet de choisir la profondeur de l'IA et de démarrer la partie.
    """
    def __init__(self, root):
        """
        Initialise le menu de configuration de Teeko.
        
        @param root: La fenêtre principale de Tkinter.
        """
        self.root = root
        self.root.title("Teeko - Configuration")
        self.root.configure(bg="lightsteelblue")

        self.depth = tk.IntVar(value=3)

        title_label = tk.Label(root, text="Teeko - Jeu à deux joueurs", font=("Helvetica", 20, "bold"), bg="lightsteelblue", fg="darkblue")
        title_label.pack(pady=20)

        depth_label = tk.Label(root, text="Choisissez la profondeur de l'IA :", font=("Helvetica", 16), bg="lightsteelblue", fg="black")
        depth_label.pack(pady=10)

        depth_comment = tk.Label(root, text="Profondeur 2 : Rapide mais moins efficace.\nProfondeur 3 : Équilibré.\nProfondeur 4 : Lent mais très performant (recommandé : 2 ou 3).", font=("Helvetica", 12), bg="lightsteelblue", fg="darkred" , justify="left")
        depth_comment.pack(pady=5)

        depth_spinner = ttk.Spinbox(root, from_=1, to=10, textvariable=self.depth, font=("Helvetica", 14), width=5)
        depth_spinner.pack(pady=10)

        start_button = tk.Button(root, text="Démarrer le jeu", font=("Helvetica", 16, "bold"), bg="green", fg="white", command=self.start_game)
        start_button.pack(pady=20)

    def start_game(self):
        """
        Démarre une nouvelle partie après la configuration.

        Cette méthode ferme le menu et crée une nouvelle instance de la fenêtre du jeu.
        """
        self.root.destroy()
        main_game = tk.Tk()
        TeekoGUI(main_game, depth=self.depth.get())
        main_game.mainloop()

class TeekoGUI:
    """
    Classe représentant l'interface graphique du jeu Teeko.
    Permet de gérer l'affichage du plateau et les interactions avec l'utilisateur.
    """
    def __init__(self, root, depth):
        """
        Initialise l'interface du jeu Teeko avec le plateau et les éléments visuels.

        @param root: La fenêtre principale de Tkinter.
        @param depth: La profondeur de recherche de l'IA choisie par l'utilisateur.
        """
        self.root = root
        self.depth = depth
        self.root.title("Teeko - Jeu à deux joueurs")
        self.root.configure(bg="lightsteelblue")
        self.game = TeekoGame()
        self.cell_size = 100

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white", bd=5, relief="ridge", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.status_label = tk.Label(root, text="Tour du joueur 1 (X)", font=("Helvetica", 16, "bold"), bg="lightsteelblue", fg="darkblue", relief="sunken", pady=10)
        self.status_label.pack(fill="x", pady=10)

        self.progress_frame = tk.Frame(root, bg="lightsteelblue")
        self.progress_frame.pack(pady=10)
        self.progress_label = tk.Label(self.progress_frame, text="", font=("Helvetica", 12), bg="lightsteelblue", fg="darkblue")
        self.progress_label.pack()
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=300, mode="indeterminate")

        self.piece_selected_row = -1
        self.piece_selected_col = -1

        self.game_over = False

        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        """
        Dessine la grille du jeu sur le canevas.
        Cette méthode génère les lignes horizontales et verticales du plateau.
        """
        self.canvas.delete("highlight")
        for row in range(6):
            y = row * self.cell_size
            self.canvas.create_line(0, y, 500, y, fill="slateblue", width=3)
        for col in range(6):
            x = col * self.cell_size
            self.canvas.create_line(x, 0, x, 500, fill="slateblue", width=3)

    def highlight_available_moves(self, moves):
        """
        Met en surbrillance les cases où le joueur peut placer ou déplacer un pion.
        
        @param moves: Liste des mouvements disponibles sous forme de coordonnées (row, col).
        """
        for (row, col) in moves:
            self.canvas.create_rectangle(
                col * self.cell_size + 5,
                row * self.cell_size + 5,
                (col + 1) * self.cell_size - 5,
                (row + 1) * self.cell_size - 5,
                outline="green",
                width=3,
                tags="highlight"
            )

    def draw_pieces(self):
        """
        Dessine les pions sur le plateau de jeu.
        Cette méthode met à jour l'affichage des pions en fonction de l'état actuel du jeu.
        """
        self.canvas.delete("piece")
        for x in range(5):
            for y in range(5):
                piece = self.game.board[x][y]
                if piece != teeko_node.empty:
                    color = "black" if piece == "X" else "white"
                    outline_color = "red" if piece == "X" else "blue"
                    if (x, y) == (self.piece_selected_row, self.piece_selected_col):
                        color = "gold"
                    self.canvas.create_oval(
                        y * self.cell_size + 15,
                        x * self.cell_size + 15,
                        (y + 1) * self.cell_size - 15,
                        (x + 1) * self.cell_size - 15,
                        fill=color,
                        outline=outline_color,
                        width=3,
                        tags="piece"
                    )

    def handle_click(self, event):
        """
        Gère les clics de souris sur le plateau. Cette méthode détermine l'action à entreprendre
        en fonction de la phase du jeu (placement ou déplacement).
        
        @param event: L'événement de clic de souris généré par l'utilisateur.
        """
        if self.game_over:
            return  # On ne fait rien si le jeu est terminé.

        row = event.y // self.cell_size
        col = event.x // self.cell_size

        if self.game.phase == "placement":
            self.game.place_piece(row, col)
            self.update_gui()

            if not self.game.is_game_over():
                self.show_ai_loading()
                self.root.after(100, self.play_ai_turn)

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
        """
        Sélectionne un pion à déplacer. Vérifie si le joueur peut déplacer un pion du joueur actuel.

        @param row: La ligne de la case sur laquelle le joueur a cliqué.
        @param col: La colonne de la case sur laquelle le joueur a cliqué.
        """
        if self.game.board[row][col] == self.game.players[self.game.current_player]:
            self.piece_selected_row = row
            self.piece_selected_col = col
            self.status_label.config(
                text=f"Joueur : {self.game.players[self.game.current_player]}  ||  Pion sélectionné : ligne {row}, colonne {col}"
            )

            if hasattr(self.game, "get_available_moves"):
                available_moves = self.game.get_available_moves(row, col)
            else:
                available_moves = self.simulate_available_moves(row, col)

            self.highlight_available_moves(available_moves)
            self.update_gui()

    def simulate_available_moves(self, row, col):
        """
        Simule les mouvements disponibles pour un pion sur la base des règles génériques de Teeko.

        @param row: La ligne de la case où le pion est actuellement.
        @param col: La colonne de la case où le pion est actuellement.

        @return: Liste des cases disponibles pour déplacer le pion.
        """
        moves = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions : haut, bas, gauche, droite
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 5 and 0 <= new_col < 5 and self.game.board[new_row][new_col] == teeko_node.empty:
                moves.append((new_row, new_col))
        return moves

    def gui_move_piece(self, row, col):
        """
        Déplace le pion sélectionné et permet à l'IA de jouer après le déplacement du joueur.

        @param row: La ligne de la case où le joueur souhaite déplacer le pion.
        @param col: La colonne de la case où le joueur souhaite déplacer le pion.
        """
        if self.piece_selected_row != -1:
            self.game.move_piece(
                row,
                col,
                self.piece_selected_row,
                self.piece_selected_col
            )

            self.piece_selected_row = -1
            self.piece_selected_col = -1

            self.update_gui()

            if not self.game.is_game_over():
                self.show_ai_loading()
                self.root.after(100, self.play_ai_turn)

    def show_ai_loading(self):
        """
        Affiche un message de chargement et une barre de progression lorsque l'IA joue.
        """
        self.progress_label.config(text="Chargement de l'IA...")
        self.progress.pack()
        self.progress.start(10)

    def hide_ai_loading(self):
        """
        Cache le message et la barre de progression après que l'IA a joué.
        """
        self.progress_label.config(text="")
        self.progress.stop()
        self.progress.pack_forget()

    def play_ai_turn(self):
        """
        Fait jouer l'IA en utilisant un algorithme de recherche pour trouver le meilleur coup.
        """
        storage = Tekko_Node_Storage()
        initial_node = Teeko_node(self.game.board, 'O')
        grille_complete(initial_node, storage, max_depth=self.depth)
        meilleure_grille = best_move(initial_node, depth=self.depth, maximizing_player=True)
        self.game.board = meilleure_grille
        self.update_gui()
        self.hide_ai_loading()

        if self.game.is_game_over():
            self.end_game(ai_wins=True)

    def update_gui(self):
        """
        Met à jour l'affichage graphique en fonction des changements dans l'état du jeu.
        """
        self.draw_board()
        self.draw_pieces()
        if not self.game_over:
            status_text = f"Tour du joueur {self.game.current_player + 1} ({self.game.players[self.game.current_player]})"
            if self.game.phase == "déplacement":
                status_text = f"Déplacement - {status_text}"
            self.status_label.config(text=status_text)

    def end_game(self, ai_wins=False):
        """
        Gère la fin de la partie, affiche un message et désactive les interactions avec le plateau.
        
        @param ai_wins: Booléen indiquant si l'IA a gagné ou non.
        """
        self.game_over = True
        if ai_wins:
            winner = "IA"
            self.status_label.config(text=f"L'IA ({winner}) a gagné !", fg="red")
        else:
            winner = self.game.players[self.game.current_player]
            self.status_label.config(text=f"Le joueur {self.game.current_player + 1} ({winner}) a gagné !", fg="green")

        self.canvas.unbind("<Button-1>")
        self.animate_winner()
        self.add_restart_button()

    def animate_winner(self):
        """
        Anime l'interface pour signaler la victoire.
        """
        for _ in range(3):
            self.root.configure(bg="gold")
            self.root.after(200, lambda: self.root.configure(bg="lightsteelblue"))

    def add_restart_button(self):
        """
        Ajoute un bouton de redémarrage de la partie une fois celle-ci terminée.
        """
        restart_button = tk.Button(
            self.root,
            text="Rejouer",
            font=("Helvetica", 16, "bold"),
            bg="blue",
            fg="white",
            command=self.restart_game
        )
        restart_button.pack(pady=20)

    def restart_game(self):
        """
        Redémarre le jeu en revenant au menu principal.
        """
        self.root.destroy()
        root = tk.Tk()
        TeekoMenu(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    TeekoMenu(root)
    root.mainloop()
