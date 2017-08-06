from tree import Tree
import csv



def read_csv(file_name):
    with open(file_name, 'rb') as f:
    reader = csv.reader(f)
    table = list(reader)
    return table


def get_majority_label(data):
    pass
    

def homogeneous(data):
    pass


def get_attribute_domain(attribute):
    pass
    

def get_data_subsest(best_attribute, value, data):
    pass
    
    

tree = Tree()

def id3(data, attributes, default):
    if not data:
        return default
        
    if homogeneous(data):
        label = data[0][-1] #TODO make sure this works
        return label
        
    
    if not attributes:
        label = get_majority_label(data)
        return label
        
    
    best_attribute = pick_best_attribute(data, attributes)
    
    tree.add_node(best_attribute)
    
    default_label = get_majority_label(data)
    
    domain = get_attribute_domain(best_attribute)
    
    for value in domain:
        tree.nodes[best_attribute].add_edge(value)
        
        subset = get_data_subsest(best_attribute, value, data)
        
        new_attributes = copy.deepcopy(attributes)
        new_attributes.remove(best_attribute)
    
        child = id3(subset, new_attributes, default_label)
        
        tree.add_node(child, best_attribute)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
