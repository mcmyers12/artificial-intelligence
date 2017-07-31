import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import copy
import math


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


def generate_labeled_data(data, n, label, one_hot_index, data_out):
    y = [0.0, 0.0, 0.0, 0.0]
    y[one_hot_index] = 1.0
    loop = len(data[label]) - 1

    index = 0
    for i in range(n):
        blurred_data = blur(data[label][index])
        blurred_data[-1] = y  # TODO: make sure I don't need to make a deep copy of this
        data_out.append(blurred_data)

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


def initialize_network(data, num_hidden_nodes, num_output_nodes):
    num_hidden_node_thetas = len(data[0])
    num_output_node_thetas = num_hidden_nodes + 1  # num hidden noes + 1 because of bias
    network = {'hidden_node_thetas': [], 'output_node_thetas': []}

    for i in range(num_hidden_nodes):
        hidden_node_thetas = [random.uniform(0, 1) for x in range(num_hidden_node_thetas)]
        network['hidden_node_thetas'].append(hidden_node_thetas)

    for i in range(num_output_nodes):
        output_node_thetas = [random.uniform(0, 1) for x in range(num_output_node_thetas)]
        network['output_node_thetas'].append(output_node_thetas)

    return network


def dot_product(thetas, xs):
    z = 0.0

    for i in range(len(thetas)):
        z += thetas[i] * xs[i]

    return z


def calculate_yhat(thetas, xs):
    z = dot_product(thetas, xs)
    yhat = 1.0 / (1.0 + math.e ** (-z))

    return yhat


def add_bias(xs):
    xs_with_bias = copy.deepcopy(xs)  # todo see if this is needed
    xs_with_bias.insert(0, 1.0)

    return xs_with_bias


def calculate_hidden_node_outputs(network, input_nodes):
    hidden_node_outputs = []
    input_nodes_with_bias = add_bias(input_nodes[:len(input_nodes) - 1])  # use only input node xs, without the y

    for hidden_node_thetas in network['hidden_node_thetas']:
        hidden_node_output = calculate_yhat(hidden_node_thetas, input_nodes_with_bias)
        hidden_node_outputs.append(hidden_node_output)

    return hidden_node_outputs


def calculate_output_node_outputs(network):
    output_node_outputs = []
    hidden_node_outputs_with_bias = add_bias(network['hidden_node_outputs'])

    for output_node_thetas in network['output_node_thetas']:
        output_node_output = calculate_yhat(output_node_thetas, hidden_node_outputs_with_bias)
        output_node_outputs.append(output_node_output)

    return output_node_outputs


def calculate_delta_o(y, yhat):
    delta_o = yhat * (1.0 - yhat) * (y - yhat)

    return delta_o


def calculate_delta_os(network, ys):
    delta_os = []

    for i in range(len(ys)):
        yhat = network['output_node_outputs'][i]
        y = ys[i]

        delta_o = calculate_delta_o(y, yhat)
        delta_os.append(delta_o)

    return delta_os


def calculate_delta_h(yhat, thetas, delta_os):
    delta_h = yhat * (1 - yhat)

    summation = 0.0
    for i in range(len(thetas)):
        theta = thetas[i]
        delta_o = delta_os[i]
        summation += (theta * delta_o)

    delta_h = delta_h * summation

    return delta_h


def calculate_delta_hs(network):
    delta_hs = []
    delta_os = network['delta_os']

    for i in range(len(network['hidden_node_thetas'])):
        thetas = []
        for output_node_thetas in network['output_node_thetas']:
            thetas.append(
                output_node_thetas[i + 1])  # Get the  first theta of each output node for the first hidden node,
            #   2nd of each output node for the second hidden node, etc.
            # i + 1 because we skip the theta for the bbias

        yhat = network['hidden_node_outputs'][i]  # TODO double check this is the right yhat but i'm pretty sure it is....
        delta_h = calculate_delta_h(yhat, thetas, delta_os)
        delta_hs.append(delta_h)

    return delta_hs


def update_output_node_thetas(network, alpha):
    for i in range(len(network['output_node_thetas'])):
        thetas = network['output_node_thetas'][i]
        delta_o = network['delta_os'][i]

        hidden_node_outputs_with_bias = add_bias(network['hidden_node_outputs'])
        for j in range(len(thetas)):
            hidden_node_y = hidden_node_outputs_with_bias[j]
            thetas[j] = thetas[j] + alpha * delta_o * hidden_node_y


def update_hidden_node_thetas(network, alpha, input_nodes):
    input_nodes_with_bias = add_bias(input_nodes[:len(input_nodes) - 1])  # use only input node xs, without the y

    for i in range(len(network['hidden_node_thetas'])):
        thetas = network['hidden_node_thetas'][i]
        delta_h = network['delta_hs'][i]

        for j in range(len(thetas)):
            xi = input_nodes_with_bias[j]
            thetas[j] = thetas[j] + alpha * delta_h * xi


def calculate_individual_error(ys, yhats):
    error_summation = 0
    for i in range(len(ys)):
        y = ys[i]
        yhat = yhats[i]

        if yhat == 0 and (1 - yhat) == 0:
            pass

        elif yhat == 0:
            error_summation += ((1 - y) * math.log(1 - yhat))

        elif (1 - yhat) == 0:
            error_summation += (y * math.log(yhat))

        else:
            error_summation += (y * math.log(yhat) + (1 - y) * math.log(1 - yhat))

    return error_summation
 
   
