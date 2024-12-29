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

     ############################ Second Part: Move and State Generation ############################

    def get_taken_positions(self, grid):
        """
        Renvoie toutes les positions déjà occupées sur la grille.

        Paramètres :
            grid : list[list] - La grille actuelle du jeu.

        Retourne :
            taken_positions : list[tuple] - Une liste des positions (row, col) occupées.
        """
        taken_positions = []
        for row in range(5):  # Parcourt les lignes
            for col in range(5):  # Parcourt les colonnes
                if grid[row][col] != ' ':  # Vérifie si la case n'est pas vide
                    taken_positions.append((row, col))  # Ajoute la position occupée
        return taken_positions

    def generate_new_state(self, grid, row, col, player):
        """
        Génère une nouvelle grille avec le pion du joueur placé à une position spécifique.

        Paramètres :
            grid : list[list] - La grille actuelle du jeu.
            row : int - La ligne où placer le pion.
            col : int - La colonne où placer le pion.
            player : int - Le joueur qui place le pion.

        Retourne :
            new_grid : list[list] - Une copie indépendante de la grille avec le pion placé.
        """
        new_grid = [[grid[r][c] for c in range(5)] for r in range(5)]
        new_grid[row][col] = player
        return new_grid

    def move_generation_placement(self, current_grid, current_player):
        """
        Génère tous les états possibles pour le placement d'un pion.

        Paramètres :
            current_grid : list[list] - La grille actuelle du jeu.
            current_player : int - Le joueur qui place le pion.

        Retourne :
            possible_grids : list[list[list]] - Une liste des nouvelles grilles possibles après placement.
        """
        possible_grids = []
        taken_positions = self.get_taken_positions(current_grid)
        for row in range(5):
            for col in range(5):
                if (row, col) not in taken_positions:
                    new_grid = self.generate_new_state(current_grid, row, col, current_player)
                    possible_grids.append(new_grid)
        return possible_grids

    def get_positions_of_current_player(self, grid, player):
        """
        Renvoie toutes les positions occupées par les pions du joueur courant.

        Paramètres :
            grid : list[list] - La grille actuelle du jeu.
            player : int - Le joueur dont on cherche les positions.

        Retourne :
            positions : list[tuple] - Une liste des positions (row, col) occupées par le joueur.
        """
        positions = []
        for row in range(5):
            for col in range(5):
                if grid[row][col] == player:
                    positions.append((row, col))
        return positions

    def generate_adjacent_positions(self, current_grid, current_player, ligne, colonne):
        """
        Génère de nouvelles grilles pour chaque position adjacente valide autour d'une case donnée.

        Paramètres :
            current_grid : list[list] - La grille actuelle.
            current_player : int - Le joueur effectuant le déplacement.
            ligne : int - Ligne actuelle du pion.
            colonne : int - Colonne actuelle du pion.

        Retourne :
            possible_grids : list[list[list]] - Une liste des nouvelles grilles possibles.
        """
        possible_grids = []
        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1),
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]

        for d_ligne, d_colonne in directions:
            new_ligne, new_colonne = ligne + d_ligne, colonne + d_colonne
            if 0 <= new_ligne < 5 and 0 <= new_colonne < 5 and current_grid[new_ligne][new_colonne] == ' ':
                new_grid = self.generate_new_state(current_grid, ligne, colonne, current_player)
                new_grid[new_ligne][new_colonne] = current_player
                new_grid[ligne][colonne] = ' '
                possible_grids.append(new_grid)
        return possible_grids

    def move_generation_deplacement(self, current_grid, current_player):
        """
        Génère tous les états possibles pour le déplacement des pions du joueur.

        Paramètres :
            current_grid : list[list] - La grille actuelle.
            current_player : int - Le joueur effectuant le déplacement.

        Retourne :
            possible_grids : list[list[list]] - Une liste des nouvelles grilles possibles après déplacement.
        """
        possible_grids = []
        player_positions = self.get_positions_of_current_player(current_grid, current_player)
        for ligne, colonne in player_positions:
            adjacent_grids = self.generate_adjacent_positions(current_grid, current_player, ligne, colonne)
            possible_grids.extend(adjacent_grids)
        return possible_grids



