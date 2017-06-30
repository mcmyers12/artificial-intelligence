from IPython.core.display import *
from StringIO import StringIO



#Transform the fitness score for minimization
def minimization_fitness(fitness_score):
    return 1 / (1 + fitness_score)


#generate n random individuals according to the encoding scheme, the genetic code
def generate_random_population(n):
    pass
    

#each individual should contain at least fields for its genome and fitness score
#evaluate applies the fitness function to each individual (make sure to transform fitness score)    
def evaluate(population):
    pass




def binary_ga(parameters):
    population = generate_random_population(parameters["population_size"])
    
    generations = 0
    while generations < parameters["number_of_generations"]:
        evaluate(population)

  
  
  
  
    
def real_ga(parameters):
    pass



def sphere( shift, xs):
    return sum( [(x - shift)**2 for x in xs])

sphere( 0.5, [1.0, 2.0, -3.4, 5.0, -1.2, 3.23, 2.87, -4.23, 3.82, -4.61])



parameters = {
   "f": lambda xs: sphere( 0.5, xs),
   "minimization": True,
   "mutation_rate": mutation rate, 
   "crossover_rate": crossover rate, 
   "population_size": population size, 
   "dimensions": dimensions, # (given for this problem), 
   "number_of_generations": number of generations,
   "minimization_fitness_function": minimization_fitness
   # put other parameters in here.
}