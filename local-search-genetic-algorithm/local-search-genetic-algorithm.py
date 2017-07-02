from StringIO import StringIO
import random
from random import gauss
import copy


# Transform the fitness score for minimization
def minimization_fitness(fitness_score):
    return 1 / (1 + fitness_score)


# Return list of 10 floats
# Return list of 10 random numbers between -5.12 to 5.12 ##TODO is this right?
def initialize_phenotype(dimensions):
    phenotype = []
    for i in range(dimensions):
        phenotype.append(round(random.uniform(-5.12, 5.12), 2))
    return phenotype


# Use a 10 bit binary encoding for each xi . This gives each xi a potential value of 0 to 1024
# which can be mapped to (-5.12, 5.12) by subtracting 512 and dividing by 100
# Genotype is a single list of 100 bits
def binary_ga_genotype_to_phenotype(genotype):
    split_genotype = [genotype[i:i + 10] for i in xrange(0, len(genotype), 10)]
    phenotype = []
    for binary_representation in split_genotype:
        decimal_representation = int("".join(str(x) for x in binary_representation), 2)
        decimal_representation = (decimal_representation - 512.0) / 100
        phenotype.append(decimal_representation)
    return phenotype


def binary_ga_phenotye_to_genotype(phenotype):
    genotype = []
    for decimal_representation in phenotype:
        decimal_representation = int((decimal_representation * 100) + 512)
        binary_representation = [int(x) for x in bin(decimal_representation)[2:]]
        for bit in binary_representation:
            genotype.append(bit)
    return genotype


# generate n random individuals according to the encoding scheme, the genetic code
# initialize each individual as a dict with field "genotype"
# the actual genetic presentation will be a List of 10*dimensions bits or dimensions real numbers
def binary_ga_initialize_population(population_size, dimensions):
    population = []
    for i in range(population_size):
        individual = {}
        phenotype = initialize_phenotype(dimensions)
        individual["phenotype"] = phenotype
        individual["genotype"] = binary_ga_phenotye_to_genotype(phenotype)
        population.append(individual)

    return population


def real_ga_initialize_population(population_size, dimensions):
    population = []
    for i in range(population_size):
        individual = {}
        phenotype = initialize_phenotype(dimensions)
        individual["phenotype"] = phenotype
        individual["genotype"] = copy.deepcopy(phenotype)
        population.append(individual)

    return population


def calculate_fitness(individual, minimization):
    phenotype = individual["phenotype"]
    fitness = sphere(0.5, phenotype)
    
    if minimization:
        fitness = minimization_fitness(fitness)
    
    individual["fitness"] = fitness


# each individual should contain at least fields for its genome and fitness score
# evaluate applies the fitness function to each individual (make sure to transform fitness score)
def evaluate_population(population, minimization):
    best_fitness = float("-inf")
    best_individual = None
    for individual in population:
        calculate_fitness(individual, minimization)
        fitness = individual["fitness"]
        if fitness > best_fitness:
            best_individual = individual
            best_fitness = fitness

    return best_individual


def select_parent(random_selection):
    max_fitness = float("-inf")
    for individual in random_selection:
        fitness = individual["fitness"]
        if fitness > max_fitness:
            max_fitness = fitness
            max_parent = individual

    return max_parent



def get_random_indices(population, tournament_selection_number):
    random_indices = []
    while len(random_indices) < tournament_selection_number:
        random_index = random.randint(0, (len(population) - 1))
        if random_index not in random_indices:
            random_indices.append(random_index)
            
    return random_indices

# There are many ways to pick parents - two options:
# Roulette wheel: each individual's fitness is a proportion of total fitness (more in notes)
# Tournament selection: pick 7 (or so) completely (uniformly) at random, choose one with highest fitness
# Ensures parent 1 and 2 are different by removing parent 1 from randomly 7 selected values for parent 2, if there
def select_parents_tournament_selection(population, tournament_selection_number):
    #population_copy = copy.deepcopy(population)  ##TODO may not need to copy
    random_indices = get_random_indices(population, tournament_selection_number)
     
    random_individuals = []       
    for index in random_indices:
        random_individuals.append(population[index])
    
    parent1 = select_parent(random_individuals)
    
    random_indices = get_random_indices(population, tournament_selection_number)
     
    random_individuals = []       
    for index in random_indices:
        random_individuals.append(population[index])

    if parent1 in random_individuals:
        random_individuals.remove(parent1)
    parent2 = select_parent(random_individuals)

    return parent1, parent2


def binary_ga_crossover(parent1, parent2):
    child1 = {}
    child2 = {}

    parent1_genotype = parent1["genotype"]
    parent2_genotype = parent2["genotype"]

    crossover_index = random.randint(0, len(parent1_genotype) - 1)

    child1_genotype = parent1_genotype[:crossover_index] + parent2_genotype[crossover_index:]
    child2_genotype = parent2_genotype[:crossover_index] + parent1_genotype[crossover_index:]

    child1["genotype"] = child1_genotype
    child2["genotype"] = child2_genotype

    child1["phenotype"] = binary_ga_genotype_to_phenotype(child1_genotype)
    child2["phenotype"] = binary_ga_genotype_to_phenotype(child2_genotype)

    return child1, child2
    

