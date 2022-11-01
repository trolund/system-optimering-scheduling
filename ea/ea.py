import sys
sys.path.insert(1, '../')
from numpy.random import randint, rand
from random import shuffle
from shared.caseLoader import CaseLoader
from shared.models.taskType import TaskType
from shared.cost_functions import cost_f
from shared.neighborhood import Neighborhood
from copy import deepcopy

max_number_of_polling_servers = 10


# tournament selection, compete k-1 other solutions 
def selection(scores, k=3):
    
    # first random selection
    selection_ix = randint(len(scores))
 
    for ix in randint(0, len(scores), k - 1):  # k-1 ix generated, all between 0 and lengh of scores
        # check if better 
        if scores[ix][1][1] < scores[selection_ix][1][1]:
            selection_ix = ix
    
    return scores[selection_ix][0]

# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]

def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # check for recombination
    if rand() < r_cross:
        # select crossover point that is not on the end of the string
        pt = randint(1, len(p1) - 2)
        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]

def recombine(parent_1, parent_2, r_cross):
    # children are copies of parents by default
    child_1, child_2 = deepcopy(parent_1), deepcopy(parent_2)
    # check for recombination
    if rand() < r_cross:
       n_attributes = randint(1, 3)

    return [child_1, child_2]


def create_pop(population_size, task_set):
    population = []

    neighborhood = Neighborhood()

    tt_tasks = [t for t in task_set if t.type == TaskType.TIME]
    et_tasks = [t for t in task_set if t.type == TaskType.EVENT]

    for x in range(population_size):
        population.append(neighborhood.create_random_ps1(et_tasks))

    return population


# genetic algorithm
def genetic_algorithm(task_set, fitness_func, number_of_generations, population_size, crossover_rate,
                      mutation_rate):
     
    tt_tasks = [t for t in task_set if t.type == TaskType.TIME]
    et_tasks = [t for t in task_set if t.type == TaskType.EVENT]
    
    # Initialise the entire population
    pop = create_pop(population_size, task_set)

    # keep track of best solution. TODO only if schedulable
    best, best_eval = min(fitness_func(pop, tt_tasks), key=lambda t: t[1][1]) # index 1 is tuple, index 1 of tuple is cost
    print(best)
    print(best_eval[1:])  
    
    # enumerate generations (repeat)
    for gen in range(number_of_generations):
        # evaluate all candidates in the population
        # scores = [fitness_func(c, init_tt_tasks) for c in pop]
        scores = fitness_func(pop, tt_tasks)
        
        # check if better solution was generated 
        cur_best, cur_best_eval = min(scores, key=lambda t: t[1][1])
        #best, best_eval = (cur_best, cur_best_eval) if cur_best_eval < best_eval else (cur_best, cur_best_eval)
        if cur_best_eval[1] < best_eval[1]:
            best, best_eval = cur_best, cur_best_eval    
            print(">%d, new best f(%s) = %.3f" % (gen, pop[i], scores[i])) 
        
        # select parents
        selected = [selection(scores) for _ in range(population_size)]
        shuffle(selected) # shuffle mating pool
        print(selected) 
        # create the next generation
        children = list()
        
        for i in range(0, population_size, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i + 1]
            
            # crossover and mutation
            for c in crossover(p1, p2, crossover_rate):
                # mutation
                mutation(c, mutation_rate)
                # store for next generation
                children.append(c)
        # replace population
        pop = children
        print(pop)
    return [best, best_eval]


# fitness function
def cost(population, tt_tasks): 
    return [(solution, cost_f(tt_tasks + [solution])) for solution in population]


def eval(population, tt_tasks):
    return min(cost(population, tt_tasks), key=lambda t: t[1])


if __name__ == "__main__":
    neighborhood = Neighborhood()
    # instantiate simulated annealer

    loader = CaseLoader()
    all_tasks = loader.load_test_case("inf_10_10", 0, filePath="../test_cases/") 
     
    tt_tasks = [t for t in all_tasks if t.type == TaskType.TIME]
    et_tasks = [t for t in all_tasks if t.type == TaskType.EVENT]

    #polling_servers_0 = [neighborhood.create_random_ps(et_tasks)]

    #task_set = tt_tasks + polling_servers_0

    # define the total iterations
    n_iter = 100
    # bits
    n_bits = 20
    # define the population size
    n_pop = 10
    # crossover rate
    r_cross = 0.9
    # mutation rate
    r_mut = 1.0 / float(n_bits)

    # perform the genetic algorithm search
    best, score = genetic_algorithm(all_tasks, cost, n_iter, n_pop, r_cross, r_mut)

    print('Done!')
    print('f(%s) = %f' % (best, score))
