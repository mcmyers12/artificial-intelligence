from node import Node


class Tree:

    def __init__(self):
        self.nodes = {}


    def add_node(self, node, parent=None):        
        node_identifier = node.id
        
        self.nodes[node_identifier] = node

        if parent is not None:
            parent_identifier = parent.id
            self.nodes[parent_identifier].add_child(node)



    '''def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett, 
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self.nodes[identifier].children
        while queue:
            yield queue[0]
            expansion = self.nodes[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first'''


        
        
        