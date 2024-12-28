import node_storage


def test_node_storage():
    storage = node_storage.Tekko_Node_Storage() ##Toujour initialiser le storage avant le début

    ## Test get quand la node n'existe pas
    state = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]] ## State peut change
    player = 1

    node = storage.get_node(state,player) ## Pour récuperer une node et ici on l'initialise

    print(node.state)
    print(node.player)


    ## Test get_node quand la node existe et que ce soit bien une référence
    node_bis = storage.get_node(state,player)
    state[0][0] = 1
    node_bis.set_state = state ## aprs ça la clé est plus bonne

    print(node.state)
    print(node.player)

    ## Test ajout d'un child

    state = [[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,0]]
    player = 2

    node.add_child(storage.get_node(state,player)) ## On ajoute un enfant à la node toujours comme ça ou en l'ayant réupérer avant dans une variable

    print(node.childrens[0].state)
    print(node.childrens[0].player)

    ## Test si on retrouve bien le child dans le storage et si son parent est bien la node

    node_child = storage.get_node(state,player)

    print(node_child.fathers[0].state)
    print(node_child.fathers[0].player)


    ## Test de modification du parent

    node.player = 2

    print(node_child.fathers[0].state)
    print(node_child.fathers[0].player)

    ## Test de get_terminal_node

    list = storage.get_terminal_node()

    print("Liste des nodes terminales")
    for node_t in list:
        print(node_t.state)
        print(node_t.player)
    ## Retourne tout car is_winner retourne True quoi qu'il arrive

    ## Test de du trie des enfants

    state = state = [[1,1,1,0,1],[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,0]]
    player = 1

    node_3 = storage.get_node(state,player) ## Cas plus réel d'ajout d'un enfant
    node.add_child(node_3)
    node_3.set_value(-3)

    state = [[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,1],[1,1,1,0,0],[1,1,1,0,0]]
    player = 1

    node_4 = storage.get_node(state,player)
    node.add_child(node_4)
    node_4.set_value(6)


    print ("Valeur des enfants avant le trie")
    for child in node.childrens:
        print(child.value)

    node.sort_childrens()

    print ("Valeur des enfants après le trie")
    for child in node.childrens:
        print(child.value)


def main():
    test_node_storage()

if __name__ == "__main__":
    main()