import csv
import random
import pprint

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
    

def get_probability_counts(data):
    probability_counts = {}
    
    for i in range(len(data[0]) - 1):
        i = i + 1
        probability_counts[i] = {}
    
    for row in data:
        for i in range(len(row) - 1):
            i = i + 1
            attribute_value = row[i]
            if attribute_value not in probability_counts[i]:
                probability_counts[i][attribute_value] = {'p': 1.0, 'e': 1.0} #+1 smoothing
            else:
                if row[0] == 'p':
                    probability_counts[i][attribute_value]['p'] += 1.0
                elif row[0] == 'e':
                    probability_counts[i][attribute_value]['e'] += 1.0
    
    pp.pprint(probability_counts)            
    return probability_counts


def get_class_label_counts(data):
    class_label_counts = {'p': 1.0, 'e': 1.0} #+1 smoothing
    for row in data:
        if row[0] == 'p':
            class_label_counts['p'] += 1.0
        elif row[0] == 'e':
            class_label_counts['e'] += 1.0
    
    pp.pprint(class_label_counts)
    return class_label_counts
        


def learn(data):
    probabilities = get_probability_counts(data)
    class_label_counts = get_class_label_counts(data)
    p_count = class_label_counts['p']
    e_count = class_label_counts['e']
    
    for attribute_index in probabilities:
        for attribute_value in probabilities[attribute_index]:
            probabilities[attribute_index][attribute_value]['p'] = probabilities[attribute_index][attribute_value]['p'] / p_count
            probabilities[attribute_index][attribute_value]['e'] = probabilities[attribute_index][attribute_value]['e'] / e_count
    
    pp.pprint(probabilities)
    return probabilities
    
    

#Returns a list of tuples: each is a class and the normalized probability of that class
#sorted in descending order
#[("e", 0.98), ("p", 0.02)]
def classify(probabilities, instances):
    pass
    

#Uses the error rate    
def evaluate():
    pass


data = read_csv('agaricus-lepiota.data')
learn(data)













