import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import pprint
import copy
import math

pp = pprint.PrettyPrinter(indent=4)

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


def generate_labeled_data(data, n, label, one_hot_index, data_out):
    y = [0.0, 0.0, 0.0, 0.0]
    y[one_hot_index] = 1.0
    loop = len(data[label]) - 1

    index = 0
    for i in range(n):
        blurred_data = blur(data[label][index])
        blurred_data[-1] = y                        #TODO: make sure I don't need to make a deep copy of this
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
    num_output_node_thetas = num_hidden_nodes + 1                             #num hidden noes + 1 because of bias
    network = { 'hidden_node_thetas': [], 'output_node_thetas': [] }
    
    for i in range(num_hidden_nodes):
        hidden_node_thetas = [random.uniform(0, 1) for x in range(num_hidden_node_thetas)]
        network['hidden_node_thetas'].append(hidden_node_thetas)
        
    for i in range(num_output_nodes):
        output_node_thetas = [random.uniform(0, 1) for x in range(num_output_node_thetas)]
        network['output_node_thetas'].append(output_node_thetas)
        
    return network


def dot_product(thetas, xs):
    z = 0.0
    if len(thetas) != len(xs):
        print '\n\n\nthetas length different than xs\n\n\n'
        print len(thetas) 
        print len(xs)

    for i in range(len(thetas)):
        z += thetas[i] * xs[i]

    return z


def calculate_yhat(thetas, xs):
    z = dot_product(thetas, xs)
    yhat = 1.0 / (1.0 + math.e ** (-z))

    if yhat < 0 or yhat > 1:
        print '\n\n\nyhat not in range 0, 1\n\n\n'

    return yhat


def add_bias(xs):
    xs_with_bias = copy.deepcopy(xs)                #todo see if this is needed
    xs_with_bias.insert(0, 1.0)  
    
    return xs_with_bias  


def calculate_hidden_node_outputs(network, input_nodes):
    hidden_node_outputs = []
    input_nodes_with_bias = add_bias(input_nodes[:len(input_nodes)-1])       #use only input node xs, without the y
    
    #print 'input_nodes', input_nodes
    #print 'input_nodes_with_bias', input_nodes_with_bias
    
    for hidden_node_thetas in network['hidden_node_thetas']:
        #print '\thidden_node_thetas'
        #pp.pprint(hidden_node_thetas)
        
        hidden_node_output = calculate_yhat(hidden_node_thetas, input_nodes_with_bias)
        hidden_node_outputs.append(hidden_node_output)
    
    '''print 'hidden_node_outputs', hidden_node_outputs
    print 
    print
    print'''    
    return hidden_node_outputs


def calculate_output_node_outputs(network):
    output_node_outputs = []
    hidden_node_outputs_with_bias = add_bias(network['hidden_node_outputs'])        

    '''print 'hidden_node_outputs_with_bias', hidden_node_outputs_with_bias
    print'''
    
    for output_node_thetas in network['output_node_thetas']:
        #print 'output_node_thetas', output_node_thetas
        output_node_output = calculate_yhat(output_node_thetas, hidden_node_outputs_with_bias)
        output_node_outputs.append(output_node_output)

    '''print 'output_node_outputs', output_node_outputs
    print 
    print
    print'''

    return output_node_outputs


def calculate_delta_o(y, yhat):
    delta_o = yhat * (1.0 - yhat) * (y - yhat)
    
    return delta_o


def calculate_delta_os(network, ys):
    delta_os = []
    '''print 'ys', ys
    print 'output_node_outputs', network['output_node_outputs']'''
    for i in range(len(ys)):
        yhat = network['output_node_outputs'][i]
        y = ys[i]
        
        delta_o = calculate_delta_o(y, yhat)
        delta_os.append(delta_o)
    
    
    '''print 'delta_os', delta_os
    print
    print'''
    return delta_os


