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


    def add_child(self, identifier):
        self.children.append(identifier)
        
    
    def add_edge(self, edge_label):
        self.edges.append(edge_label)