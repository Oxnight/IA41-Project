import teeko_node

class Tekko_Node_Storage:

    def __init__(self):
        self.map = {}
    

    def get_node(self, state, player):
        key = str(player) + " " + str(state)
        if key in self.map:
            return self.map[key]
        else :
            rtn = teeko_node.Teeko_node(state,player)
            self.map[key] = rtn
            return rtn
        
    def get_terminal_node(self):
        list = []

        for node in self.map.items():
            if node[1].is_winner():
                list.append(node[1])
        
        return list
    
