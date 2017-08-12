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
    

def initialize_probability_counts(data):
    probability_counts = {}
    
    for i in range(len(data[0]) - 1):
        i = i + 1           #Skip the first column
        probability_counts[i] = {}
    
    for row in data:
        for i in range(len(row) - 1):
            i = i + 1           #Skip the first column
            attribute_value = row[i]
            if attribute_value not in probability_counts[i]:
                probability_counts[i][attribute_value] = {'p': 1, 'e': 1}
            else:
                if row[0] == 'p':
                    probability_counts[i][attribute_value]['p'] += 1
                elif row[0] == 'e':
                    probability_counts[i][attribute_value]['e'] += 1
    
    pp.pprint(probability_counts)            
    return probability_counts


def calculate_class_probabilities(data):
    pass


def learn(data):
    pass
    

#Returns a list of tuples: each is a class and the normalized probability of that class
#sorted in descending order
#[("e", 0.98), ("p", 0.02)]
def classify(probabilities, instances):
    pass
    

#Uses the error rate    
def evaluate():
    pass


data = read_csv('agaricus-lepiota.data')
initialize_probability_counts(data)













