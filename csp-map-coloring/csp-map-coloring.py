%matplotlib inline

from __future__ import division

import matplotlib.pyplot as plt
import networkx as nx


def draw_map(planar_map, size, color_assignments=None):
    def as_dictionary(a_list):
        dct = {}
        for i, e in enumerate(a_list):
            dct[i] = e
        return dct
    
    G = nx.Graph()
    
    labels = as_dictionary(planar_map[ "nodes"])
    pos = as_dictionary(planar_map["coordinates"])
    
    # create a List of Nodes as indices to match the "edges" entry.
    nodes = [n for n in range(0, len(planar_map[ "nodes"]))]

    if color_assignments:
        colors = [c for n, c in color_assignments]
    else:
        colors = ['red' for c in range(0,len(planar_map[ "nodes"]))]

    G.add_nodes_from( nodes)
    G.add_edges_from( planar_map[ "edges"])

    plt.figure( figsize=size, dpi=600)

    nx.draw( G, node_color = colors, with_labels = True, labels = labels, pos = pos)

#the planar_map
connecticut = { "nodes": ["Fairfield", "Litchfield", "New Haven", "Hartford", "Middlesex", "Tolland", "New London", "Windham"],
                "edges": [(0,1), (0,2), (1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (3,6), (4,6), (5,6), (5,7), (6,7)],
                "coordinates": [( 46, 52), ( 65,142), (104, 77), (123,142), (147, 85), (162,140), (197, 94), (217,146)]}


def initialize_node_color_map(planar_map, colors):
    color_map = {}
    for node in planar_map["nodes"]:
        csp_graph[node] = colors
    
    return color_map
    

#Minimum remaining values
def select_unassigned_variable(color_map, colors):
    mininimum_remaining = len(colors)
    for node, colors in color_map:
        num_remaining = len(colors)
        if num_remaining < mininimum_remaining and num_remaining > 0:
            mininimum_remaining = num_remaining
    
    selected_nodes = []
    for node, colors in color_map:
        if len(colors) == mininimum_remaining
            selected_nodes.append(node)
        
    return selected_nodes.sort()[0]

def node_assigned(node, assignments):
    for assignment in assignments:
        if assignment[0] == node:
            return True
            
    return False        

def check_complete_assignment(assignments):
    for node in planar_map["nodes"]:
        if not node_assigned(node, assignments):
            return False
    
    return True      



def backtracking_search(planar_map):
    return backtrack({}, planar_map)
    

def backtrack(assignment, planar_map, colors)
    if check_complete(assignment) #All nodes are assigned colors?
        return assignment
        
    variable = select_unassigned_variable(planar_map) #Minimum remaining values - choose variable with fewest values left
    
    for value in order_domain_values(variable, assignment, planar_map)  #Least constraining value
        if #value is consitent with assignment
            #add {variable = value} to assignment
            
            forward_check_success = determine_forward_check()
            
            if forward_check_success:
                forward_check()
                
                result = backtrack(assignment, planar_map)
                if result
                    return result
        remove {var = value} and inferences from assignment
        
    return False 
        


#Return false if after forward check, there are would be no values left for the variable
def determine_forward_check():        
    pass
    
#For each unassigned variable Y that is connected to X, delete from Y the color assigned to X
def forward_check():
    pass








