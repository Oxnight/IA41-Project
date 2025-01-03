from teeko_logique import TeekoGame

player_1 = 'X'
player_2 = 'O'
empty = ' '
non_eval = -2



class Teeko_node:
    def __init__(self, state: list[list[str]], player: str):
        self.state = state  # Grille actuelle (5x5) avec 'X', 'O', et ' '
        self.player = player  # Joueur courant ('X' ou 'O')
        self.childrens = []  # Liste des nœuds enfants
        self.fathers = []  # Liste des nœuds parents
        self.value = non_eval  # Valeur du nœud (non évalué par défaut)

    def is_winner(self) :
        """Vérifie si l'état représenté par ce noeud est un état gagnant pour le joueur."""
        game = TeekoGame()
        return game.check_win(self.player, self.state)

    def eval(self):
        """
        Évalue la grille du point de vue de 'O'.
        Retourne une valeur dans [-1, 1] où :
        - +1 est une victoire pour 'O'
        - -1 est une victoire pour 'X'
        """
        if TeekoGame.check_win('O', self.state):
            return 1.0
        if TeekoGame.check_win('X', self.state):
            return -1.0

        positions_O, positions_X = [], []
        alignment_zones_O, alignment_zones_X = {}, {}

        # Collecter les positions et analyser les alignements
        for r in range(5):
            for c in range(5):
                val = self.state[r][c]
                if val == 'O':
                    positions_O.append((r, c))
                    self.update_alignment_zones(r, c, alignment_zones_O)
                elif val == 'X':
                    positions_X.append((r, c))
                    self.update_alignment_zones(r, c, alignment_zones_X)

        # Alignements partiels
        alignments_O = TeekoGame.count_partial_alignments('O', self.state)
        alignments_X = TeekoGame.count_partial_alignments('X', self.state)

        # Détection des zones chaudes
        hot_spots_O = len([zone for zone, count in alignment_zones_O.items() if count >= 2])
        hot_spots_X = len([zone for zone, count in alignment_zones_X.items() if count >= 2])

        # Pondérations dynamiques
        nb_O, nb_X = len(positions_O), len(positions_X)
        total_pieces = nb_O + nb_X

        if total_pieces < 6:
            w_align, w_hot_spot, w_defense = 0.6, 0.4, 0.7
        elif total_pieces < 14:
            w_align, w_hot_spot, w_defense = 0.5, 0.5, 0.6
        else:
            w_align, w_hot_spot, w_defense = 0.4, 0.6, 0.5

        # Calcul des scores
        score_O = (
                w_align * alignments_O
                + w_hot_spot * hot_spots_O
        )
        score_X = (
                w_align * alignments_X
                + w_hot_spot * hot_spots_X
        )

        # Défense : Pénaliser les alignements adverses menaçant une victoire
        if alignments_X >= 3:
            score_X += w_defense * 1.0

        raw_value = score_O - score_X
        denom = abs(score_O) + abs(score_X) + 1e-5
        return raw_value / denom

    def update_alignment_zones(self, row, col, alignment_zones):
        """
        Met à jour les zones chaudes (positions proches d'alignements) pour un joueur.
        """
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1)  # Horizontal, vertical, diagonale
        ]
        for dr, dc in directions:
            for step in range(1, 3):
                nr, nc = row + dr * step, col + dc * step
                if 0 <= nr < 5 and 0 <= nc < 5 and self.state[nr][nc] == ' ':
                    if (nr, nc) not in alignment_zones:
                        alignment_zones[(nr, nc)] = 0
                    alignment_zones[(nr, nc)] += 1

    def add_child(self, child: 'Teeko_node'):
        """Ajoute un enfant au nœud et met ce nœud comme parent de l'enfant."""
        # Déterminer automatiquement le joueur pour l'enfant
        child.player = 'O' if self.player == 'X' else 'X'

        self.childrens.append(child)
        child.fathers.append(self)

    @staticmethod
    def sort_childrens(self):  ## Trie les enfants de la node en fonction de leur valeur par ordre décroissant
        self.childrens = sorted(self.childrens, key=lambda x: x.value, reverse=True)
