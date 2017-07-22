import numpy as np
import matplotlib.pyplot as plt
import random
import math
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

plain = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]
forest = [0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0]
hills = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
swamp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0]

'''
figure = plt.figure(figsize=(20,6))

axes = figure.add_subplot(1, 3, 1)
pixels = np.array([255 - p * 255 for p in plain], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title( "Left Camera")
axes.imshow(pixels, cmap='gray')

axes = figure.add_subplot(1, 3, 2)
pixels = np.array([255 - p * 255 for p in forest], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title( "Front Camera")
axes.imshow(pixels, cmap='gray')

axes = figure.add_subplot(1, 3, 3)
pixels = np.array([255 - p * 255 for p in hills], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title( "Right Camera")
axes.imshow(pixels, cmap='gray')

plt.show()
plt.close()
'''

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


# Let's create a function that allows us to view any of these:
def view_sensor_image(data):
    figure = plt.figure(figsize=(4, 4))
    axes = figure.add_subplot(1, 1, 1)
    pixels = np.array([255 - p * 255 for p in data[:-1]], dtype='uint8')
    pixels = pixels.reshape((4, 4))
    axes.set_title("Left Camera:" + data[-1])
    axes.imshow(pixels, cmap='gray')
    plt.show()
    plt.close()


# view_sensor_image( clean_data[ "forest"][0])

# view_sensor_image( clean_data["swamp"][0])


def blur(data):
    def apply_noise(value):
        if value < 0.5:
            v = random.gauss(0.10, 0.05)
            if v < 0.0:
                return 0.0
            if v > 0.75:
                return 0.75
            return v
        else:
            v = random.gauss(0.90, 0.10)
            if v < 0.25:
                return 0.25
            if v > 1.00:
                return 1.00
            return v

    noisy_readings = [apply_noise(v) for v in data[0:-1]]
    return noisy_readings + [data[-1]]


# view_sensor_image( blur( clean_data["swamp"][0]))


def generate_hills(data, n, label, data_out):
    hill_index = 0
    for i in range(n):
        blurred_hill = blur(clean_data[label][hill_index])
        blurred_hill[-1] = 1.0
        blurred_hill.insert(0, 1.0)  # Add x_0 of 1
        data_out.append(blurred_hill)

        if hill_index < 3:
            hill_index += 1
        else:
            hill_index = 0


def generate_not_hills(data, n, label, data_out):
    not_hill_data = []
    for key in data:
        if key != label:
            for data_point in data[key]:
                not_hill_data.append(data_point)

    not_hill_index = 0
    for i in range(n):
        blurred_not_hill = blur(not_hill_data[not_hill_index])
        blurred_not_hill[-1] = 0.0
        blurred_not_hill.insert(0, 1.0)  # Add x_0 of 1
        data_out.append(blurred_not_hill)

        if not_hill_index < 6:
            not_hill_index += 1
        else:
            not_hill_index = 0


def generate_data(data, n, label):
    data_out = []

    # Create n hills, with equal number of different types of hills blurred
    generate_hills(data, n, label, data_out)

    # Create n not hills
    generate_not_hills(data, n, label, data_out)

    return data_out


'''
Use generate_data to generate 10 blurred "hills" examples with balanced (same number of) "non hills" 
examples to see that the function is working.
results = generate_data(clean_data, 10, "hills")
for result in results:
    for point in result:
        if type(point) == float:
            sys.stdout.write(str(round(point, 2)) + '\t')
        else:
            sys.stdout.write(point + ' ')
    print
'''



def dot_product(thetas, xs):
    z = 0
    xs_no_y = xs[0:len(xs) - 1]
    if len(thetas) != len(xs_no_y):
        print '\n\n\nthetas length different than xs\n\n\n'

    for i in range(len(thetas)):
        z += thetas[i] * xs[i]

    return z


def calculate_yhat(thetas, xs):
    z = dot_product(thetas, xs)
    yhat = 1 / (1 + math.e ** (-z))

    if yhat < 0 or yhat > 1:
        print '\n\n\nyhat not in range 0, 1\n\n\n'

    return yhat


