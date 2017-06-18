
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


europe = {
    "nodes":  ["Iceland", "Ireland", "United Kingdom", "Portugal", "Spain",
                 "France", "Belgium", "Netherlands", "Luxembourg", "Germany",
                 "Denmark", "Norway", "Sweden", "Finland", "Estonia",
                 "Latvia", "Lithuania", "Poland", "Czech Republic", "Austria",
                 "Liechtenstein", "Switzerland", "Italy", "Malta", "Greece",
                 "Albania", "Macedonia", "Kosovo", "Montenegro", "Bosnia Herzegovina",
                 "Serbia", "Croatia", "Slovenia", "Hungary", "Slovakia",
                 "Belarus", "Ukraine", "Moldova", "Romania", "Bulgaria",
                 "Cyprus", "Turkey", "Georgia", "Armenia", "Azerbaijan",
                 "Russia" ], 
    "edges": [(0,1), (0,2), (1,2), (2,5), (2,6), (2,7), (2,11), (3,4),
                 (4,5), (4,22), (5,6), (5,8), (5,9), (5,21), (5,22),(6,7),
                 (6,8), (6,9), (7,9), (8,9), (9,10), (9,12), (9,17), (9,18),
                 (9,19), (9,21), (10,11), (10,12), (10,17), (11,12), (11,13), (11,45), 
                 (12,13), (12,14), (12,15), (12,17), (13,14), (13,45), (14,15),
                 (14,45), (15,16), (15,35), (15,45), (16,17), (16,35), (17,18),
                 (17,34), (17,35), (17,36), (18,19), (18,34), (19,20), (19,21), 
                 (19,22), (19,32), (19,33), (19,34), (20,21), (21,22), (22,23),
                 (22,24), (22,25), (22,28), (22,29), (22,31), (22,32), (24,25),
                 (24,26), (24,39), (24,40), (24,41), (25,26), (25,27), (25,28),
                 (26,27), (26,30), (26,39), (27,28), (27,30), (28,29), (28,30),
                 (29,30), (29,31), (30,31), (30,33), (30,38), (30,39), (31,32),
                 (31,33), (32,33), (33,34), (33,36), (33,38), (34,36), (35,36),
                 (35,45), (36,37), (36,38), (36,45), (37,38), (38,39), (39,41),
                 (40,41), (41,42), (41,43), (41,44), (42,43), (42,44), (42,45),
                 (43,44), (44,45)],
    "coordinates": [( 18,147), ( 48, 83), ( 64, 90), ( 47, 28), ( 63, 34),
                   ( 78, 55), ( 82, 74), ( 84, 80), ( 82, 69), (100, 78),
                   ( 94, 97), (110,162), (116,144), (143,149), (140,111),
                   (137,102), (136, 95), (122, 78), (110, 67), (112, 60),
                   ( 98, 59), ( 93, 55), (102, 35), (108, 14), (130, 22),
                   (125, 32), (128, 37), (127, 40), (122, 42), (118, 47),
                   (127, 48), (116, 53), (111, 54), (122, 57), (124, 65),
                   (146, 87), (158, 65), (148, 57), (138, 54), (137, 41),
                   (160, 13), (168, 29), (189, 39), (194, 32), (202, 33),
                   (191,118)]}


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


def check_complete_assignment(assignments, planar_map, trace):
    if trace:
        print 'Checking for a complete assignment'
    for node in planar_map["nodes"]:
        if not node_assigned(node, assignments):
            if trace:
                print '\tAssignment not complete, continuing algorithm\n'
            return False
    
    if trace:
        print '\tAssignment is complete\n'
    return True 
 

#Minimum remaining values
def select_unassigned_variable(node_info_map, colors, trace):
    if trace:
        print 'Selecting an unassigned variable using minimum remaining values, ties broken in ascending order'

    mininimum_remaining = len(colors)
        
    for node, node_info in node_info_map.iteritems():
        colors = node_info["colors"]
        if not node_info["assigned"]:
            num_remaining = len(colors)
            if num_remaining < mininimum_remaining and num_remaining > 0:
                mininimum_remaining = num_remaining
    
    selected_nodes = []
    for node, node_info in node_info_map.iteritems():
        colors = node_info["colors"]
        if not node_info["assigned"]:
            if len(colors) == mininimum_remaining:
                selected_nodes.append(node)
    
    if selected_nodes:
        selected_nodes.sort()
        
        if trace:
            print '\tLeast value node found with minimum remaining values: ', selected_nodes[0], '\n'
        return selected_nodes[0]
    
    return None


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
            
            
def order_domain_values(variable, node_info_map, planar_map, trace): 
    if trace:
        print 'Ordering domain values using Least Constraining Value'
    
    priority_queue = [] # priority queue of (color, num_constraints)
    for color in node_info_map[variable]["colors"]:   
        num_constraints = get_num_constraints(variable, planar_map, node_info_map, color)
        
        for i in range(len(priority_queue)):
            if num_constraints < priority_queue[i][1]:
                priority_queue.insert(i, (color, num_constraints))
                
        if (color, num_constraints) not in priority_queue:
            priority_queue.append((color, num_constraints))
            
    ordered_colors = [item[0] for item in priority_queue]
    
    if trace:
        print '\tOrdered domain values:', ordered_colors, '\n'    
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
    
    
def check_consistent(variable, color, assignments, planar_map, trace):
    if trace:
        print 'Checking whether variable', variable, ' and value', color, 'are consistent with assignment'

    connected_nodes = get_connected_nodes(variable, planar_map)
    
    for item in assignments:
        if item[0] in connected_nodes:
            if item[1] == color:
                if trace:
                    print '\tNot consistent\n'
                return False
    if trace:
        print '\tConsistent\n'
    return True


