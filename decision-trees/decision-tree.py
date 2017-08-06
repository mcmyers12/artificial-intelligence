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


def create_decision_tree(data, attributes, target_attr, fitness_func):
    """
    Returns a new decision tree based on the examples given.
    """
    data    = data[:]
    vals    = [record[target_attr] for record in data]
    default = majority_value(data, target_attr)

    # If the dataset is empty or the attributes list is empty, return the
    # default value. When checking the attributes list for emptiness, we
    # need to subtract 1 to account for the target attribute.
    if not data or (len(attributes) - 1) <= 0:
        return default
    # If all the records in the dataset have the same classification,
    # return that classification.
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        # Choose the next best attribute to best classify our data
        best = choose_attribute(data, attributes, target_attr, fitness_func)

        # Create a new decision tree/node with the best attribute and an empty
        # dictionary object--we'll fill that up next.
        tree = {best:{}}

        # Create a new decision tree/sub-node for each of the values in the
        # best attribute field
        for val in get_values(data, best):
            # Create a subtree for the current value under the "best" field
            subset = get_examples(data, best, val)
            new_attributes = [attr for attr in attributes if attr != best]
            subtree = create_decision_tree(subset, new_attributes, target_attr, fitness_func)


            # Add the new subtree to the empty dictionary object in our new
            # tree/node we just created.
            tree[best][val] = subtree

    return tree       


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
    

def view(tree):
     pp.pprint(tree)   



def classify_instance(tree, instance):
    print instance
    root = next(iter(tree))
    instance_value = instance[root]
    #branch = tree[root]
    
    '''print 'root', root
    print 'instance_value', instance_value
    print 'tree'
    pp.pprint(tree) '''
    
    while type(tree) == dict:
        tree = tree[root][instance_value]
        
        if type(tree) == dict:
            root = next(iter(tree))
            instance_value = instance[root]
            
        '''print 'root', root
        print 'instance_value', instance_value
        print 'tree'
        pp.pprint(tree) '''
    
    return tree

def classify(tree, test_data):
    classifications = []
    for row in test_data:
        classification = classify_instance(tree, row)
        classifications.append(classification)
        print 'classification', classification
        print
    
    return classifications    
    

def evaluate(test_data, classifications):
    #print 'classifications', classifications
    errors = 0.0
    for i in range(len(test_data)):
        #print 'classifications[i]',classifications[i], test_data[i][0]
        if classifications[i] != test_data[i][0]:
            errors += 1
            #print errors
            
    error_rate = errors / len(test_data)
    return error_rate


data = read_csv('agaricus-lepiota.data')
tree = train(data)
classifications = classify(tree, data)      #TODO split test/train data
error_rate = evaluate(data, classifications)
print error_rate

    
    
    
    
    
    
    
    
    
    
    
    
