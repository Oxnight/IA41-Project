class TeekoGame:
    def __init__(self):
        # Initialisation du plateau de jeu (5x5)
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.players = ['X', 'O'] # X pour le joueur 1, O pour le joueur 2
        self.current_player = 0 # Index du joueur actuel (0 ou 1)
        self.phase = "placement" # Peut etre "placement" ou "déplacement"
        self.move_count = 0 # Compteur pour vérifier la fin de la phase de déplacement

    def display_board(self):
        """Affiche le plateau dans un format texte (débogage)."""
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)

    def is_valid_placement(self, x, y):
        """Vérifie si un emplacement est valide pour poser un pion."""
        return self.board[x][y] == ' '

    def place_piece(self, x, y):
        """Place un pion sur le plateau."""
        if self.phase != "placement":
            raise Exception("La phase actuelle n'est pas la phase de placement.")
        if self.is_valid_placement(x, y):
            self.board[x][y] = self.players[self.current_player]
            self.move_count += 1
            self.check_win()
            self.switch_player()

            # Passe à la phase de déplacement après 8 placements
            if self.move_count == 8:
                self.phase = "déplacement"
        else :
            raise ValueError("Emplacement invalide pour placement.")

    def is_valid_move(self, x1, y1, x2, y2): #x1 y1 = pion initialemenet placer
        """Vérifie si un déplacement est valide."""
        if self.phase != "déplacement":
            return False
        if self.board[x1][y1] != self.players[self.current_player]:
            return False
        if self.board[x2][y2] != ' ':
            return False
        # Vérifie si la destination est adjacente
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1
    
    def move_piece(self, x1, y1, x2, y2):
        """Déplace un pion sur le plateau."""
        if self.is_valid_move(x1, y1, x2, y2):
            self.board[x1][y1] = ' '
            self.board[x2][y2] = self.players[self.current_player]
            self.switch_player()
        else:
            raise ValueError("Déplacement invalide.")

    def check_win(self):
        """Vérifie si le joueur actuel a gagné."""

        player = self.players[self.current_player]
        # Vérification des alignements horizontaux
        for l in range(5):  # Parcourt chaque ligne
            for c in range(2):  # Vérifie les séquences de 4 colonnes possibles
                bool = True  # On suppose que c'est un alignement gagnant
                for p in range(4):  # Vérifie les 4 cases consécutives
                    if self.board[l][c + p] != player:
                        bool = False  # Ce n'est pas un alignement gagnant
                        break  # Arrête la vérification pour ce groupe
                if bool:  # Si c'est un alignement gagnant
                    print(f"Le joueur {player} a gagné (alignement horizontal)!")
                    return True  # Victoire trouvée

        #Verification des alignement Vertical
        for c in range(5):
            for l in range(2):
                bool = True
                for p in range(4):
                    if self.board[l+p][c] != player:
                        bool = False
                        break
                if bool:
                    print(f"Le joueur {player} a gagné (alignement vertical)!")
                    return True

        #Verification des alignement Diagonal
        #Diagonal descendante
        for l in range (2):
            for c in range(2):
                bool = True
                for p in range (4):
                    if self.board[l+p][c+p] != player:
                        bool = False
                        break
                if bool :
                    print(f"Le joueur {player} a gagné (diagonale descendante)!")
                    return True
        #Diagonal ascendante
        for l in range (3,5):
            for c in range(2):
                bool = True
                for p in range(4):
                    if self.board[l - p][c + p] != player:
                        bool = False
                        break
                if bool:
                    print(f"Le joueur {player} a gagné (diagonale ascendante)!")
                    return True


        #Verifier pour le premier X[1,1]
        if self.board[1][1] == player:
            if (self.board[0][1] == player and self.board[0][0] == player and self.board[1][0] == player):
                return True
            if (self.board[0][2] == player and self.board[1][2] == player and self.board[0][1] == player):
                return True
            if (self.board[1][2] == player and self.board[2][1] == player and self.board[2][2] == player):
                return True
            if (self.board[1][0] == player and self.board[2][0] == player and self.board[2][1] == player):
                return True

        # Vérifier pour le deuxième X [1][3]
        if self.board[1][3] == player:
            if (self.board[0][3] == player and self.board[0][2] == player and self.board[1][2] == player):
                return True
            if (self.board[0][4] == player and self.board[0][3] == player and self.board[1][4] == player):
                return True
            if (self.board[2][3] == player and self.board[2][4] == player and self.board[1][4] == player):
                return True
            if (self.board[2][2] == player and self.board[2][3] == player and self.board[1][2] == player):
                return True

        # Vérifier pour le troisième X [3][3]
        if self.board[3][3] == player:
            if (self.board[2][3] == player and self.board[2][2] == player and self.board[3][2] == player):
                return True
            if (self.board[2][4] == player and self.board[2][3] == player and self.board[3][4] == player):
                return True
            if (self.board[4][4] == player and self.board[4][3] == player and self.board[3][4] == player):
                return True
            if (self.board[4][2] == player and self.board[4][3] == player and self.board[3][2] == player):
                return True

        # Vérifier pour le quatrième X [3][1]
        if self.board[3][1] == player:
            if (self.board[2][1] == player and self.board[2][0] == player and self.board[3][0] == player):
                return True
            if (self.board[2][2] == player and self.board[2][1] == player and self.board[3][2] == player):
                return True
            if (self.board[4][2] == player and self.board[4][1] == player and self.board[3][2] == player):
                return True
            if (self.board[4][0] == player and self.board[4][1] == player and self.board[3][0] == player):
                return True
        return False

    def switch_player(self):
        """Passe au joueur suivant."""
        self.current_player = 1 - self.current_player

    def is_game_over(self):
        return self.check_win()



