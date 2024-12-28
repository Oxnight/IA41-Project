# Description: Classe pour les noeuds de l'arbre de recherche

player_1 = 1
player_2 = 2
empty = 0

non_eval = -2


class Teeko_node:
    def __init__(self):
        self.state = [[empty for i in range(5)] for j in range(5)] ## pourat être emplacer par une class si jamais
        self.player = player_1 ## 1 pour le joueur 1 et 2 pour le joueur 2
        self.childrens = [] ## liste des enfants
        self.fathers = [] ## liste des parents
        self.value = non_eval ## valeur de la node v -1 si non évalué

    def __init__(self, state, player): ## overloading si on connait déjà l'état et le joueur
        self.state = state
        self.player = player
        self.childrens = []
        self.fathers = []
        self.value = non_eval

    def add_child(self, child): ## Ajoute un enfant à la node et met la node comme parent de l'enfant
        self.childrens.append(child)
        child.fathers.append(self)
    
    def is_winner(self):

        ## A faire avec une fonction pour savoir

        is_winner = True

        return (is_winner, self.player)

    def eval(self): ## Retour un tuple (bool, value) si la node est évalué ou non avec bool = True si évalué, False sinon
        ## A faire avec une fonction pour savoir

        if self.is_winner()[0]:
            self.value = 1
        else:
             ## A completer
        
            if self.value == -1: ## Si la node n'est pas évalué
                return (False, self.value)
            else:
                return (True, self.value)
    
    def sort_childrens(self): ## Trie les enfants de la node en fonction de leur valeur par ordre décroissant
        self.childrens = sorted(self.childrens, key=lambda x: x.value, reverse=True)

    ## A partir d'ici que des fonction de control qui doivent être utiliser dans de rares cas
    ## Donc faites plutot des foction si vpous avez besoin de faire des choses similaires
    
    def get_state(self):
        return self.state
    
    def get_player(self):
        return self.player
    
    def get_childrens(self):
        return self.childrens
    
    def get_fathers(self):
        return self.fathers
    
    def get_value(self):
        return self.value
    
    def set_state(self, state):
        self.state = state

    def set_player(self, player): 
        self.player = player

    def set_childrens(self, childrens):
        self.childrens = childrens

    def set_fathers(self, fathers):
        self.fathers = fathers

    def set_value(self, value):
        self.value = value  