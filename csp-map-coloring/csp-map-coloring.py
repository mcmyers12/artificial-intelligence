#%matplotlib inline

from __future__ import division

import matplotlib.pyplot as plt
import networkx as nx
import copy


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


def initialize_node_info_map(planar_map, colors):
    node_info_map = {}
    for node in planar_map["nodes"]:
        node_info_map[node] = {"colors" : [], "assigned": False}
        node_info_map[node]["colors"] = copy.deepcopy(colors)
    
    return node_info_map
    

def node_assigned(node, assignments):
    for assignment in assignments:
        if assignment[0] == node:
            return True
            
    return False        


def check_complete_assignment(assignments, planar_map):
    for node in planar_map["nodes"]:
        if not node_assigned(node, assignments):
            return False
    
    return True 
 

#Minimum remaining values
def select_unassigned_variable(node_info_map, colors):
    mininimum_remaining = len(colors)
        
    for node, node_info in node_info_map.iteritems():
        colors = node_info["colors"]
        if not node_info["assigned"]:
            num_remaining = len(colors)
            if num_remaining < mininimum_remaining and num_remaining > 0:
                mininimum_remaining = num_remaining
    
    selected_nodes = []
    for node, node_info in node_info_map.iteritems():
        print node, node_info
        colors = node_info["colors"]
        if not node_info["assigned"]:
            if len(colors) == mininimum_remaining:
                selected_nodes.append(node)
    
    selected_nodes.sort() 
    return selected_nodes[0]


def get_num_constraints(variable, planar_map, node_info_map, color):
    node_index = planar_map["nodes"].index(variable)
    
    num_constraints = 0
    for edge in planar_map["edges"]:
        other_node_index = None
        if edge[0] == node_index:
            other_node_index = edge[1]
        
        elif edge[1] == node_index:
            other_node_index = edge[0]   
        
        if other_node_index:   
            other_node = planar_map["nodes"][other_node_index]
            for other_color in node_info_map[other_node]["colors"]:
                if color == other_color:
                    num_constraints += 1
                        
    return num_constraints
            
            
def order_domain_values(variable, node_info_map, planar_map): 
    priority_queue = [] # priority queue of (color, num_constraints)
    for color in node_info_map[variable]["colors"]:   
        num_constraints = get_num_constraints(variable, planar_map, node_info_map, color)
        
        for i in range(len(priority_queue)):
            if num_constraints < priority_queue[i][1]:
                priority_queue.insert(i, (color, num_constraints))
                
        if (color, num_constraints) not in priority_queue:
            priority_queue.append((color, num_constraints))
            
    ordered_colors = [item[0] for item in priority_queue]
    return ordered_colors

    
def get_connected_nodes(variable, planar_map):
    connected_nodes = []
    node_index = planar_map["nodes"].index(variable)
    
    for edge in planar_map["edges"]:
        other_node_index = None
        if edge[0] == node_index:
            other_node_index = edge[1]
        
        elif edge[1] == node_index:
            other_node_index = edge[0] 
        
        if other_node_index:
            connected_node = planar_map["nodes"][other_node_index]
            connected_nodes.append(connected_node)
        
    return connected_nodes
    
    
def check_consistent(variable, color, assignments, planar_map):
    connected_nodes = get_connected_nodes(variable, planar_map)
    
    for item in assignments:
        if item[0] in connected_nodes:
            if item[1] == color:
                return False
    
    return True


#Return false if after forward check, there are would be no values left for the variable
def determine_forward_check_success(variable, color, node_info_map, planar_map):        
    connected_nodes = get_connected_nodes(variable, planar_map)
    
    for node in connected_nodes:
        node_colors_copy = copy.deepcopy(node_info_map[node]["colors"])
        node_colors_copy.remove(color)
        if not node_colors_copy:
            return False
            
    return True
    
    
#For each unassigned variable Y that is connected to X, delete from Y the color assigned to X
def forward_check(variable, color, node_info_map, planar_map):
    connected_nodes = get_connected_nodes(variable, planar_map)
    
    for node in connected_nodes:
        node_info_map[node]["colors"].remove(color)
        

def remove_forward_check(variable, color, node_info_map, planar_map):
    connected_nodes = get_connected_nodes(variable, planar_map)
    
    for node in connected_nodes:
        node_info_map[node]["colors"].append(color)
                

def backtracking_search(planar_map, colors, trace):
    return backtrack([], planar_map, colors, trace)
    

def backtrack(assignments, planar_map, colors, trace):
    if trace:
        print "Beginning backtracking"
    
    node_info_map = initialize_node_info_map(planar_map, colors)
    
    if check_complete_assignment(assignments, planar_map): #All nodes are assigned colors?
        return assignments
        
    node = select_unassigned_variable(node_info_map, colors) #Minimum remaining values - choose variable with fewest values left
    
    values = order_domain_values(node, node_info_map, planar_map) #Least constraining value
    for color in values:  
        if check_consistent(node, color, assignments, planar_map): #value is consitent with assignment
            assignments.append((node, color)) #add {variable = value} to assignment
            
            print "\nAdded"
            print assignments
            
            node_info_map[node]["assigned"] = True;
            
            forward_check_success = determine_forward_check_success(node, color, node_info_map, planar_map)
            
            if forward_check_success:
                forward_check(node, color, node_info_map, planar_map)
                
                result = backtrack(assignments, planar_map)
                if result:
                    return result
        #remove {var = value} and inferences from assignments
        assignments.pop(-1) #removes the last added value
        
        print "\nRemoved"
        print assignments
        remove_forward_check(node, color, node_info_map, planar_map)
        
    return False 
        

def color_map(planar_map, colors, trace=False):
    backtracking_search(planar_map, colors, trace)



connecticut_colors = color_map( connecticut, ["red", "blue", "green", "yellow"], trace=True)   




#TODO check for any deep copy issues