def real_ga_crossover(parent1, parent2):
    child1 = {}
    child2 = {}

    parent1_genotype = parent1["genotype"]
    parent2_genotype = parent2["genotype"]

    crossover_index = random.randint(0, len(parent1_genotype) - 1)

    child1_genotype = parent1_genotype[:crossover_index] + parent2_genotype[crossover_index:]
    child2_genotype = parent2_genotype[:crossover_index] + parent1_genotype[crossover_index:]

    child1["genotype"] = child1_genotype
    child2["genotype"] = child2_genotype

    child1["phenotype"] = child1_genotype
    child2["phenotype"] = child2_genotype

    return child1, child2


# randomly pick a mutation site, randomly pick a mutation
def binary_ga_mutate(child):
    genotype = child["genotype"]
    mutation_site = random.randint(0, len(genotype) - 1)
    mutation = random.randint(0, 1)
    genotype[mutation_site] = mutation
    

#use gaussian distribution, selecting 1.7 as the standard deviation, since this is 5.12 / 3
def real_ga_mutate(child):
    genotype = child["genotype"]
    mutation_site = random.randint(0, len(genotype) - 1)
    mutation = gauss(0, 1.7)
    while mutation > 5.12 or mutation < -5.12:
        mutation = gauss(0, 1.7)
    genotype[mutation_site] = mutation
    

def reproduce(parent1, parent2, crossover_rate, mutation_rate, crossover, mutate):
    crossover_chance = random.uniform(0, 1)
    if crossover_chance > crossover_rate:
        return parent1, parent2

    child1, child2 = crossover(parent1, parent2)

    child1_mutation_chance = random.uniform(0, 1)
    if child1_mutation_chance < crossover_rate:
        mutate(child1)

    child2_mutation_chance = random.uniform(0, 1)
    if child2_mutation_chance < crossover_rate:
        mutate(child2)

    return child1, child2


# Create a population, evaluate it, select parents, apply crossover and mutation, repeat until the number of desired generations have been generated
# Use higher order functions

# Print out the best individual of each generation including the generation number,
    # genotype (the representation), phenotype (the actual value), the fitness (based on your fitness function transformation)
    # and the function value (for the shifted sphere) if passed a DEBUG=True flag.
# Keep the tracing limited - print the best individual of the population every i generations (e.g. every 10)
    # should see about 50 lines of tracing to show the best individual and their fitness
def genetic_algorithm(parameters, initialize_population, crossover, mutate):
    population_size = parameters["population_size"]
    population = initialize_population(population_size, parameters["dimensions"])

    best_individual = { "fitness": float("-inf") }  # TODO may not need to initialize this

    generations = 0
    while generations < parameters["number_of_generations"]:
        print 'generations', generations
        candidate_best_individual = evaluate_population(population, parameters["minimization"])  # each individual gets a fitness score before we go to pick parents

        if candidate_best_individual["fitness"] > best_individual["fitness"]:
            best_individual = candidate_best_individual
            print 'fitness', best_individual["fitness"]

        next_population = []
        for i in range(population_size / 2):
            parent1, parent2 = select_parents_tournament_selection(population, parameters["tournament_selection_number"])
            child1, child2 = reproduce(parent1, parent2, parameters["crossover_rate"], parameters["mutation_rate"], crossover, mutate)

            next_population.append(child1)
            next_population.append(child2)

        population = next_population  # always replace the entire population with a new population
        generations += 1

    # return the best individual ever encountered (and all their data including genotype, phenotype, fitness, and actual objective function value)
    print '\n\n\nBest Individual:\n', best_individual
    return best_individual


def binary_ga(parameters):
    genetic_algorithm(parameters, binary_ga_initialize_population, binary_ga_crossover, binary_ga_mutate)


def real_ga(parameters):
    genetic_algorithm(parameters, real_ga_initialize_population, real_ga_crossover, real_ga_mutate)


def sphere(shift, xs):
    return sum([(x - shift) ** 2 for x in xs])



# There is some trade off between population size and generations (parameters to experiment with)
# Should not take long at all to converge
binary_ga_parameters = {
    "f": lambda xs: sphere(0.5, xs),
    "minimization": True,  
    "mutation_rate": .05,
    "crossover_rate": .9,
    "population_size": 10000,  # 50-500s of individuals
    "dimensions": 10,  # (given for this problem),
    "number_of_generations": 100,  
    "tournament_selection_number": 7
}
#binary_ga(binary_ga_parameters)


real_ga_parameters = {
    "f": lambda xs: sphere(0.5, xs),
    "minimization": True,  
    "mutation_rate": .05,
    "crossover_rate": .9,
    "population_size": 5000,  # 50-500s of individuals
    "dimensions": 10,  # (given for this problem),
    "number_of_generations": 600,  
    "tournament_selection_number": 100
}
real_ga(real_ga_parameters)















