from tree import Tree
from node import Node
import csv
import pprint
import copy
import random
import math

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
    

def get_data_subset(best_attribute, value, data):
    data_subset = []
    for row in data:
        if row[best_attribute] == value:
            row_copy = copy.deepcopy(row)
            data_subset.append(row_copy)

    return data_subset
    

def calculate_entropy(data):
    poisonous_count = 0.0
    edible_count = 0.0
    
    for row in data:
        if row[0] == 'p':
            poisonous_count += 1
        if row[0] == 'e':
            edible_count += 1
    
    length_data = len(data)
    p1 = poisonous_count / length_data
    p2 = edible_count / length_data
    entropy = p1 * math.log(p1) + p2 * math.log(p2)
    
    return -entropy


def calculate_information_gain(attribute, data, entropy):
    value_counts = {}
    for row in data:
        value = row[attribute]
        label = row[0]
        
        if value in value_counts:
            value_counts[value]['count'] += 1.0
            value_counts[value][label] += 1.0
        else:
            value_counts[value] = {}
            value_counts[value]['count'] = 1.0
            value_counts[value]['p'] = 0.0
            value_counts[value]['e'] = 0.0
            value_counts[value][label] += 1.0
    
    summation = 0.0
    data_length = len(data)
    
    for value in value_counts:
        count = value_counts[value]['count']
        p = value_counts[value]['p']
        e = value_counts[value]['e']
        
        #if count != 0:
        if p/count == 0.0:
            summation -= (count / data_length) * ( (e/count) * math.log(e/count) )
        elif e/count == 0.0:
            summation -= (count / data_length) * ( (p/count) * math.log(p/count) )
        else:
            summation -= (count / data_length) * ( (p/count) * math.log(p/count) + (e/count) * math.log(e/count) )

    information_gain = entropy - summation
    
    return information_gain
        
    
def pick_best_attribute(data, attributes):
    entropy = calculate_entropy(data)
    max_information_gain = 0.0
    best_attribute = None
    
    for attribute in attributes:
        information_gain = calculate_information_gain(attribute, data, entropy)
        if information_gain > max_information_gain:
            max_information_gain = information_gain
            best_attribute = attribute
            
    return best_attribute
        


def id3(data, tree, attributes, default, parent_node):
    if not data:
        return default
        
    if homogeneous(data):
        label = data[0][0] #TODO make sure this works
        return label
        
    if not attributes:
        label = get_majority_label(data)
        return label
    
    default_label = get_majority_label(data)
    best_attribute = pick_best_attribute(data, attributes)
    domain = attributes[best_attribute]
    
    node = Node(best_attribute)
    tree.add_node(node, parent_node)
        
    for value in domain:
        node.add_edge(value)
        
        subset = get_data_subset(best_attribute, value, data)
        
        new_attributes = copy.deepcopy(attributes)
        new_attributes.pop(best_attribute, None)
    
        child = id3(subset, tree, new_attributes, default_label, node)
        
        node.add_child(child)
        if type(child) != str:
            tree.add_node(child, node)
    
    return node
    
    
def train(training_data):
    default_label = get_majority_label(training_data)
    attributes = get_attribute_domains(training_data)
    decision_tree = Tree()
     
    id3(training_data, decision_tree, attributes, default_label, None)

    return decision_tree
    

    
data = read_csv('agaricus-lepiota.data')
tree = train(data)
nodes = tree.nodes
for node_id in nodes:
    print nodes[node_id]
    for child in nodes[node_id].children:
        print '\t', child
    
    
    
    
    
    
    
    
    
    
    
    
    
