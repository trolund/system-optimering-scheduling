import sys
sys.path.insert(1, '../')
from numpy.random import randint, random_sample # remember numpy randint is [a, b), meaning excluding b
from random import shuffle
from shared.caseLoader import CaseLoader
from shared.models.taskType import TaskType
from shared.models.task import Task
from shared.cost_functions import cost_f
from shared.neighborhood import Neighborhood
from sympy import isprime 
import concurrent.futures
import time
from os import cpu_count
from itertools import repeat

# Do not consider multiple polling servers 
# represent a solution (a polling server) as [duration, period, deadline]
# do 1 point crossover 
# create 2nd ctor for task taking such a list - use for getting cost

DURATION = 0
PERIOD = 1
DEADLINE = 2

# TODO: terminate when n genrations or all members of population is same i.e. population has converged 
# TODO: threads when generating and evaluating solutions. really just evaluating this is the most time consuming
# TODO: try instantiating solutions as in sa and mutating as in sa
# TODO: check solution after crossover and mating -> bias discussed in modern heuristics p. 158
# TODO: try with num threads = size of population
# TODO: try context manager 
# TODO: find out what % of execution time we spend in objective function would be nice for report maybe
# 20*10 and steps seems to make evaluating solutions better.... 
  
# generate a solution
def create_solution():
    period = randint(1, 20) * 10
    #period = randint(1, 500)
    while isprime(period): # avoid explosion of hyper period? and enforce period >= deadline 
        period = randint(1, 20) * 10
        #period = randint(1, 500)

    deadline = randint(1, period + 1) # set deadline to some random int <= period

    duration = randint(1, deadline + 1)    
 
    return [duration, period, deadline] # representation of a solution 

def create_population(population_size): 
    return [create_solution() for _ in range(population_size)]

def to_task(solution, et_set):
    # decide whether we want to uniquely name these. we only use task class to evaluate but none the less
    return Task("tTTps", solution[DURATION], solution[PERIOD], TaskType.TIME, 7, solution[DEADLINE], et_set)

# get cost of each solution in population
def evaluate_population(population, tt_task_set, et_task_set):
    return [[solution, cost_f(tt_task_set + [to_task(solution, et_task_set)])] for solution in population] 

# tournament selection, compete k-1 other solutions 
def selection(pop_and_costs, k=3): 
    #print(pop_and_costs[0][1][1]) 
    # first random selection
    selection_ix = randint(len(pop_and_costs))
    #print("in selection")
    #print("population is: ")
    #for i in range(len(pop_and_costs)):
    #    print(pop_and_costs[i][0])
    #print("pop[selection_ix]: ", pop_and_costs[selection_ix][0])
    for ix in randint(0, len(pop_and_costs), k - 1):  # k-1 ix generated, all between 0 and lengh of scores
        # check if better ('cheaper')
        #print("pop[ix]: ", pop_and_costs[ix][0])
        if pop_and_costs[ix][1][1] < pop_and_costs[selection_ix][1][1]:
            selection_ix = ix

    # pop_and_costs is list of [solution, (return value from cost_f)]    
    return pop_and_costs[selection_ix][0]


# check and "fix" solution in order to not generate too many infeasible solutions. many infeasible solutions generated anyway
def check_solution(solution): 
    sign = 1 if randint(0, 2) == 0 else -1 # increment or decrement till not prime
    while isprime(solution[PERIOD]):
        solution[PERIOD] += sign

    solution[DEADLINE] = min(solution[DEADLINE], solution[PERIOD])
    solution[DURATION] = min(solution[DEADLINE], solution[DURATION]) # minus one to enforce allcaps below??
    
    if solution[DURATION] == solution[PERIOD] == solution[DEADLINE]:
        solution[DURATION] -= 1
    # IF PERIOD == DEADLINE, DURATION MAY NOT ALSO == DEADLINE 
    # list is mutable and pass by reference etc -- we do not have to return solution

# mutation operator. hardcoded for this problem and representation of problem... well ... 
def mutate(solution, r_mut):
    sign = 1 if randint(0, 2) == 0 else -1
    #print("in mutate. solution is: ", solution)

    steps = [1, 5, 10, 10, 10, 10]
    for i in range(len(solution)):
        # check for a mutation
        if random_sample() < r_mut:
            #print("boing")
            # mutate solution
            #solution[i] = max(1, solution[i] + sign * randint(1, 50))
            
            solution[i] = max(1, solution[i] + sign * steps[randint(1, len(steps)-1)])
            # consider just calling check solution but worried this degrades things to random search
            if i == PERIOD and isprime(solution[i]): 
                solution[i] += sign # 2 3 prime and adjacent but ok
    #check_solution(solution)

# a bit of freestyling but we use one of three possible crossovers here
# so we have one or two crossover points but fine fine 
# l1[0] + l1[1] + l2[2],  l2[0] + l2[1] + l1[2]
# l1[0] + l2[1] + l2[2], l2[0] + l1[1] + l1[2]   
# l1[0] + l2[1] + l1[2], l2[0] + l1[1] + l2[2]   
def recombine(p1, p2, r_cross):
 
    # check for recombination
    if random_sample() < r_cross:
        # select crossover point 
        pt = randint(0, len(p1))

        # consider slicing but whatever
        if pt == 0:
             p1, p2 = [p1[0]] + [p2[1]] + [p1[2]], [p2[0]] + [p1[1]] + [p2[2]]  
        else:
            p1, p2 = p1[:pt] + p2[pt:], p2[:pt] + p1[pt:] 
    
    # we could just return nothing but conceptually cleaner maybe this 
    return [p1, p2]

