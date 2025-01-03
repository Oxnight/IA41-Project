class TeekoGame:
    def __init__(self):
        # Initialisation du plateau de jeu (5x5)
        self.board = [[' ' for x in range(5)] for x in range(5)]
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

    def place_piece(self, ligne, colonne):
        """Place un pion sur le plateau."""
        if self.phase != "placement":
            raise Exception("La phase actuelle n'est pas la phase de placement.")
        if self.is_valid_placement(ligne, colonne):
      
            self.board[ligne][colonne] = self.players[self.current_player]
            self.move_count += 1
            self.switch_player()
            # Passe à la phase de déplacement après 8 placements
            if self.move_count == 8:
                self.phase = "déplacement"
        else :
            raise ValueError("Emplacement invalide pour placement.")

    def is_valid_move(self, ligne_final, colonne_final, ligne_initiale, colonne_initiale): #x1 y1 = pion initialemenet placer  y2 = i
        """Vérifie si un déplacement est valide."""
        if self.phase != "déplacement":
         
            return False
        if self.board[ligne_initiale][colonne_initiale] != self.players[self.current_player]:
           
            return False
        if self.board[ligne_final][colonne_final] != ' ':
     
            return False
        # Vérifie si la destination est adjacente
        return abs(ligne_initiale - ligne_final) <= 1 and abs(colonne_initiale - colonne_final) <= 1
    
    def move_piece(self, ligne_final, colonne_final, ligne_initiale, colonne_initiale): #x1 y1 future deplacement x2 y2 position de base
        """Déplace un pion sur le plateau."""
        if self.is_valid_move(ligne_final, colonne_final, ligne_initiale, colonne_initiale):
            self.board[ligne_initiale][colonne_initiale] = ' '
            self.board[ligne_final][colonne_final] = self.players[self.current_player]
            self.switch_player()

        else:
            raise ValueError("Déplacement invalide.")

    def check_win(self,player):
        """Vérifie si le joueur actuel a gagné."""


        # Vérification des alignements horizontaux
        for l in range(5):  # Parcourt chaque ligne
            for c in range(2):  # Vérifie les séquences de 4 colonnes possibles
                bool = True  # On suppose que c'est un alignement gagnant
                for p in range(4):  # Vérifie les 4 cases consécutives
                    if self.board[l][c + p] != player:
                        bool = False  # Ce n'est pas un alignement gagnant
                        break  # Arrête la vérification pour ce groupe
                if bool:  # Si c'est un alignement gagnant
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

        # Vérifier pour le deuligne_initialeème X [1][3]
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
        # Vérification pour les deux joueurs
        j1 = self.players[0]
        j2 = self.players[1]

        # Si l'un des deux joueurs a gagné, la partie est finie
        if self.check_win(j1) or self.check_win(j2):
            return True
        return False



