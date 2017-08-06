from tree import Tree
import csv
import pprint
import copy
import random

pp = pprint.PrettyPrinter(indent=4)


def read_csv(file_name):
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        table = list(reader)
    
    return table


def get_attribute_domains(data):
    attributes = {}
    
    for i in range(len(data[0]) - 1):
        i = i + 1           #Skip the first column
        attributes[i] = []
    
    for row in data:
        for i in range(len(row) - 1):
            i = i + 1           #Skip the first column
            attribute_value = row[i]
            if attribute_value not in attributes[i]:
                attributes[i].append(attribute_value)
                
    return attributes


def get_majority_label(data):
    poisonous_count = 0
    edible_count = 0
    
    for row in data:
        if row[0] == 'p':
            poisonous_count += 1
        if row[0] == 'e':
            edible_count += 1
            
    if poisonous_count > edible_count:
        return 'p'
    elif edible_count > poisonous_count:
        return 'e'
    else:
        random_choice = random.randint(0, 1)
        if random_choice == 0:
            return 'p'
        else:
            return 'e'
    

def homogeneous(data):
    label = data[0][0]
    for row in data:
        if row[0] != label:
            return False
    
    return True
    

def get_data_subsest(best_attribute, value, data):
    data_subset = []
    for row in data:
        if row[best_attribute] == value:
            row_copy = copy.deepcopy(row)
            data_subset.append(row_copy)

    return data_subset
    

def train(training_data):
    default_label = get_majority_label(training_data)
    attributes = get_attribute_domains(training_data)
    tree = Tree()
     
    decision_tree = id3(training_data, tree, attributes, default_label)

    return decision_tree
    
    
def pick_best_attribute(data, attributes):
    


def id3(data, attributes, default):
    if not data:
        return default
        
    if homogeneous(data):
        label = data[0][0] #TODO make sure this works
        return label
        
    if not attributes:
        label = get_majority_label(data)
        return label
    
    best_attribute = pick_best_attribute(data, attributes)
    
    tree.add_node(best_attribute)
    
    default_label = get_majority_label(data)
    
    domain = attributes[best_attribute]
    
    for value in domain:
        tree.nodes[best_attribute].add_edge(value)
        
        subset = get_data_subsest(best_attribute, value, data)
        
        new_attributes = copy.deepcopy(attributes)
        new_attributes.pop(best_attribute, None)
    
        child = id3(subset, new_attributes, default_label)
        
        tree.add_node(child, best_attribute)
    
    
    
data = read_csv('agaricus-lepiota.data')
pp.pprint(get_attribute_domains(data) ) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