def calculate_error(data, network, alpha):
    error = 0
    test_network = {}
    test_network['hidden_node_thetas'] = copy.deepcopy(network['hidden_node_thetas'])
    test_network['output_node_thetas'] = copy.deepcopy(network['output_node_thetas'])

    for input_nodes in data:
        test_network['hidden_node_outputs'] = calculate_hidden_node_outputs(network, input_nodes)
        test_network['output_node_outputs'] = calculate_output_node_outputs(network)

        ys = input_nodes[-1]
        yhats = test_network['output_node_outputs']
        
        error += calculate_individual_error(ys, yhats)
            
        test_network['delta_os'] = calculate_delta_os(network, ys)
        test_network['delta_hs'] = calculate_delta_hs(test_network)  # TODO check this

        update_output_node_thetas(test_network, alpha)
        update_hidden_node_thetas(test_network, alpha, input_nodes)

    return -1/(error / len(data))
    


# Use `learn_model` to learn a ANN model for classifying sensor images as hills, swamps, plains or forest.
# The hidden layer will be one vector of thetas for each hidden node
# The output layer will be one vector of thetas for each output (4 outputs)
def learn_model(data, num_hidden_nodes, verbose=False):
    num_output_nodes = 4
    network = initialize_network(data, num_hidden_nodes, num_output_nodes)
    epsilon = 0.0000001
    alpha = 0.01 
    
    previous_error = 0.0
    current_error = float('-inf')

    iter = 0

    while iter < 5000 and abs(current_error - previous_error) > epsilon:
        iter += 1
        for input_nodes in data:
            # feed forward step
            # calculate output of every node in the network (yhat function)
            network['hidden_node_outputs'] = calculate_hidden_node_outputs(network, input_nodes)
            network['output_node_outputs'] = calculate_output_node_outputs(network)

            # back prop step
            # calculate delta_o for every output node
            ys = input_nodes[-1]
            network['delta_os'] = calculate_delta_os(network, ys)

            # calculate delta_h for every hidden node
            network['delta_hs'] = calculate_delta_hs(network)  # TODO check this

            # update all of the thetas
            update_output_node_thetas(network, alpha)
            update_hidden_node_thetas(network, alpha, input_nodes)

        if verbose and iter % 1000 == 0:
            print 'error: ', current_error

        previous_error = current_error

        current_error = calculate_error(data, network, alpha)

    return (network['hidden_node_thetas'], network['output_node_thetas'])


def get_labeled_data_results(actuals, predictions):
    result = []
    max_prediction_index = predictions.index(max(predictions))

    for i in range(len(predictions)):
        actual = actuals[i]
        if i != max_prediction_index:
            prediction = 0.0
            result.append((actual, prediction))

        else:
            prediction = 1.0
            result.append((actual, prediction))

    return result


def get_unlabeled_data_results(predictions):
    result = []
    max_prediction_index = predictions.index(max(predictions))

    for i in range(len(predictions)):
        prediction = predictions[i]
        if i != max_prediction_index:
            result.append((0, 1 - prediction))

        else:
            result.append((1, prediction))

    return result


def apply_model(model, test_data, labeled=False):
    network = {}
    results = []
    network['hidden_node_thetas'] = model[0]
    network['output_node_thetas'] = model[1]

    for input_nodes in test_data:
        network['hidden_node_outputs'] = calculate_hidden_node_outputs(network, input_nodes)
        network['output_node_outputs'] = calculate_output_node_outputs(network)

        if labeled:
            actuals = input_nodes[-1]
            predictions = network['output_node_outputs']
            result = get_labeled_data_results(actuals, predictions)
            results.append(result)

        else:
            predictions = network['output_node_outputs']
            result = get_unlabeled_data_results(predictions)
            results.append(result)

    return results


def calculate_validation_curve_error(results):
    n = 0.0
    errors = 0.0
    not_errors = 0.0
    for result in results:
        for point in results:
            error = False
            for pair in point:
                if pair[0] != pair[1]:
                    error = True
            if error:
                errors += 1.0

            else:
                not_errors += 1.0
            n += 1.0
    print 'errors', errors
    print 'not_errors', not_errors
    print
    print
    error_rate = errors / n
    return error_rate


def generate_validation_curves(clean_data):
    train = generate_data(clean_data, 100)
    test = generate_data(clean_data, 100)
    train_error_values = []
    test_error_values = []
    hidden_nodes = [2, 4, 8]
    for n in hidden_nodes:
        model = learn_model(train, n)  # verbose is False now please!
        train_results = apply_model(model, train, True)
        test_results = apply_model(model, test, True)

        train_error_values.append(calculate_validation_curve_error(train_results))
        test_error_values.append(calculate_validation_curve_error(test_results))

    print   'hidden_nodes', hidden_nodes
    print   'train_error_values', train_error_values
    print 'test_error_values', test_error_values

    plt.plot(hidden_nodes, train_error_values)
    plt.plot(hidden_nodes, test_error_values)
    plt.show()

generate_validation_curves(clean_data)


