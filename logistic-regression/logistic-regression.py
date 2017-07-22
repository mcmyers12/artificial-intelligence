import numpy as np
import matplotlib.pyplot as plt
import random
import math
import sys

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


'''
With the clean examples and the blur function, we have an unlimited amount of data for training 
and testing our classifier, a logistic regression that determines if a sensor image is hills (1) or not (0).
In classification, there is a general problem called the "unbalanced class problem". In general, we want 
our training data to have the same number of classes, in this case "hills" and "not hills". This means you 
should probably generate training data with, say, 100 hills and then 100 of all the other types of terrain 
combined. When you send your data to the actual learn_model function, it will need to have all the 
String labels transformed to 0 or 1 appropriately. Remember, you also need to set  x0x0  = 1.0; where you 
do that is up to you but you need to be consistent (if you do it in generate_data then don't also do it in 
learn_model or apply_model.
You can make generate_data as sophisticated as you like. But it should at least take n and a label so that:
generate_data( clean_data, 100, "hills")
generates 100 hills, 100 not hills and has transformed the String labels into 1 and 0, respectively.
'''


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
    m = len(train_data[0])  # TODO IS THIS REALLY M??
    # initialize thetas to random values between [-1, 1]
    thetas = [random.uniform(-1, 1) for i in range(m - 1)]  # TODO: should this be m?
    print 'length thetas: ', len(thetas)
    previous_error = 0.0
    current_error = calculate_error(thetas, train_data)
    while abs(current_error - previous_error) > epsilon:
        print 'thetas:', thetas

        new_thetas = [0 for i in range(m - 1)]
        # print 'length new thetas: ', len(new_thetas)
        # print 'new thetas: ', (new_thetas)
        for j in range(m - 1):  # TODO is this right?
            new_thetas[j] = thetas[j] - alpha * derivative(j, thetas, train_data)
        thetas = new_thetas

        print 'new thetas:', new_thetas

        if verbose:
            print 'error: ', current_error
            

        if current_error < previous_error:
            print 'LESS'
            print
            print
        else:
            print 'GREATER'
            print
            print
        previous_error = current_error

        current_error = calculate_error(thetas, train_data)


train_data = generate_data(clean_data, 100, "hills")
model = learn_model(train_data, True)

# Use `generate_data` to generate 100 blurred "hills" examples with balanced "non hills" examples and use this as your test data. Set labeled=True and generate results to use in `calculate_confusion_matrix`. Print out the first 10 results, one per line.
'''
test_data = generate_data( clean_data, 100, "hills")

def apply_model( model, test_data, labeled=False):
    pass

results = apply_model( model, test_data)
print results


# Using the results above, show your confusion matrix for your model.
def calculate_confusion_matrix( results):
    pass
'''