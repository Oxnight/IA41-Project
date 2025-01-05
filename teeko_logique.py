import teeko_node

class TeekoGame:
    """
    Classe représentant un jeu de Teeko avec un plateau 5x5.
    Permet de gérer les phases de placement et de déplacement des pions, ainsi que la vérification de la victoire.
    """

    def __init__(self):
        """
        Initialise le plateau de jeu, les joueurs, et l'état du jeu.
        - Le plateau est une grille 5x5 vide.
        - Deux joueurs sont définis : 'X' et 'O'.
        - Le joueur actuel commence à l'index 0 (X).
        - Le jeu commence en phase de placement.
        """
        self.board = [[teeko_node.empty for x in range(5)] for x in range(5)]  # Initialisation d'un plateau vide
        self.players = ['X', 'O']  # Définition des joueurs
        self.current_player = 0  # Le joueur actuel (X commence)
        self.phase = "placement"  # La phase actuelle est le placement
        self.move_count = 0  # Le nombre de coups effectués

    def display_board(self):
        """
        Affiche le plateau de jeu sous forme texte dans la console.
        Cette fonction est utilisée pour afficher l'état actuel du jeu.
        """
        for row in self.board:
            print(' | '.join(row))  # Affichage de chaque ligne du plateau
            print('-' * 9)  # Séparateur entre les lignes

    def is_valid_placement(self, x, y):
        """
        Vérifie si une position sur le plateau est valide pour placer un pion.
        Une position est valide si la case est vide.
        
        @param x: L'index de la ligne de la case.
        @param y: L'index de la colonne de la case.
        
        @return: True si la case est vide, sinon False.
        """
        return self.board[x][y] == teeko_node.empty  # Vérifie si la case est vide

    def place_piece(self, ligne, colonne):
        """
        Place un pion sur le plateau à la position spécifiée, si c'est une phase de placement.
        
        @param ligne: La ligne où le pion doit être placé.
        @param colonne: La colonne où le pion doit être placé.
        
        @raise Exception: Si la phase n'est pas la phase de placement.
        @raise ValueError: Si l'emplacement est invalide (case déjà occupée).
        """
        if self.phase != "placement":  # Vérifie que la phase est bien celle du placement
            raise Exception("La phase actuelle n'est pas la phase de placement.")
        if self.is_valid_placement(ligne, colonne):  # Vérifie que la case est vide
            self.board[ligne][colonne] = self.players[self.current_player]  # Place le pion
            self.move_count += 1  # Augmente le nombre de coups
            if self.move_count == 4:  # Passe à la phase de déplacement après 4 placements
                self.phase = "déplacement"
        else:
            raise ValueError("Emplacement invalide pour placement.")  # L'emplacement est déjà occupé

    def is_valid_move(self, ligne_final, colonne_final, ligne_initiale, colonne_initiale):
        """
        Vérifie si un déplacement est valide pendant la phase de déplacement.
        
        @param ligne_final: La ligne de la destination.
        @param colonne_final: La colonne de la destination.
        @param ligne_initiale: La ligne de la source.
        @param colonne_initiale: La colonne de la source.
        
        @return: True si le déplacement est valide, sinon False.
        """
        if self.phase != "déplacement":  # Vérifie que la phase est bien celle du déplacement
            return False
        if self.board[ligne_initiale][colonne_initiale] != self.players[self.current_player]:  # Vérifie que le pion appartient au joueur actuel
            return False
        if self.board[ligne_final][colonne_final] != teeko_node.empty:  # Vérifie que la case de destination est vide
            return False
        # Vérifie si la destination est adjacente à la position initiale
        return abs(ligne_initiale - ligne_final) <= 1 and abs(colonne_initiale - colonne_final) <= 1

    def move_piece(self, ligne_final, colonne_final, ligne_initiale, colonne_initiale):
        """
        Déplace un pion d'une position à une autre si le déplacement est valide.
        
        @param ligne_final: La ligne de la destination.
        @param colonne_final: La colonne de la destination.
        @param ligne_initiale: La ligne de la source.
        @param colonne_initiale: La colonne de la source.
        
        @raise ValueError: Si le déplacement est invalide.
        """
        if self.is_valid_move(ligne_final, colonne_final, ligne_initiale, colonne_initiale):  # Vérifie que le déplacement est valide
            self.board[ligne_initiale][colonne_initiale] = teeko_node.empty  # Vide la case source
            self.board[ligne_final][colonne_final] = self.players[self.current_player]  # Déplace le pion
        else:
            raise ValueError("Déplacement invalide.")  # Le déplacement est invalide

    @staticmethod
    def check_win(player, board):
        """
        Vérifie si un joueur a gagné selon les règles du jeu de Teeko.
        Un joueur gagne s'il aligne 4 de ses pions sur une ligne, une colonne ou une diagonale.
        
        @param player: Le joueur ('X' ou 'O').
        @param board: L'état actuel du plateau de jeu (5x5).
        
        @return: True si le joueur a gagné, sinon False.
        """
        for l in range(5):  # Vérifie les alignements horizontaux
            for c in range(2):
                if all(board[l][c + p] == player for p in range(4)):
                    return True

        for c in range(5):  # Vérifie les alignements verticaux
            for l in range(2):
                if all(board[l + p][c] == player for p in range(4)):
                    return True

        # Vérification des diagonales descendantes
        for l in range(2):
            for c in range(2):
                if all(board[l + p][c + p] == player for p in range(4)):
                    return True

        # Vérification des diagonales ascendantes
        for l in range(3, 5):
            for c in range(2):
                if all(board[l - p][c + p] == player for p in range(4)):
                    return True

        return False

    def switch_player(self):
        """
        Change le joueur actuel (alterne entre 0 et 1).
        """
        self.current_player = 1 - self.current_player  # Alterne entre 0 et 1 pour changer de joueur

    def is_game_over(self):
        """
        Vérifie si la partie est terminée en vérifiant si un joueur a gagné.
        
        @return: True si la partie est terminée (un joueur a gagné), sinon False.
        """
        j1 = self.players[0]
        j2 = self.players[1]
        if self.check_win(j1, self.board) or self.check_win(j2, self.board):  # Vérifie si un joueur a gagné
            return True
        return False

    @staticmethod
    def count_partial_alignments(player, state):
        """
        Compte les alignements partiels (lignes, colonnes, diagonales) où un joueur a 2 pions
        et une case vide.
        
        @param player: Le joueur ('X' ou 'O').
        @param state: L'état actuel du plateau de jeu (5x5).
        
        @return: Le nombre d'alignements partiels.
        """
        alignments = 0

        # Vérification des lignes
        for row in state:
            for i in range(3):
                segment = row[i:i + 3]
                if segment.count(player) == 2 and segment.count(teeko_node.empty) == 1:
                    alignments += 1

        # Vérification des colonnes
        for col in range(5):
            col_values = [state[row][col] for row in range(5)]
            for i in range(3):
                segment = col_values[i:i + 3]
                if segment.count(player) == 2 and segment.count(teeko_node.empty) == 1:
                    alignments += 1

        # Vérification des diagonales
        for i in range(3):
            for j in range(3):
                diagonal_1 = [state[i + k][j + k] for k in range(3)]
                if diagonal_1.count(player) == 2 and diagonal_1.count(teeko_node.empty) == 1:
                    alignments += 1

                diagonal_2 = [state[i + k][j + 2 - k] for k in range(3)]
                if diagonal_2.count(player) == 2 and diagonal_2.count(teeko_node.empty) == 1:
                    alignments += 1

        return alignments
