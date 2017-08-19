




#Euclidean distance without sqrt
def euclidean_distance(row, instance):
    distance = 0.0
    for i in range(len(row) - 2):       #skip the y
        distance += (row[i] - instance[i]) ** 2
        
    return distance


def priority_queue_insert(priority_queue, value):
    for i in range(len(priority_queue)):
        entry = priority_queue[i]
        if value[0] >= entry[0]:
            priority_queue.insert(i + 1, value)
            

def average_ys(k_nearest_neighbors):
    sum = 0.0
    for neighbor in k_nearest_neighbors:
        sum += neighbor[0]
    
    return sum / len(k_nearest_neighbors)


def predict_instance(data, k, instance):
    distance_priority_queue = []        #List of tuples with distance, y
    for row in data:
        distance = euclidean_distance(row, instance)
        insert_value = (distance, instance[-1])
        priority_queue_insert(distance_priority_queue, insert_value)
        
    prediction = average_ys(distance_priority_queue[:k])    #pass in the k nearest neighbors
    return prediction


#return a list of predictions (regression)
def k-nearest-neighbor(data, k, instances):
    predictions = []
    for instance in instances:
        predictions.append(predict_instance(data, k, instance))
    
    
    