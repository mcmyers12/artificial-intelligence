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
        probability *= probabilities[attribute_index][attribute_value][label]
        
    probability *= class_probabilities[label]
    
    print 'probability: '
    print '\tinstance: ', instance
    print '\tlabel: ', label    
    print '\tprobability: ', probability

    return probability


def normalize(results):
    denominator = results['p'] + results['e']
    
    print 'results before normalization: ', results

    results['p'] = results['p'] / denominator
    results['e'] = results['e'] / denominator

    print 'results after normalization: ', results

    
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
    


def get_class_probabilities(p_count, e_count):
    class_probabilities = {}
    p_count = p_count - 1.0
    e_count = e_count - 1.0
    total = p_count + e_count
    
    class_probabilities['p'] = p_count / total
    class_probabilities['e'] = e_count / total
    
    return class_probabilities


#Returns a list of tuples: each is a class and the normalized probability of that class
#sorted in descending order
#[("e", 0.98), ("p", 0.02)]
def classify(probabilities, instances):
    classifications = []
    p_count, e_count = get_class_label_counts(data)
    class_probabilities = get_class_probabilities(p_count, e_count)
    print 'class_probabilities', class_probabilities
    classify_instance(probabilities, instances[0], class_probabilities)
    
    #for instance in instances:
    #    classifications.append(classify_instance(probabilities, instance, class_probabilities))
    
    return sorted(classifications, key = lambda x: x[1])
    

#Uses the error rate    
def evaluate():
    pass


data = read_csv('agaricus-lepiota.data')
probabilities = learn(data)

classifications = classify(probabilities, data) #TODO use test data
#pp.pprint(classifications)











