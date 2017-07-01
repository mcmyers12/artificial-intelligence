from IPython.core.display import *
from StringIO import StringIO
import random
import copy



#Transform the fitness score for minimization
def minimization_fitness(fitness_score):
    return 1 / (1 + fitness_score)
    

#Return list of 10 floats
#Return list of 10 random numbers between -5.12 to 5.12 ##TODO is this right?
def initialize_phenotype(dimensions):
    phenotype = []
    for i in range(dimensions):
        phenotype.append(round(random.uniform(-5.12, 5.12), 2))
    return phenotype  


#Use a 10 bit binary encoding for each xi . This gives each xi a potential value of 0 to 1024 
    #which can be mapped to (-5.12, 5.12) by subtracting 512 and dividing by 100
#Genotype is a single list of 100 bits
def binary_ga_genotype_to_phenotype(genotype):
    split_genotype = [genotype[i:i + 10] for i in xrange(0, len(genotype), 10)]
    phenotype = []
    for binary_representation in split_genotype:
        decimal_representation = int("".join(str(x) for x in binary_representation),2)
        decimal_representation = (decimal_representation - 512.0) / 100
        phenotype.append(decimal_representation)    
    return phenotype
        
        

def binary_ga_phenotye_to_genotype(phenotype):
    genotype = []
    for decimal_representation in phenotype:
        print 'original: ', decimal_representation
        decimal_representation = int((decimal_representation * 100) + 512)
        print 'decimal_representation: ', decimal_representation
        binary_representation = [int(x) for x in bin(decimal_representation)[2:]]
        print 'binary_representation: ', binary_representation
        print 'back to original: ', (decimal_representation - 512.0) / 100
        for bit in binary_representation:
            genotype.append(bit)
    return genotype


#generate n random individuals according to the encoding scheme, the genetic code
#initialize each individual as a dict with field "genotype"
#the actual genetic presentation will be a List of 10*dimensions bits or dimensions real numbers
def binary_ga_initialize_population(population_size, dimensions):
    population = []
    for i in range(population_size):
        individual = {}
        individual["phenotype"] = initialize_phenotype(dimensions)
        individual["genotype"] = binary_ga_phenotye_to_genotype(phenotype)
        population.append(individual)
        
    return population



'''Fitness Score:
1. Convert to binary representation (genotype) to 10 floating point numbers (phenotype).
2. Apply the objective function (shifted sphere).
3. If the objective function is a maximization problem, you have a fitness score. If it is a minimization problem, you have to convert it to a fitness score.

For the decimal case,

1. Genotype and phenotype are identical.
2. Apply the objective function (shifted sphere).
3. If the objective function is a maximization problem, you have a fitness score. If it is a minimization problem, you have to convert it to a fitness score.

The fitness function is only defined in terms of the phenotype. You must provide a decoding function to translate between genotype and phenotype. This is "just like" the real world...you have genes, they are expressed as hands, eyes, eye color, height, etc...and those interact with the world...not the genes.

Also make sure to remember that you may have to translate the objective function into a fitness function as well. GA's "only" do maximization.
'''
def calculate_fitness(individual):
    phenotype = individual["phenotype"]
    sphere_value = sphere(0.5, phenotype)
    fitness = minimization_fitness(sphere_value)    
    individual["fitness"] = fitness
 

#each individual should contain at least fields for its genome and fitness score
#evaluate applies the fitness function to each individual (make sure to transform fitness score)    
def evaluate(population):
    for individual in population:
        individual["fitness"] = calculate_fitness(individual)
    

def select_parent(random_selection):
    max_fitness = float("-inf")
    for individual in random_selection:
        fitness = individual["fitness"]
        if fitness > max_fitness:
            max_fitness = fitness
            max_parent = individual
            
    return max_parent
    
    
    
#There are many ways to pick parents - two options:
    #Roulette wheel: each individual's fitness is a proportion of total fitness (more in notes)
    #Tournament selection: pick 7 (or so) completely (uniformly) at random, choose one with highest fitness
