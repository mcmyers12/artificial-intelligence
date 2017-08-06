from node import Node


class Tree:

    def __init__(self):
        self.nodes = {}


    def add_node(self, identifier, parent=None):
        node = Node(identifier)
        self.nodes[identifier] = node

        if parent is not None:
            self.nodes[parent].add_child(identifier)

        return node


    def traverse(self, identifier, mode=_DEPTH):
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
                queue = queue[1:] + expansion  # width-first


        
        
        