#Return false if after forward check, there are would be no values left for the variable
def determine_forward_check_success(variable, color, node_info_map, planar_map):        
    connected_nodes = get_connected_nodes(variable, planar_map)
    
    for node in connected_nodes:
        node_colors_copy = copy.deepcopy(node_info_map[node]["colors"])

        if color in node_colors_copy:
            node_colors_copy.remove(color)

        if not node_colors_copy:
            return False
            
    return True
    
    
#For each unassigned variable Y that is connected to X, delete from Y the color assigned to X
def forward_check(variable, color, node_info_map, planar_map, trace):
    if trace:
        print 'Forward checking for variable', variable
    
    connected_nodes = get_connected_nodes(variable, planar_map)
    
    for node in connected_nodes:
        if color in node_info_map[node]["colors"]:
            if trace:
                print '\tRemoving value', color, 'from variable', node
                
            node_info_map[node]["colors"].remove(color)
            
    if trace:
        print
        

def remove_forward_check(variable, color, node_info_map, planar_map):
    connected_nodes = get_connected_nodes(variable, planar_map)
    
    for node in connected_nodes:
        if color not in node_info_map[node]["colors"]:
            node_info_map[node]["colors"].append(color)


#Put the assignments in the same order as the order of "nodes" in the planar_map
def order_assignments(assignments, planar_map):
    nodes = planar_map["nodes"]
    
    ordered_assignments = []
    
    for node in nodes:
        for tuple in assignments:
            if tuple[0] == node:
                ordered_assignments.append(tuple)
    
    return ordered_assignments
    
    
def remove_assignments_and_forward_checks(assignments, node, color, node_info_map, planar_map, trace):
    if trace:
        'Removing assignment and forward checking for variable', node, 'and value ', color, '\n'
 
    if assignments:
        unassigned_node = assignments.pop(-1) #removes the last added value
        node_info_map[unassigned_node[0]]["assigned"] = False
    
    remove_forward_check(node, color, node_info_map, planar_map)
                

def backtracking_search(planar_map, colors, trace):
    if trace:
        print '\n\nExecuting search\n'
        
    node_info_map = initialize_node_info_map(planar_map, colors)
    return backtrack([], planar_map, colors, trace, node_info_map)
    

def backtrack(assignments, planar_map, colors, trace, node_info_map):
    if check_complete_assignment(assignments, planar_map, trace): #All nodes are assigned colors?
        return order_assignments(assignments, planar_map)
        
    node = select_unassigned_variable(node_info_map, colors, trace) #Minimum remaining values - choose variable with fewest values left
    if not node: 
        return None #returns None if no coloring can be found???'''
            
    values = order_domain_values(node, node_info_map, planar_map, trace) #Least constraining value
    for color in values:  
        if check_consistent(node, color, assignments, planar_map, trace): #value is consitent with assignment
            if ((node, color)) not in assignments:
                assignments.append((node, color)) #add {variable = value} to assignment

            node_info_map[node]["assigned"] = True;
            
            forward_check_success = determine_forward_check_success(node, color, node_info_map, planar_map)
            if forward_check_success:
                forward_check(node, color, node_info_map, planar_map, trace)
                
                result = backtrack(assignments, planar_map, colors, trace, node_info_map)
                if result:
                    return result
        
        if trace:
            print 'Forward checking not successful, backtracking\n'
        remove_assignments_and_forward_checks(assignments, node, color, node_info_map, planar_map, trace)
        
    return None 
    
        

def color_map(planar_map, colors, trace=False):
    assignments = backtracking_search(planar_map, colors, trace)
    return assignments



connecticut_colors = color_map(connecticut, ["red", "blue", "green", "yellow"], trace=True)

print '\n\n\nconnecticut colors', connecticut_colors

edges = connecticut["edges"]
nodes = connecticut["nodes"]
colors = connecticut_colors
COLOR = 1

for start, end in edges:
    try:
        assert colors[start][COLOR] != colors[end][COLOR]
    except AssertionError:
        print "%s and %s are adjacent but have the same color.\n\n" % (nodes[ start], nodes[ end])
        

europe_colors = color_map( europe, ["red", "blue", "green", "yellow"], trace=True)

print '\n\n\neurope_colors', europe_colors


edges = europe["edges"]
nodes = europe[ "nodes"]
colors = europe_colors
COLOR = 1

for start, end in edges:
    try:
        assert colors[ start][COLOR] != colors[ end][COLOR]
    except AssertionError:
        print "%s and %s are adjacent but have the same color." % (nodes[ start], nodes[ end])
        
        

