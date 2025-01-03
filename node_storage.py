import teeko_node


class Tekko_Node_Storage:
    """
    Classe pour gérer le stockage et la récupération des nœuds (nodes) dans un jeu de Teeko.
    Chaque nœud est associé à un état de jeu et un joueur spécifique.
    """

    def __init__(self):
        """
        Initialise un dictionnaire vide pour stocker les nœuds.
        """
        self.map = {}

    def get_or_create_node(self, state, player):
        """
        Renvoie un nœud en fonction de l'état de jeu et du joueur. Si le nœud n'existe pas encore,
        il le crée, le stocke, et le retourne.

        Paramètres :
            state : list[list[str]] - L'état actuel du jeu (grille ou configuration).
            player : str - Le joueur actuel (par exemple, 'X' ou 'O').

        Retourne :
            teeko_node.Teeko_node - Le nœud correspondant à l'état et au joueur.
        """
        key = (player, str(state))  # Clé unique basée sur le joueur et l'état converti en chaîne
        if key in self.map:
            return self.map[key]  # Retourne le nœud existant si trouvé
        else:
            rtn = teeko_node.Teeko_node(state, player)  # Crée un nouveau nœud
            self.map[key] = rtn  # Stocke le nœud dans le dictionnaire
            return rtn
