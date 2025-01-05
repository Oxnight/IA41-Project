from teeko_logique import TeekoGame
import teeko_node

def get_taken_positions(grid):
    """
    Renvoie toutes les positions déjà occupées sur la grille.

    @param grid : list[list[str]] - La grille actuelle du jeu
    @return taken_positions : list[tuple[int, int]] - Liste des positions (ligne, colonne) occupées.
    """
    taken_positions = []
    for row in range(5):  # Parcourt les lignes de la grille
        for col in range(5):  # Parcourt les colonnes de la grille
            if grid[row][col] != teeko_node.empty:  # Si la case est occupée
                taken_positions.append((row, col))  # Ajoute la position occupée à la liste
    return taken_positions

def generate_new_state(grid, row, col, player):
    """
    Génère une nouvelle grille avec un pion placé à une position spécifique.

    @param grid : list[list[str]] - La grille actuelle du jeu
    @param row : int - La ligne où le pion est placé
    @param col : int - La colonne où le pion est placé
    @param player : str - Le joueur courant (symbole représentant le joueur)
    @return new_grid : list[list[str]] - La nouvelle grille après placement du pion
    """
    new_grid = [[grid[r][c] for c in range(5)] for r in range(5)]  # Copie la grille actuelle
    new_grid[row][col] = player  # Place le pion du joueur sur la case spécifiée
    return new_grid

def move_generation_placement(current_grid, current_player):
    """
    Génère les mouvements possibles pour la phase de placement,
    en priorisant les cases proches des pions existants.

    @param current_grid : list[list[str]] - La grille actuelle du jeu
    @param current_player : str - Le symbole représentant le joueur courant
    @return possible_grids : list[list[list[str]]] - Liste des nouvelles grilles générées
    """
    possible_grids = []
    taken_positions = get_taken_positions(current_grid)  # Positions occupées

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Directions adjacentes
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    hot_zones = set()  # Zones chaudes autour des pions existants
    for row, col in taken_positions:
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and current_grid[nr][nc] == teeko_node.empty:  # Case vide adjacente
                hot_zones.add((nr, nc))  # Ajoute la case chaude à la liste

    # Génère les nouvelles grilles à partir des zones chaudes
    for row, col in hot_zones:
        new_grid = generate_new_state(current_grid, row, col, current_player)  # Place le pion
        alignment_score = TeekoGame.count_partial_alignments(current_player, new_grid)  # Calcul du score d'alignement
        possible_grids.append((new_grid, alignment_score))  # Ajoute la grille générée avec son score

    # Trie les grilles par score d'alignement décroissant
    possible_grids.sort(key=lambda x: x[1], reverse=True)
    return [grid for grid, _ in possible_grids]

def get_positions_of_current_player(grid, player):
    """
    Renvoie toutes les positions occupées par les pions du joueur courant.

    @param grid : list[list[str]] - La grille actuelle du jeu
    @param player : str - Le symbole représentant le joueur
    @return positions : list[tuple[int, int]] - Liste des positions des pions du joueur
    """
    positions = []
    for row in range(5):  # Parcourt les lignes
        for col in range(5):  # Parcourt les colonnes
            if grid[row][col] == player:  # Si la case appartient au joueur
                positions.append((row, col))  # Ajoute la position à la liste
    return positions

def generate_adjacent_positions(current_grid, current_player, ligne, colonne):
    """
    Génère de nouvelles grilles pour chaque position adjacente valide autour d'une case donnée.

    @param current_grid : list[list[str]] - La grille actuelle du jeu
    @param current_player : str - Le symbole représentant le joueur courant
    @param ligne : int - La ligne actuelle du pion
    @param colonne : int - La colonne actuelle du pion
    @return possible_grids : list[list[list[str]]] - Liste des nouvelles grilles générées
    """
    possible_grids = []
    directions = [
        (-1, 0), (1, 0),  # Directions adjacentes (haut, bas)
        (0, -1), (0, 1),  # Directions adjacentes (gauche, droite)
        (-1, -1), (-1, 1),  # Directions diagonales
        (1, -1), (1, 1)
    ]

    for d_ligne, d_colonne in directions:
        new_ligne, new_colonne = ligne + d_ligne, colonne + d_colonne
        if 0 <= new_ligne < 5 and 0 <= new_colonne < 5 and current_grid[new_ligne][new_colonne] == teeko_node.empty:
            new_grid = generate_new_state(current_grid, ligne, colonne, current_player)  # Crée la grille avec le pion déplacé
            new_grid[new_ligne][new_colonne] = current_player  # Place le pion sur la nouvelle case
            new_grid[ligne][colonne] = teeko_node.empty  # Libère l'ancienne case
            possible_grids.append(new_grid)  # Ajoute la grille générée à la liste

    return possible_grids

def move_generation_deplacement(current_grid, current_player):
    """
    Génère tous les états possibles pour le déplacement des pions,
    en priorisant les mouvements proches des autres pions et des zones stratégiques.

    @param current_grid : list[list[str]] - La grille actuelle du jeu
    @param current_player : str - Le symbole représentant le joueur courant
    @return possible_grids : list[list[list[str]]] - Liste des nouvelles grilles générées
    """
    possible_grids = []
    player_positions = get_positions_of_current_player(current_grid, current_player)  # Positions des pions du joueur

    hot_zones = set()  # Zones chaudes autour des pions
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    for row, col in player_positions:
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and current_grid[nr][nc] == teeko_node.empty:  # Case vide adjacente
                hot_zones.add((nr, nc))  # Ajoute la case chaude à la liste

    # Génère les nouvelles grilles à partir des positions des pions
    for row, col in player_positions:
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and current_grid[nr][nc] == teeko_node.empty:
                new_grid = generate_new_state(current_grid, row, col, current_player)  # Simule le déplacement
                new_grid[nr][nc] = current_player  # Place le pion à la nouvelle position
                new_grid[row][col] = teeko_node.empty  # Libère l'ancienne position
                score = 1 if (nr, nc) in hot_zones else 0  # Priorise les zones chaudes
                possible_grids.append((new_grid, score))  # Ajoute la grille générée avec son score

    # Trie les grilles par priorité des zones chaudes
    possible_grids.sort(key=lambda x: x[1], reverse=True)
    return [grid for grid, _ in possible_grids]

def count_non_empty_cells(grid):
    """
    Compte le nombre de cases non vides dans la grille.

    @param grid : list[list[str]] - La grille actuelle du jeu
    @return compteur : int - Le nombre de cases non vides
    """
    compteur = 0
    for row in range(5):  # Parcourt les lignes
        for col in range(5):  # Parcourt les colonnes
            if grid[row][col] != teeko_node.empty:  # Si la case est occupée
                compteur += 1  # Incrémente le compteur
    return compteur
