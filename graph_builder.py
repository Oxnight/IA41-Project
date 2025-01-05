from grid_utils import move_generation_placement, count_non_empty_cells, move_generation_deplacement
from teeko_logique import TeekoGame
from teeko_node import Teeko_node
import time

def grille_complete(node, storage, depth=0, max_depth=3):
    """
    Gère la génération des enfants d'un nœud dans un arbre de jeu.

    @param node: Teeko_node - Le nœud actuel à étudier.
    @param storage: objet - Gestionnaire des nœuds pour éviter les duplications.
    @param depth: int - Profondeur actuelle de la récursion.
    @param max_depth: int - Profondeur maximale de recherche dans l'arbre.
    @return: None
    """
    # Arrête la récursion si la profondeur maximale est atteinte
    if depth > max_depth:
        return

    # Crée ou récupère le nœud correspondant à l'état actuel
    storage.get_or_create_node(node.state, node.player)

    # Vérifie les conditions de victoire
    if TeekoGame.check_win('X', node.state):
        node.value = -1  # Victoire pour X
        return
    elif TeekoGame.check_win('O', node.state):
        node.value = 1  # Victoire pour O
        return

    # Génère les mouvements en fonction du nombre de cellules remplies
    if count_non_empty_cells(node.state) < 8:
        liste_enfants_grilles = move_generation_placement(node.state, node.player)
    else:
        liste_enfants_grilles = move_generation_deplacement(node.state, node.player)

    # Crée des nœuds enfants pour chaque mouvement possible
    for grille in liste_enfants_grilles:
        noeud_enfant = storage.get_or_create_node(grille, node.player)
        node.add_child(noeud_enfant)
        noeud_enfant.value = noeud_enfant.eval()

    # Trie les enfants par valeur, en ordre décroissant
    node.childrens.sort(key=lambda x: x.value, reverse=True)

    # Explore récursivement les enfants
    for child in node.childrens:
        grille_complete(child, storage, depth=depth + 1, max_depth=max_depth)

def filter_relevant_moves(possible_moves, player):
    """
    Filtre les mouvements possibles pour inclure ceux qui maximisent les chances de victoire ou minimisent les risques.

    @param possible_moves: list - Liste des grilles (mouvements possibles).
    @param player: str - Joueur courant ('X' ou 'O').
    @return: list - Liste des mouvements filtrés.
    """
    # Initialise une liste pour stocker les mouvements pertinents
    filtered_moves = []
    opponent = 'O' if player == 'X' else 'X'

    # Analyse chaque mouvement possible
    for move in possible_moves:
        node = Teeko_node(move, player)
        # Ajoute le mouvement s'il mène à une victoire pour le joueur
        if TeekoGame.check_win(player, move):
            filtered_moves.append(move)
        # Ajoute le mouvement s'il bloque une victoire de l'adversaire
        elif TeekoGame.check_win(opponent, move):
            filtered_moves.append(move)
        # Ajoute le mouvement s'il améliore les alignements partiels
        elif TeekoGame.count_partial_alignments(player, move) > 0:
            filtered_moves.append(move)

    return filtered_moves

def alphabeta(node, depth, alpha, beta, maximizing_player):
    """
    Implémente l'algorithme Alpha-Bêta pour évaluer les nœuds d'un arbre de jeu.

    @param node: Teeko_node - Le nœud à évaluer.
    @param depth: int - Profondeur restante à explorer.
    @param alpha: float - Meilleure valeur possible pour le joueur max.
    @param beta: float - Meilleure valeur possible pour le joueur min.
    @param maximizing_player: bool - Indique si le joueur courant maximise (True) ou minimise (False).
    @return: float - Valeur évaluée pour le nœud courant.
    """
    # Si la profondeur est nulle ou si le nœud est un état gagnant, évalue directement
    if depth == 0 or node.is_winner():
        return node.eval()

    if maximizing_player:
        # Initialise la valeur maximale
        max_val = float('-inf')
        for child in node.childrens:
            # Évalue le nœud enfant
            val = alphabeta(child, depth - 1, alpha, beta, False)
            max_val = max(max_val, val)
            alpha = max(alpha, val)
            # Interrompt la recherche si élagage possible
            if beta <= alpha or max_val >= 0.9:
                break
        return max_val
    else:
        # Initialise la valeur minimale
        min_val = float('inf')
        for child in node.childrens:
            # Évalue le nœud enfant
            val = alphabeta(child, depth - 1, alpha, beta, True)
            min_val = min(min_val, val)
            beta = min(beta, val)
            # Interrompt la recherche si élagage possible
            if beta <= alpha or min_val <= -0.9:
                break
        return min_val

def best_move(node, depth=3, maximizing_player=True):
    """
    Trouve le meilleur mouvement à partir de l'état actuel.

    @param node: Teeko_node - Le nœud représentant l'état actuel.
    @param depth: int - Profondeur de recherche de l'algorithme Alpha-Bêta.
    @param maximizing_player: bool - Indique si le joueur courant maximise ou minimise.
    @return: list[list[str]] - La grille correspondant au meilleur coup.
    """
    # Enregistre le temps de départ
    start_time = time.time()

    # Initialise les variables pour le meilleur coup
    best_val = float('-inf') if maximizing_player else float('inf')
    best_move = None

    # Parcourt les enfants du nœud pour trouver le meilleur coup
    for child in node.childrens:
        val = alphabeta(child, depth - 1, float('-inf'), float('inf'), not maximizing_player)
        if maximizing_player and val > best_val:
            best_val = val
            best_move = child.state
        elif not maximizing_player and val < best_val:
            best_val = val
            best_move = child.state

    # Calcul le temps écoulé
    elapsed_time = time.time() - start_time
    return best_move if best_move else node.state
