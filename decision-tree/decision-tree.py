import csv
import copy
import random
import math


attribute_names = {
    1: 'cap-shape',                
    2: 'cap-surface',              
    3: 'cap-color',                
    4: 'bruises?',                
    5: 'odor',                 
    6: 'gill-attachment',          
    7: 'gill-spacing',         
    8: 'gill-size',            
    9: 'gill-color',               
    10: 'stalk-shape',              
    11: 'stalk-root',             
    12: 'stalk-surface-above-ring', 
    13: 'stalk-surface-below-ring',
    14: 'stalk-color-above-ring',   
    15: 'stalk-color-below-ring',  
    16: 'veil-type',                
    17: 'veil-color',               
    18: 'ring-number',              
    19: 'ring-type',             
    20: 'spore-print-color',        
    21: 'population',         
    22: 'habitat'

}


def read_csv(file_name):
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        table = list(reader)
    
    return table


def create_train_test_sets(data):
    random.shuffle(data)
    split_point = len(data) / 2
    test_set = data[:split_point]
    train_set = data[split_point:]
    
    return train_set, test_set
    

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


def id3(data, attributes, default):
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
    
    tree = { best_attribute: {} }
        
    for value in domain:        
        subset = get_data_subset(best_attribute, value, data)
        
        new_attributes = copy.deepcopy(attributes)
        new_attributes.pop(best_attribute, None)
    
        subtree = id3(subset, new_attributes, default_label)
        tree[best_attribute][value] = subtree
    
    return tree
    
    
def train(training_data):
    default_label = get_majority_label(training_data)
    attributes = get_attribute_domains(training_data)
     
    decision_tree = id3(training_data, attributes, default_label)

    return decision_tree


def pretty_print_tree(tree, indent=0):
    for key, value in tree.iteritems():
        if type(key) == int:
            key = attribute_names[key]
        print '    ' * indent + str(key)
        if isinstance(value, dict):
            pretty_print_tree(value, indent+1)
        else:
            print '    ' * (indent+1) + str(value)    


def view(tree):
    pretty_print_tree(tree)


def classify_instance(tree, instance):
    root = next(iter(tree))
    instance_value = instance[root]
    
    while type(tree) == dict:
        tree = tree[root][instance_value]
        
        if type(tree) == dict:
            root = next(iter(tree))
            instance_value = instance[root]
            
    return tree


def classify(tree, test_data):
    classifications = []
    for row in test_data:
        classification = classify_instance(tree, row)
        classifications.append(classification)
    
    return classifications    
    

def evaluate(test_data, classifications):
    errors = 0.0
    for i in range(len(test_data)):
        if classifications[i] != test_data[i][0]:
            errors += 1
            
    error_rate = errors / len(test_data)
    return error_rate


data = read_csv('agaricus-lepiota.data')
set1, set2 = create_train_test_sets(data)

tree = train(set1)
view(tree)
classifications = classify(tree, set2)
error_rate = evaluate(set2, classifications)
print error_rate
print
print
print


tree = train(set2)
view(tree)
classifications = classify(tree, set1)
error_rate = evaluate(set1, classifications)
print error_rate




    
    
    
    
    
    
    
    
    
    
    
    
