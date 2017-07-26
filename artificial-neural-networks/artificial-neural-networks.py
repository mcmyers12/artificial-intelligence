import numpy as np
import matplotlib.pyplot as plt
import random
import sys


clean_data = {
    "plains": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, "plains"]
    ],
    "forest": [
        [0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, "forest"],
        [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, "forest"],
        [1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, "forest"],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, "forest"]
    ],
    "hills": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, "hills"]
    ],
    "swamp": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, "swamp"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, "swamp"]        
    ]
}



def blur( data):
    def apply_noise( value):
        if value < 0.5:
            v = random.gauss( 0.10, 0.05)
            if v < 0.0:
                return 0.0
            if v > 0.75:
                return 0.75
            return v
        else:
            v = random.gauss( 0.90, 0.10)
            if v < 0.25:
                return 0.25
            if v > 1.00:
                return 1.00
            return v
    noisy_readings = [apply_noise( v) for v in data[0:-1]]
    return noisy_readings + [data[-1]]



def generate_hills(data, n, data_out):
    y = [1, 0, 0, 0]

    hill_index = 0
    for i in range(n):
        blurred_hill = blur(clean_data["hills"][hill_index])
        blurred_hill[-1] = y                        #TODO: make sure I don't need to make a deep copy of this
        data_out.append(blurred_hill)

        if hill_index < 3:
            hill_index += 1
        else:
            hill_index = 0


def generate_swamps(data, n, data_out):
    y = [0, 1, 0, 0]

    swamp_index = 0
    for i in range(n):
        blurred_hill = blur(clean_data["hills"][hill_index])
        blurred_hill[-1] = y                        #TODO: make sure I don't need to make a deep copy of this
        data_out.append(blurred_hill)

        if hill_index < 3:
            hill_index += 1
        else:
            hill_index = 0
            

def generate_forests(data, n, data_out):
    y = [0, 0, 1, 0]

    swamp_index = 0
    for i in range(n):
        blurred_hill = blur(clean_data["hills"][hill_index])
        blurred_hill[-1] = y                        #TODO: make sure I don't need to make a deep copy of this
        data_out.append(blurred_hill)

        if hill_index < 3:
            hill_index += 1
        else:
            hill_index = 0
            

def generate_labeled_data(data, n, label, one_hot_index, data_out):
    y = [0, 0, 0, 0]
    y[one_hot_index] = 1
    loop = len(data[label]) - 1

    index = 0
    for i in range(n):
        blurred_data = blur(data[label][index])
        blurred_data[-1] = y                        #TODO: make sure I don't need to make a deep copy of this
        data_out.append(blurred_data)
        
        #TODO remove
        data_out.append(data[label][index])

        if index < loop:
            index += 1
        else:
            index = 0


def generate_data(data, n):
    data_out = []

    generate_labeled_data(data, n, "hills", 0, data_out)
    generate_labeled_data(data, n, "swamp", 1, data_out)
    generate_labeled_data(data, n, "forest", 2, data_out)
    generate_labeled_data(data, n, "plains", 3, data_out)

    return data_out


results = generate_data( clean_data, 10)
for result in results:
    for x in result:
        if type(x) == float:
            sys.stdout.write(str(round(x, 2)) + '\t')
        else:
            sys.stdout.write(str(x) + '\t')
    print

'''
# Use `learn_model` to learn a ANN model for classifying sensor images as hills, swamps, plains or forest. Use your `generate_data` function to generate a training set with 100 examples for each. **Set Verbose to True**
def learn_model( data, hidden_nodes, verbose=False):
    pass

train_data = generate_data( clean_data, 100)
model = learn_model( train_data, 2, True)


# Use `generate_data` to generate 100 blurred examples of each terrain and use this as your test data. Print out the first 10 results, one per line.
test_data = generate_data( clean_data, 100)

def apply_model( model, test_data, labeled=False):
    pass

results = apply_model( model, test_data)
print results


# Now that you're pretty sure your algorithm works (the error rate during training is going down, and you can evaluate `apply_model` results for its error rate, learn validation curves:
def calculate_confusion_matrix( results):
    pass



train = generate_data( clean_data, 100)
test  = generate_data( clean_data, 100)
for n in [2, 4, 8]:
    model = learn_model( train, n) # verbose is False now please!
    train_results = apply_model( model, train)
    test_results = apply_model( model, test)
    # evaluate results for for each
# plot


# which number of hidden nodes is best? ____
'''