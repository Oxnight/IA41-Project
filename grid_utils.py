from teeko_logique import TeekoGame

def get_taken_positions(grid):
    """
    Renvoie toutes les positions déjà occupées sur la grille.

    Paramètres :
        grid : list[list[str]] - La grille actuelle du jeu.

    Retourne :
        taken_positions : list[tuple[int, int]] - Une liste des positions (row, col) occupées.
    """
    taken_positions = []
    for row in range(5):  # Parcourt les lignes de la grille (0 à 4)
        for col in range(5):  # Parcourt les colonnes de la grille (0 à 4)
            if grid[row][col] != ' ':  # Vérifie si la case n'est pas vide
                taken_positions.append((row, col))  # Ajoute la position occupée (ligne, colonne)
    return taken_positions

def generate_new_state(grid, row, col, player):
    """
    Génère une nouvelle grille avec le pion du joueur placé à une position spécifique.

    Paramètres :
        grid : list[list[str]] - La grille actuelle du jeu.
        row : int - La ligne où placer le pion (0 à 4).
        col : int - La colonne où placer le pion (0 à 4).
        player : str - Le symbole représentant le joueur (par exemple 'X' ou 'O').

    Retourne :
        new_grid : list[list[str]] - Une copie indépendante de la grille avec le pion placé.
    """
    new_grid = [[grid[r][c] for c in range(5)] for r in range(5)]  # Crée une copie de la grille
    new_grid[row][col] = player  # Place le pion du joueur sur la position donnée
    return new_grid

def move_generation_placement(current_grid, current_player):
    """
    Génère les mouvements possibles pour la phase de placement,
    en priorisant les cases proches des pions existants.

    Paramètres :
        current_grid : list[list[str]] - La grille actuelle du jeu.
        current_player : str - Le symbole représentant le joueur courant.

    Retourne :
        possible_grids : list[list[list[str]]] - Une liste de nouvelles grilles générées.
    """
    possible_grids = []
    taken_positions = get_taken_positions(current_grid)  # Positions occupées actuelles

    # Directions adjacentes pour rechercher les "zones chaudes"
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    # Identifier les cases adjacentes disponibles (zones chaudes)
    hot_zones = set()
    for row, col in taken_positions:
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and current_grid[nr][nc] == ' ':
                hot_zones.add((nr, nc))

    # Générer de nouveaux états uniquement pour les zones chaudes
    for row, col in hot_zones:
        new_grid = generate_new_state(current_grid, row, col, current_player)
        alignment_score = TeekoGame.count_partial_alignments(current_player, new_grid)  # Calcul du score
        possible_grids.append((new_grid, alignment_score))

    # Trier les grilles par score décroissant
    possible_grids.sort(key=lambda x: x[1], reverse=True)
    return [grid for grid, _ in possible_grids]

def get_positions_of_current_player(grid, player):
    """
    Renvoie toutes les positions occupées par les pions du joueur courant.

    Paramètres :
        grid : list[list[str]] - La grille actuelle du jeu.
        player : str - Le symbole représentant le joueur.

    Retourne :
        positions : list[tuple[int, int]] - Une liste des positions (row, col) occupées par le joueur.
    """
    positions = []
    for row in range(5):
        for col in range(5):
            if grid[row][col] == player:
                positions.append((row, col))  # Ajoute la position (ligne, colonne) du joueur
    return positions

def generate_adjacent_positions(current_grid, current_player, ligne, colonne):
    """
    Génère de nouvelles grilles pour chaque position adjacente valide autour d'une case donnée.

    Paramètres :
        current_grid : list[list[str]] - La grille actuelle du jeu.
        current_player : str - Le symbole représentant le joueur.
        ligne : int - Ligne actuelle du pion.
        colonne : int - Colonne actuelle du pion.

    Retourne :
        possible_grids : list[list[list[str]]] - Une liste des nouvelles grilles possibles.
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
            new_grid = generate_new_state(current_grid, ligne, colonne, current_player)
            new_grid[new_ligne][new_colonne] = current_player  # Place le pion sur la nouvelle case
            new_grid[ligne][colonne] = ' '  # Libère l'ancienne case
            possible_grids.append(new_grid)
    return possible_grids

def move_generation_deplacement(current_grid, current_player):
    """
    Génère tous les états possibles pour le déplacement des pions,
    en priorisant les mouvements proches des autres pions et des zones stratégiques.

    Paramètres :
        current_grid : list[list[str]] - La grille actuelle du jeu.
        current_player : str - Le symbole représentant le joueur courant.

    Retourne :
        possible_grids : list[list[list[str]]] - Une liste des nouvelles grilles générées.
    """
    possible_grids = []
    player_positions = get_positions_of_current_player(current_grid, current_player)

    # Collecte des zones chaudes autour des pions actuels
    hot_zones = set()
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    for row, col in player_positions:
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and current_grid[nr][nc] == ' ':
                hot_zones.add((nr, nc))

    # Générer les nouveaux états à partir des positions des pions actuels
    for row, col in player_positions:
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and current_grid[nr][nc] == ' ':
                # Simuler le déplacement
                new_grid = generate_new_state(current_grid, row, col, current_player)
                new_grid[nr][nc] = current_player  # Place le pion sur la nouvelle case
                new_grid[row][col] = ' '  # Libère l'ancienne position

                # Calculer un score basé sur la proximité des hot zones
                score = 1 if (nr, nc) in hot_zones else 0
                possible_grids.append((new_grid, score))

    # Trier les grilles par priorité (hot zones en premier)
    possible_grids.sort(key=lambda x: x[1], reverse=True)
    return [grid for grid, _ in possible_grids]

def count_non_empty_cells(grid):
    """
    Compte le nombre de cases non vides dans la grille.

    Paramètres :
        grid : list[list[str]] - La grille actuelle du jeu.

    Retourne :
        compteur : int - Le nombre de cases non vides.
    """
    compteur = 0
    for row in range(5):
        for col in range(5):
            if grid[row][col] != ' ':  # Vérifie si la case n'est pas vide
                compteur += 1
    return compteur