# genetic algorithm
def genetic_algorithm(task_set, fitness_func, number_of_generations, population_size, crossover_rate,
                      mutation_rate):
     
    tt_tasks = [t for t in task_set if t.type == TaskType.TIME]
    et_tasks = [t for t in task_set if t.type == TaskType.EVENT]
    
    # Initialise the entire population
    population = create_population(population_size)

    # create pool and keep it to minimize overhead of creating threads 
    #pool = concurrent.futures.ThreadPoolExecutor(cpu_count()) # do not use "with" bc we want to hold on to pool
    #pool = concurrent.futures.ThreadPoolExecutor(population_size) # do not use "with" bc we want to hold on to pool
    t0 = time.time()
    
    # keep track of best solution. TODO only if schedulable? or just rely on penalty and many generations. could get min in same function but ok two iterations
    #pop_and_costs = [fitness_func(solution, tt_tasks, et_tasks) for solution in population]
    pop_and_costs = [] 
    #for result in pool.map(fitness_func, population, repeat(tt_tasks), repeat(et_tasks)):
    #        pop_and_costs.append(result) 

    with concurrent.futures.ThreadPoolExecutor(cpu_count()) as executor:
        for result in executor.map(fitness_func, population, repeat(tt_tasks), repeat(et_tasks)):
            pop_and_costs.append(result)

    best_solution = min(pop_and_costs, key=lambda t: t[1][1]) # index 1 is tuple, index 1 of tuple is cost 
    
    # enumerate generations (repeat)
    for gen in range(number_of_generations): 
        print("gen is: ", gen)
        print("population is: ", population)
        print("best cost: ", best_solution[1][1], best_solution[1][2])   
        for p in pop_and_costs:
            print("\t", p[1][1], p[1][2])
         
        mating_pool = [selection(pop_and_costs) for _ in range(population_size)]
        population = [] # we can reset population at this point its ok 
        shuffle(mating_pool)
        #population.append(best_solution[0]) # always let best solution pass try?? pop of size size_pop + 1 then... considered again next round ...? 
        
        # recombine, mutate. two individuals handled per iteration
        for i in range(0, population_size, 2):
           population += recombine(mating_pool[i], mating_pool[i+1], crossover_rate) # pop must be of even number size
           mutate(population[i], mutation_rate)
           mutate(population[i+1], mutation_rate)
           check_solution(population[i]) # removeeee
           check_solution(population[i+1]) 
        
        pop_and_costs = []

        #pop_and_costs = [fitness_func(solution, tt_tasks, et_tasks) for solution in population]
        # https://docs.python.org/3/library/concurrent.futures.html 
        # https://stackoverflow.com/questions/20838162/how-does-threadpoolexecutor-map-differ-from-threadpoolexecutor-submit 
        # use pool but when this with is inside loop do we create pool on each it or is one kept?
        # few threads and chunks or thread per solution?

        # should block 
        #for result in pool.map(fitness_func, population, repeat(tt_tasks), repeat(et_tasks)):
        #    pop_and_costs.append(result)
            #print("boing") 
        
        with concurrent.futures.ThreadPoolExecutor(cpu_count()) as executor:
            for result in executor.map(fitness_func, population, repeat(tt_tasks), repeat(et_tasks)):
                pop_and_costs.append(result)
        
        tmp_best_solution = min(pop_and_costs, key=lambda t: t[1][1]) # index 1 is tuple, index 1 of tuple is cost 
        # keep track of best solution. TODO only if schedulable? or just rely on penalty and many generations 
        if tmp_best_solution[1][1] < best_solution[1][1]:
            best_solution = tmp_best_solution

        # replace worst with best a couple of times 
        for i in range(2):
            worst_solution = max(pop_and_costs, key=lambda t: t[1][1]) # index 1 is tuple, index 1 of tuple is cost 
            pop_and_costs.remove(worst_solution)
            pop_and_costs.append(best_solution)

    #pool.shutdown()
    print("seconds: ", time.time() - t0)
    return [best_solution, (time.time() - t0)]
        
# fitness function applied to list of solutions
def cost_list(population, tt_tasks, et_tasks):
    return [[solution, cost_f(tt_tasks + [to_task(solution, et_tasks)])] for solution in population]

# apply to one solution
def cost(solution, tt_tasks, et_tasks):
    return [solution, cost_f(tt_tasks + [to_task(solution, et_tasks)])]

def eval(population, tt_tasks):
    return min(cost(population, tt_tasks), key=lambda t: t[1])


if __name__ == "__main__":
    loader = CaseLoader()
    all_tasks = loader.load_test_case("inf_40_20", 30, filePath="../test_cases/") 
     
    tt_tasks = [t for t in all_tasks if t.type == TaskType.TIME]
    et_tasks = [t for t in all_tasks if t.type == TaskType.EVENT]

    # define the total iterations
    n_iter = 15
    # bits
    n_bits = 20
    # define the population size
    n_pop = 26
    # crossover rate
    r_cross = 0.9
    # mutation rate
    r_mut = 1/3

    # perform the genetic algorithm search
    results = [genetic_algorithm(all_tasks, cost, n_iter, n_pop, r_cross, r_mut) for _ in range(2)]
    sum_t = 0
    sum_cost = 0

    for i in range(len(results)):
        t = results[i][1]
        sum_t += t
        #sum_cost += c

    print("avg t: ", sum_t / len(results))
    #print("avg costs: ", sum_cost / len(results))


    #print('Done!')
    #print('f(%s) = %f' % (best[0], best[1][1]))
    #print("is schedulable: ", best[1][2])
