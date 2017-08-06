'''class Node:
    def __init__(self, label):
        self.label = label
        self.children = []
        
    def add_child(self, child'''
    
class Node:
    def __init__(self, node_label):
        self.node_label = node_label
        self.children = []
        self.edges = []
        self.id = id(self)


    def add_child(self, node):
        self.children.append(node)
        
    
    def add_edge(self, edge_label):
        self.edges.append(edge_label)
        
    
    def __str__(self):
        print_string = ''
        print_string += 'label: ' + str(self.node_label) +'\n\n'
        print_string += 'children: ' + str(self.children) +'\n\n'
        print_string += 'edges: ' + str(self.edges) +'\n\n'
        print_string += 'id: ' + str(self.id) +'\n\n'
        
        return print_string