def calculate_error(thetas, train_data):
    error_summation = 0
    for xs in train_data:
        y = xs[-1]
        yhat = calculate_yhat(thetas, xs)

        if yhat == 0 and (1 - yhat) == 0:
            pass

        elif yhat == 0:
            error_summation += ((1 - y) * math.log(1 - yhat))

        elif (1 - yhat) == 0:
            error_summation += (y * math.log(yhat))

        else:
            error_summation += (y * math.log(yhat) + (1 - y) * math.log(1 - yhat))

    n = len(train_data)  # TODO is this right?
    error = - (1.0 / n) * error_summation

    return error


def derivative(j, thetas, train_data):
    derivative_summation = 0

    n = len(train_data)

    for xs in train_data:
        y = xs[-1]
        yhat = calculate_yhat(thetas, xs)
        xij = xs[j]

        derivative_summation += (yhat - y) * xij

    deriv = (1.0 / n) * derivative_summation
    return deriv


# Use `learn_model` to learn a logistic regression model for classifying sensor images as "hills" or "not hills".
# Use your `generate_data` function to generate a training set with 100 hills examples. **Set Verbose to True**
# learn_model returns the List of Thetas.
def learn_model(train_data, verbose=False):
    epsilon = 1 / 10000000.0
    alpha = 0.1
    m = len(train_data[0]) - 1  # TODO IS THIS REALLY M??
    # initialize thetas to random values between [-1, 1]
    thetas = [random.uniform(-1, 1) for i in range(m)]  # TODO: should this be m?
    print 'length thetas: ', len(thetas)
    previous_error = 0.0
    current_error = calculate_error(thetas, train_data)
    while abs(current_error - previous_error) > epsilon:
        print 'thetas:', thetas

        new_thetas = [0 for i in range(m)]
        # print 'length new thetas: ', len(new_thetas)
        # print 'new thetas: ', (new_thetas)
        for j in range(m):  # TODO is this right?
            new_thetas[j] = thetas[j] - alpha * derivative(j, thetas, train_data)
        thetas = new_thetas

        print 'new thetas:', new_thetas

        if verbose:
            print 'error: ', current_error
            

        if current_error > previous_error:
            alpha = alpha / 10.0
            print 'GREATER'
            print
            print
        else:
            print 'LESS'
            print
            print
        previous_error = current_error

        current_error = calculate_error(thetas, train_data)


def apply_model(model, test_data, labeled=False):
    results = []
    for xs in test_data:
        yhat = calculate_yhat(model, xs)
        predicted = None
        if yhat < .5:
            predicted = 0
        else:
            predicted = 1
        
        
        if labeled:
            actual = xs[-1]
            results.append((actual, predicted))
        else:
           results.append((predicted, yhat))
            
    return results

#The calculate_confusion_matrix takes the results of apply_model when labeled=True 
#and prints a nice HTML version of a confusion matrix and include statistics for 
#error rate, true positive rate and true negative rate.
def calculate_confusion_matrix(results):
    n = len(results)
    TP = 0.0
    FP = 0.0
    FN = 0.0
    TN = 0.0
    for result in results:
        actual = result[0]
        predicted = result[1]
        if actual == predicted:
            if actual == 1:
                TP += 1
            else:
                TN += 1
        
        else:
            if predicted == 1:
                FP += 1
            else:
                FN += 1
    
    print "TP: ", TP
    print "FP: ", FP
    print "FN: ", FN
    print "TN: ", TN
    
    error = (FN + FP) / n
    print "error: ", error
    
    true_positive_rate = TP / (TP + FN)
    print "true_positive_rate: ", true_positive_rate

    true_negative_rate = TN / (TN + FP)
    print "true_negative_rate: ", true_negative_rate



train_data = generate_data(clean_data, 100, "hills")
#model = learn_model(train_data, True)
model = [-22.400546976561237, -10.451067964042313, -18.6086749056464, -14.1214695347607, -6.36399199170839, 11.428122477078729, 3.0248446407761627, 3.4316227441828544, 12.576993255048198, -10.316226530691987, 10.761316221645709, 12.501387621641353, -9.776272973274683, 0.3172110649805399, 13.275939870295009, 12.24751308359399, -4.983004296479011]

# Use `generate_data` to generate 100 blurred "hills" examples with balanced "non hills" examples and use 
# this as your test data. Set labeled=True and generate results to use in `calculate_confusion_matrix`. 
# Print out the first 10 results, one per line.
test_data = generate_data(clean_data, 100, "hills")


results = apply_model(model, test_data,True)
pp.pprint(results)

calculate_confusion_matrix( results)
