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
        Chaque clé du dictionnaire est une combinaison unique de l'état de jeu et du joueur,
        permettant un accès rapide aux nœuds correspondants.
        """
        self.map = {}  # Dictionnaire pour stocker les nœuds, avec une clé basée sur l'état et le joueur.

    def get_or_create_node(self, state, player):
        """
        Renvoie un nœud en fonction de l'état de jeu et du joueur. Si le nœud n'existe pas encore,
        il le crée, le stocke, et le retourne.

        @param state: list[list[str]], l'état actuel du jeu sous forme de grille (5x5).
                      Chaque cellule contient 'X', 'O', ou un espace vide (' ').
        @param player: str, le joueur actuel ('X' ou 'O').

        @return: teeko_node.Teeko_node, le nœud correspondant à l'état et au joueur.
        
        La méthode crée une clé unique basée sur le joueur et l'état de la grille sous forme
        de chaîne de caractères. Si le nœud avec cette clé existe déjà dans le dictionnaire,
        il est retourné depuis le stockage. Sinon, un nouveau nœud est créé, stocké, et retourné.
        """
        key = (player, str(state))  # Crée une clé unique basée sur le joueur et l'état converti en chaîne
        
        # Vérification si le nœud existe déjà dans le dictionnaire
        if key in self.map:
            return self.map[key]  # Si le nœud existe déjà, on le retourne depuis le dictionnaire
        else:
            # Si le nœud n'existe pas, on crée un nouveau nœud avec l'état et le joueur donnés
            rtn = teeko_node.Teeko_node(state, player)
            self.map[key] = rtn  # Enregistre le nouveau nœud dans le dictionnaire avec sa clé unique
            return rtn  # Retourne le nœud nouvellement créé
