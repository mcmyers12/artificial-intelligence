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


def get_class_label_counts(data):
    p_count = 1.0
    e_count = 1.0
    for row in data:
        if row[0] == 'p':
            p_count += 1.0
        elif row[0] == 'e':
            e_count += 1.0
    
    print
    print 'p_count', p_count, 'e_count', e_count
    return p_count, e_count
    

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
                else:
                    print 'not p or e'
                    print
                    print 
                    row[0]
                    print
                    print
                    print
    
    pp.pprint(probability_counts)            
    return probability_counts


def get_class_probabilities(p_count, e_count):
    class_probabilities = { 'p' : {}, 'e' : {} }
    p_count = p_count - 1.0
    e_count = e_count - 1.0
    total = p_count + e_count
    
    class_probabilities['p']['probability'] = p_count / total
    class_probabilities['e']['probability'] = e_count / total
    class_probabilities['p']['count'] = p_count 
    class_probabilities['e']['count'] = e_count 
    
    return class_probabilities


def learn(data):
    probabilities = get_probability_counts(data)
    p_count, e_count = get_class_label_counts(data)
    
    for attribute_index in probabilities:
        for attribute_value in probabilities[attribute_index]:
            probabilities[attribute_index][attribute_value]['p'] = probabilities[attribute_index][attribute_value]['p'] / p_count
            probabilities[attribute_index][attribute_value]['e'] = probabilities[attribute_index][attribute_value]['e'] / e_count
    
    pp.pprint(probabilities)
    return probabilities


def calculate_probability(probabilities, instance, label, class_probabilities):
    probability = 1
    for attribute_index in range(len(instance) - 1):
        attribute_index += 1                                #skip class label
        attribute_value = instance[attribute_index]
        
        if attribute_value in probabilities[attribute_index]:
            probability *= probabilities[attribute_index][attribute_value][label]
        
        else:
            probability *= 1 / class_probabilities[label]['count']  #If some combination wasn't in the training data, do +1 smoothing
        
    probability *= class_probabilities[label]['probability']
    
    return probability


def normalize(results):
    denominator = results['p'] + results['e']
    
    results['p'] /= denominator
    results['e'] /= denominator
    
    return results


def classify_instance(probabilities, instance, class_probabilities):
    results = {}
    
    results['p'] = calculate_probability(probabilities, instance, 'p', class_probabilities)
    results['e'] = calculate_probability(probabilities, instance, 'e', class_probabilities)
    
    results = normalize(results)
    if results['p'] > results['e']:
        return ('p', results['p'])
    else:
        return ('e', results['e'])
    

#Returns a list of tuples: each is a class and the normalized probability of that class
#sorted in descending order
#[("e", 0.98), ("p", 0.02)]
def classify(probabilities, instances):
    classifications = []
    p_count, e_count = get_class_label_counts(data)
    class_probabilities = get_class_probabilities(p_count, e_count)

    for instance in instances:
        classifications.append(classify_instance(probabilities, instance, class_probabilities))
    
    #return sorted(classifications, key = lambda x: x[1])
    return classifications


#Uses the error rate    
def evaluate(data, classifications):
    errors = 0.0
    for i in range(len(data)):
        if classifications[i][0] != data[i][0]:
            errors += 1
    
    print 'errors ', errors
    print 'len(data) ', len(data)  
    error_rate = errors / len(data)
    return error_rate


data = read_csv('agaricus-lepiota.data')
set1, set2 = create_train_test_sets(data)


probabilities = learn(set1)
classifications = classify(probabilities, set2) 

error_rate = evaluate(set2, classifications)
print 'error_rate ', error_rate
print
print
print

probabilities = learn(set2)
classifications = classify(probabilities, set1) 

error_rate = evaluate(set1, classifications)
print 'error_rate ', error_rate
print
print
print












