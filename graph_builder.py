from grid_utils import move_generation_placement, count_non_empty_cells,move_generation_deplacement
from teeko_logique import TeekoGame
from teeko_node import Teeko_node
import time

def grille_complete(node, storage, depth=0, max_depth=3):
    """
    Génère les enfants d'un nœud avec logs pour le débogage.
    """
    if depth > max_depth:
        return

    storage.get_or_create_node(node.state, node.player)

    # Vérification des conditions de victoire
    if TeekoGame.check_win('X', node.state):
        node.value = -1  # Victoire pour X
        return
    elif TeekoGame.check_win('O', node.state):
        node.value = 1  # Victoire pour O
        return

    # Génération des mouvements
    if count_non_empty_cells(node.state) < 8:
        liste_enfants_grilles = move_generation_placement(node.state, node.player)
    else:
        liste_enfants_grilles = move_generation_deplacement(node.state, node.player)

    # Création des noeuds enfants
    for grille in liste_enfants_grilles:
        noeud_enfant = storage.get_or_create_node(grille, node.player)
        node.add_child(noeud_enfant)
        noeud_enfant.value = noeud_enfant.eval()

    # Tri des enfants
    node.childrens.sort(key=lambda x: x.value, reverse=True)

    # Exploration récursive
    for child in node.childrens:
        grille_complete(child, storage, depth=depth + 1, max_depth=max_depth)

def filter_relevant_moves(possible_moves, player):
    """
    Filtre les mouvements pour inclure uniquement ceux qui contribuent à une victoire
    ou défendent contre une menace imminente.
    """
    filtered_moves = []
    opponent = 'O' if player == 'X' else 'X'

    for move in possible_moves:
        node = Teeko_node(move, player)
        # Vérifie si le mouvement rapproche le joueur d'une victoire
        if TeekoGame.check_win(player, move):
            filtered_moves.append(move)
        # Vérifie si le mouvement empêche l'adversaire de gagner
        elif TeekoGame.check_win(opponent, move):
            filtered_moves.append(move)
        # Privilégie les mouvements qui améliorent les alignements
        elif TeekoGame.count_partial_alignments(player, move) > 0:
            filtered_moves.append(move)

    return filtered_moves


def alphabeta(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.is_winner():
        return node.eval()

    if maximizing_player:
        max_val = float('-inf')
        for child in node.childrens:
            val = alphabeta(child, depth - 1, alpha, beta, False)
            max_val = max(max_val, val)
            alpha = max(alpha, val)
            if beta <= alpha or max_val >= 0.9:  # Élagage si proche de victoire
                break
        return max_val
    else:
        min_val = float('inf')
        for child in node.childrens:
            val = alphabeta(child, depth - 1, alpha, beta, True)
            min_val = min(min_val, val)
            beta = min(beta, val)
            if beta <= alpha or min_val <= -0.9:  # Élagage si proche de défaite
                break
        return min_val


def best_move(node, depth=3, maximizing_player=True):
    """
    Retourne la grille (board) correspondant au meilleur coup
    trouvé par l'algorithme Min-Max avec élagage alpha-bêta.

    :param node: Teeko_node, le nœud actuel.
    :param depth: int, la profondeur de recherche souhaitée.
    :param maximizing_player: bool, True si le joueur courant est le 'maximizing player'.
    :return: list[list[str]] - la grille du meilleur coup.
    """
    start_time = time.time()

    best_val = float('-inf') if maximizing_player else float('inf')
    best_move = None

    for child in node.childrens:
        val = alphabeta(child, depth - 1, float('-inf'), float('inf'), not maximizing_player)
        if maximizing_player and val > best_val:
            best_val = val
            best_move = child.state
        elif not maximizing_player and val < best_val:
            best_val = val
            best_move = child.state

    elapsed_time = time.time() - start_time
    return best_move if best_move else node.state
