import csv
import math
import random
import pprint

pp = pprint.PrettyPrinter(indent=4)

'''
1. Implement k-Nearest Neighbor regression as described in the Module.
'''
##################### K NEAREST NEIGHBOR #####################
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
         
        distance += (row[i] - instance[i]) ** 2.0
        
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
    

'''
2. Use validation curves as described in Module 9 to determine the best value of k trying 
    values of 1 to 10. (You don't need to use odd values for regression). For this you can 
    simply split the data randomly into a training and a test set with a 67/33 split.
'''
##################### VALIDATION CURVES #####################
def create_train_test_sets(data):
    random.shuffle(data)
    split_point = len(data) / 3
    test_set = data[:split_point]
    train_set = data[split_point:]
    
    return train_set, test_set
    

'''def generate_validation_curves(data):
    train_set, test_set = create_train_test_sets(data)
    train_error_values = []
    test_error_values = []
    k_values = [x for x in range(1, 11)]
    for k in k_values:
        model = learn_model(train, n)  # verbose is False now please!
        train_results = apply_model(model, train, True)
        test_results = apply_model(model, test, True)

        train_error_values.append(calculate_validation_curve_error(train_results))
        test_error_values.append(calculate_validation_curve_error(test_results))

    plt.plot(hidden_nodes, train_error_values)
    plt.plot(hidden_nodes, test_error_values)
    plt.show()'''


'''
3. Use learning curves as described in Module 9 to determine if your model could use more 
    data. For this you can simply split the data randomly into a training and a test set 
    with a 67/33 split. Use the best k from part 2.
'''



'''
4. Use 10-fold cross-validation to establish confidence bounds on your model's 
    performance. Calculate the mean (average) MSE (which sounds funny, I know) and the 
    standard deviation.
'''
def create_folds(data, num_folds):
    #folds = [[] for x in range(num_folds)]
    folds = []
    random.shuffle(data)
    
    fold_index = 0
    for i in range(0, len(data) - 1, num_folds):
        if fold_index < num_folds:

            folds.append(data[i:i + num_folds])
            '''for f in folds:
                for instance in f:
                    print instance
            print
            print'''
            fold_index += 1
        
    return folds


def calculate_mean_squared_error(actuals, predictions):
    mse = 0.0
    num_observations = len(actuals)
    for i in range(num_observations):
        actual = actuals[i]
        prediction = predictions[i]
        mse += (actual - prediction) ** 2.0
    
    mse = mse / num_observations
    return mse


def calculate_standard_deviation(mean, values):
    print 'mse_values', values
    standard_deviation = 0.0
    for value in values:
        standard_deviation += (value - mean) ** 2
    
    standard_deviation /= len(values)
    standard_deviation = math.sqrt(standard_deviation)
    return standard_deviation
    
 
def cross_validation(data, k):
    average_mse = 0.0
    mse_values = []
    num_folds = 10
    folds = create_folds(data, num_folds)
    
    pp.pprint(folds)
    print len(folds)
    for i in range(len(folds)):
        instances = folds[i]                         #chunk of instances
        train = []                              #bigger chunk of instances
        for fold in folds[:i]:
            for instance in fold:
                train.append(instance)
        for fold in folds[i + 1:]:
            for instance in fold:
                train.append(instance)
        
        predictions = k_nearest_neighbors(train, k, instances)        #TODO make sure this is right...
        actuals = [x[-1] for x in instances]
        mse = calculate_mean_squared_error(actuals, predictions)
        
        print
        print 'actuals'
        pp.pprint(actuals)
        print
        print 'predictions'
        pp.pprint([round(x,2) for x in predictions])
        print 'mse', mse
        print
        
        average_mse += mse
        mse_values.append(mse)
    
    average_mse = average_mse / num_folds
    standard_deviation = calculate_standard_deviation(average_mse, mse_values)
    
    print "Average MSE: ", average_mse
    print "Standard Deviation: ", standard_deviation




#generate_validation_curves(clean_data)
    

data = read_csv('concrete-data.csv')

'''random.shuffle(data)
instances = data[:10]
predictions = k_nearest_neighbors(data, 10, instances)

print
print 'actuals'
pp.pprint([x[-1] for x in instances])
print
print 'predictions'
pp.pprint([round(x,2) for x in predictions])'''


cross_validation(data, 10)










    
    