def calculate_delta_h(yhat, thetas, delta_os):
    delta_h = yhat * (1 - yhat)
    
    if len(thetas) != len(delta_os):
        print '\n\n\nthetas length not equal to delta_os length\n\n\n'
    
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
            thetas.append(output_node_thetas[i + 1])            #Get the  first theta of each output node for the first hidden node, 
                                                                #   2nd of each output node for the second hidden node, etc.
                                                                #i + 1 because we skip the theta for the bbias
    
        yhat = network['hidden_node_outputs'][i]                #TODO double check this is the right yhat but i'm pretty sure it is....
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
    input_nodes_with_bias = add_bias(input_nodes[:len(input_nodes)-1])       #use only input node xs, without the y
    
    '''print 'input_nodes_with_bias'
    pp.pprint(input_nodes_with_bias)'''
    
    for i in range(len(network['hidden_node_thetas'])):
        thetas = network['hidden_node_thetas'][i]
        delta_h = network['delta_hs'][i]
        
        '''print 'thetas'
        pp.pprint(thetas)
        print 'delta_h', delta_h'''

        for j in range(len(thetas)):
            xi = input_nodes_with_bias[j]
            thetas[j] = thetas[j] + alpha * delta_h * xi
            
        '''print 'new_thetas' 
        pp.pprint(thetas)
        print
        print'''
 
 
 #TODO is this right?
 
 #LEFT OFF FIGURING OUT HOW TO CALCULATE ERROR
def calculate_error(network, ys):
    '''error = 0
    for i in range(len(ys)):
        y = ys[i]  
        yhat = network['output_node_outputs'][i]
        
        #error += abs(y - yhat)
        error += calculate_delta_o(y, yhat)
        
    return error''' 
    
    error_summation = 0
    for i in range(len(ys)):
        y = ys[i]
        yhat = network['output_node_outputs'][i]

        if yhat == 0 and (1 - yhat) == 0:
            pass

        elif yhat == 0:
            error_summation += ((1 - y) * math.log(1 - yhat))

        elif (1 - yhat) == 0:
            error_summation += (y * math.log(yhat))

        else:
            error_summation += (y * math.log(yhat) + (1 - y) * math.log(1 - yhat))

    n = len(ys)  # TODO is this right?
    error = - (1.0 / n) * error_summation
    return error
    

# Use `learn_model` to learn a ANN model for classifying sensor images as hills, swamps, plains or forest. 
# The hidden layer will be one vector of thetas for each hidden node
# The output layer will be one vector of thetas for each output (4 outputs)
def learn_model(data, num_hidden_nodes, verbose=False):
    num_output_nodes = 4
    network = initialize_network(data, num_hidden_nodes, num_output_nodes)   
    epsilon = 1 / 10000000.0
    alpha = 0.1                         #TODO make alpha adaptive 
    previous_error = 0.0
    current_error = float('inf')
    
    #pp.pprint(network)
    
    #previous_error = 0.0
    while True: # abs(current_error - previous_error) > epsilon:
        for input_nodes in data:
            
            #feed forward step
            #calculate output of every node in the network (yhat function)
            network['hidden_node_outputs'] = calculate_hidden_node_outputs(network, input_nodes)
            network['output_node_outputs'] = calculate_output_node_outputs(network)

            #back prop step
            #calculate delta_o for every output node
            ys = input_nodes[-1]
            network['delta_os'] = calculate_delta_os(network, ys)

            #calculate delta_h for every hidden node            
            network['delta_hs'] = calculate_delta_hs(network)           #TODO check this

            #update all of the thetas
            update_output_node_thetas(network, alpha)
            update_hidden_node_thetas(network, alpha, input_nodes)
            
            print 'ys' 
            pp.pprint(ys)
            print 'y_hats'
            pp.pprint(network['output_node_outputs'])
            print
            print
            
            
        '''    
        if verbose:
            print 'error: ', current_error
            #print network['hidden_node_outputs']
            #print network['output_node_outputs']
        
        print 'alpha', alpha
        if current_error > previous_error:
            alpha = alpha / 10.0
            print 'GREATER'
            print
            print
        else:
            print 'LESS'
            print
            print
            
        '''        
        previous_error = current_error
        
        current_error = calculate_error(network, ys)
        
        pp.pprint(network)
        print
        print            

    return (network['hidden_node_thetas'], network['output_node_thetas'])
    





train_data = generate_data( clean_data, 100)
'''for result in train_data:
    for x in result:
        if type(x) == float:
            sys.stdout.write(str(round(x, 2)) + '\t')
        else:
            sys.stdout.write(str(x) + '\t')
    print
print'''
model = learn_model( train_data, 2, True)
print
pp.pprint(model)

'''
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

