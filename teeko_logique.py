import teeko_node

class TeekoGame:
    def __init__(self):
        # Initialisation du plateau de jeu (5x5)
        self.board = [[teeko_node.empty for x in range(5)] for x in range(5)]
        self.players = ['X', 'O']  # X pour le joueur 1, O pour le joueur 2
        self.current_player = 0  # Index du joueur actuel (0 ou 1)
        self.phase = "placement"  # Peut etre "placement" ou "déplacement"
        self.move_count = 0  # Compteur pour vérifier la fin de la phase de déplacement

    def display_board(self):
        """Affiche le plateau dans un format texte (débogage)."""
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)

    def is_valid_placement(self, x, y):
        """Vérifie si un emplacement est valide pour poser un pion."""
        return self.board[x][y] == teeko_node.empty

    def place_piece(self, ligne, colonne):
        """Place un pion sur le plateau."""
        if self.phase != "placement":
            raise Exception("La phase actuelle n'est pas la phase de placement.")
        if self.is_valid_placement(ligne, colonne):

            self.board[ligne][colonne] = self.players[self.current_player]
            self.move_count += 1
            # Passe à la phase de déplacement après 8 placements
            if self.move_count == 4:
                self.phase = "déplacement"
        else:
            raise ValueError("Emplacement invalide pour placement.")

    def is_valid_move(self, ligne_final, colonne_final, ligne_initiale,
                      colonne_initiale):  # x1 y1 = pion initialemenet placer  y2 = i
        """Vérifie si un déplacement est valide."""
        if self.phase != "déplacement":
            return False
        if self.board[ligne_initiale][colonne_initiale] != self.players[self.current_player]:
            return False
        if self.board[ligne_final][colonne_final] != teeko_node.empty:
            return False
        # Vérifie si la destination est adjacente
        return abs(ligne_initiale - ligne_final) <= 1 and abs(colonne_initiale - colonne_final) <= 1

    def move_piece(self, ligne_final, colonne_final, ligne_initiale,
                   colonne_initiale):  # x1 y1 future deplacement x2 y2 position de base
        """Déplace un pion sur le plateau."""
        if self.is_valid_move(ligne_final, colonne_final, ligne_initiale, colonne_initiale):
            self.board[ligne_initiale][colonne_initiale] = teeko_node.empty
            self.board[ligne_final][colonne_final] = self.players[self.current_player]


        else:
            raise ValueError("Déplacement invalide.")

    @staticmethod
    def check_win(player, board):
        """Vérifie si le joueur actuel a gagné dans une grille donnée."""
        # Logique de vérification des conditions de victoire
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

            # Vérifier pour le premier X [1][1]
        if board[1][1] == player:
            if (board[0][1] == player and board[0][0] == player and board[1][0] == player):
                return True
            if (board[0][2] == player and board[1][2] == player and board[0][1] == player):
                return True
            if (board[1][2] == player and board[2][1] == player and board[2][2] == player):
                return True
            if (board[1][0] == player and board[2][0] == player and board[2][1] == player):
                return True

            # Vérifier pour le deuxième X [1][3]
        if board[1][3] == player:
            if (board[0][3] == player and board[0][2] == player and board[1][2] == player):
                return True
            if (board[0][4] == player and board[0][3] == player and board[1][4] == player):
                return True
            if (board[2][3] == player and board[2][4] == player and board[1][4] == player):
                return True
            if (board[2][2] == player and board[2][3] == player and board[1][2] == player):
                return True

            # Vérifier pour le troisième X [3][3]
        if board[3][3] == player:
            if (board[2][3] == player and board[2][2] == player and board[3][2] == player):
                return True
            if (board[2][4] == player and board[2][3] == player and board[3][4] == player):
                return True
            if (board[4][4] == player and board[4][3] == player and board[3][4] == player):
                return True
            if (board[4][2] == player and board[4][3] == player and board[3][2] == player):
                return True

            # Vérifier pour le quatrième X [3][1]
        if board[3][1] == player:
            if (board[2][1] == player and board[2][0] == player and board[3][0] == player):
                return True
            if (board[2][2] == player and board[2][1] == player and board[3][2] == player):
                return True
            if (board[4][2] == player and board[4][1] == player and board[3][2] == player):
                return True
            if (board[4][0] == player and board[4][1] == player and board[3][0] == player):
                return True

        return False

    def switch_player(self):
        """Passe au joueur suivant."""
        self.current_player = 1 - self.current_player

    def is_game_over(self):
        # Vérification pour les deux joueurs
        j1 = self.players[0]
        j2 = self.players[1]

        # Si l'un des deux joueurs a gagné, la partie est finie
        if self.check_win(j1, self.board) or self.check_win(j2, self.board):
            return True
        return False

    @staticmethod
    def count_partial_alignments(player, state):
        """
        Compte les alignements partiels (lignes, colonnes, diagonales) pour un joueur donné.
        Un alignement partiel consiste en une suite de 3 cases (sur une ligne, colonne ou diagonale)
        qui contient exactement 2 pions du joueur et 1 case vide.

        Arguments :
        - player : str, le joueur ('X' ou 'O').
        - state : list[list[str]], la grille actuelle (5x5).

        Retourne :
        - int : Le nombre d'alignements partiels pour le joueur.
        """
        alignments = 0

        # Vérification des lignes
        for row in state:
            # On peut regarder les sous-séquences de 3 cases : indices [0..2], [1..3], [2..4]
            for i in range(3):
                segment = row[i:i + 3]
                if segment.count(player) == 2 and segment.count(teeko_node.empty) == 1:
                    alignments += 1

        # Vérification des colonnes
        for col in range(5):
            # Construction de la colonne col_values
            col_values = [state[row][col] for row in range(5)]
            for i in range(3):
                segment = col_values[i:i + 3]
                if segment.count(player) == 2 and segment.count(teeko_node.empty) == 1:
                    alignments += 1

        # Vérification des diagonales (3x3 dans un 5x5)
        for i in range(3):
            for j in range(3):
                # Diagonale principale (vers le bas à droite)
                diagonal_1 = [state[i + k][j + k] for k in range(3)]
                if diagonal_1.count(player) == 2 and diagonal_1.count(teeko_node.empty) == 1:
                    alignments += 1

                # Diagonale secondaire (vers le bas à gauche)
                diagonal_2 = [state[i + k][j + 2 - k] for k in range(3)]
                if diagonal_2.count(player) == 2 and diagonal_2.count(teeko_node.empty) == 1:
                    alignments += 1

        return alignments
