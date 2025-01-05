import teeko_node

class Tekko_Node_Storage:
    """
    Classe pour gérer le stockage et la récupération des nœuds (nodes) dans un jeu de Teeko.
    Chaque nœud est associé à un état de jeu et un joueur spécifique.
    """

    def __init__(self):
        """
        Initialise un dictionnaire vide pour stocker les nœuds.
        Ce dictionnaire sera utilisé pour enregistrer les états de jeu et les joueurs associés.
        """
        self.map = {}

    def get_or_create_node(self, state, player):
        """
        Renvoie un nœud en fonction de l'état de jeu et du joueur. Si le nœud n'existe pas encore,
        il le crée, le stocke, et le retourne.

        Paramètres :
            state : list[list[str]] - L'état actuel du jeu (grille ou configuration) sous forme de liste de listes.
            player : str - Le joueur actuel, représenté par un caractère comme 'X' ou 'O'.

        Retourne :
            teeko_node.Teeko_node - Le nœud correspondant à l'état et au joueur.

        La fonction crée une clé unique en combinant le joueur et l'état de la grille sous forme de chaîne de caractères.
        Si le nœud avec cette clé existe déjà, il est retourné depuis le dictionnaire de stockage.
        Sinon, un nouveau nœud est créé, stocké, et retourné.
        """
        key = (player, str(state))  # Crée une clé unique basée sur le joueur et l'état converti en chaîne
        if key in self.map:
            return self.map[key]  # Si le nœud existe déjà, on le retourne depuis le dictionnaire
        else:
            rtn = teeko_node.Teeko_node(state, player)  # Crée un nouveau nœud avec l'état et le joueur
            self.map[key] = rtn  # Enregistre le nouveau nœud dans le dictionnaire
            return rtn  # Retourne le nœud nouvellement créé