#Ensures parent 1 and 2 are different by removing parent 1 from randomly 7 selected values for parent 2, if there
def select_parents_tournament_selection(population):
    population_copy = copy.deepcopy(population)     ##TODO may not need to copy
    random.shuffle(population_copy)
    random_selection = population_copy[0:7]
    parent1 = select_parent(random_selection)
    
    random.shuffle(population_copy)
    random_selection = population_copy[0:7]
    if parent1 in random_selection:
        random_selection.remove(parent1)
    parent2 = select_parent(random_selection)
    
    return parent1, parent2


#randomly pick a mutation site, randomly pick a mutation
def mutate(child):
    pass


def reproduce(parent1, parent2, crossover_rate, mutation_rate):
    crossover_chance = random.uniform(0, 1)
    if crossover_chance > crossover_rate:
        return parent1, parent2
        
    child1, child2 = crossover(parent1, parent2)
    
    child1_mutation_chance = random.uniform(0, 1)
    if child1_mutation_chance < crossover_rate:
        child1 = mutate(child1)
        
    child2_mutation_chance = random.uniform(0, 1)
    if child2_mutation_chance < crossover_rate:
        child2 = mutate(child1)
    
    return child1, child2
    

#Create a population, evaluate it, select parents, apply crossover and mutation, repeat until the number of desired generations have been generated
#Use higher order functions
#Print out the best individual of each generation including the generation number, 
    #genotype (the representation), phenotype (the actual value), the fitness (based on your fitness function transformation) 
    #and the function value (for the shifted sphere) if passed a DEBUG=True flag.
#Keep the tracing limited - print the best individual of the population every i generations (e.g. every 10) 
    #should see about 50 lines of tracing to show the best individual and their fitness
def genetic_algorithm(parameters, initialize_population, crossover, mutate):
    population_size = parameters["population_size"]
    population = initialize_population(population_size, parameters["dimensions"])
    
    generations = 0
    while generations < parameters["number_of_generations"]:
        evaluate(population)  #each individual gets a fitness score before we go to pick parents
        next_population = []
        
        for i in range(population_size / 2):
            parent1, parent2 = select_parents_tournament_selection(population)
            child1, child2 = reproduce(parent1, parent2, parameters["crossover_rate"], parameters["mutation_rate"])
            
            #TODO is this right, or replace??
            next_population.append(child1)
            next_population.append(child2)
            
        population = next_population #always replace the entire population with a new population
        generations += 1
        
    #return the best individual ever encountered (and all their data including genotype, phenotype, fitness, and actual objective function value)
  

def binary_ga(parameters):
    genetic_algorithm(parameters, binary_ga_initialize_population, binary_ga_crossover, binary_ga_mutate)
    
     
    
def real_ga(parameters):
    pass



def sphere( shift, xs):
    return sum( [(x - shift)**2 for x in xs])

sphere( 0.5, [1.0, 2.0, -3.4, 5.0, -1.2, 3.23, 2.87, -4.23, 3.82, -4.61])


#There is some trade off between population size and generations (parameters to experiment with)
#Should not take long at all to converge
binary_ga_parameters = {
   "f": lambda xs: sphere( 0.5, xs),
   "minimization": True,
   "mutation_rate": mutation rate, 
   "crossover_rate": crossover rate, 
   "population_size": 500, #50-500s of individuals
   "dimensions": 10, # (given for this problem), 
   "number_of_generations": 100,  #TODO play with this
   "minimization_fitness_function": minimization_fitness
   # put other parameters in here.
}



binary_ga(parameters)


'''Fitness Score:
1. Convert to binary representation (genotype) to 10 floating point numbers (phenotype).
2. Apply the objective function (shifted sphere).
3. If the objective function is a maximization problem, you have a fitness score. If it is a minimization problem, you have to convert it to a fitness score.

For the decimal case,

1. Genotype and phenotype are identical.
2. Apply the objective function (shifted sphere).
3. If the objective function is a maximization problem, you have a fitness score. If it is a minimization problem, you have to convert it to a fitness score.

The fitness function is only defined in terms of the phenotype. You must provide a decoding function to translate between genotype and phenotype. This is "just like" the real world...you have genes, they are expressed as hands, eyes, eye color, height, etc...and those interact with the world...not the genes.

Also make sure to remember that you may have to translate the objective function into a fitness function as well. GA's "only" do maximization.

There's no real answer to "how many generations are enough". In this case you know because you know what the minimum actually is. (You do know, right?) NO I DON'T KNOW
'''















