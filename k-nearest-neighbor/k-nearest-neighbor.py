import csv
import random
import pprint

pp = pprint.PrettyPrinter(indent=4)


#Skip the first row
def read_csv(file_name):
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)
        table = [[float(x) for x in record] for record in reader]
    
    return table[1:len(table)]
    

#Euclidean distance without sqrt
def euclidean_distance(row, instance):
    distance = 0.0
    for i in range(len(row) - 2):       #skip the y
         
        distance += (row[i] - instance[i]) ** 2
        
    return distance


def priority_queue_insert(priority_queue, value):
    for i in range(len(priority_queue)):
        entry = priority_queue[i]
        if value[0] <= entry[0]:
            priority_queue.insert(i, value)
            return
    
    if value not in priority_queue:
        priority_queue.append(value)
            

def average_ys(k_nearest_neighbors):
    sum = 0.0
    for neighbor in k_nearest_neighbors:
        sum += neighbor[-1]
    
    return sum / len(k_nearest_neighbors)


def predict_instance(data, k, instance):
    distance_priority_queue = []        #List of tuples with distance, y
    for row in data:
        distance = euclidean_distance(row, instance)
        insert_value = (distance, row[-1])
        priority_queue_insert(distance_priority_queue, insert_value)
    
    prediction = average_ys(distance_priority_queue[:k])    #pass in the k nearest neighbors
    return prediction


#return a list of predictions (regression)
def k_nearest_neighbors(data, k, instances):
    predictions = []
    for instance in instances:
        predictions.append(predict_instance(data, k, instance))
        
    return predictions
    


def create_train_test_sets(data):
    random.shuffle(data)
    split_point = len(data) / 3
    test_set = data[:split_point]
    train_set = data[split_point:]
    
    return train_set, test_set
    

data = read_csv('concrete-data.csv')
train_set, test_set = create_train_test_sets(data)

random.shuffle(data)
instances = data[:10]
predictions = k_nearest_neighbors(data, 10, instances)

print
print 'actuals'
pp.pprint([x[-1] for x in instances])
print
print 'predictions'
pp.pprint([round(x,2) for x in predictions])











    
    