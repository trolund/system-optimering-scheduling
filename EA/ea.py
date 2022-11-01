from numpy.random import randint, rand

from mess.taskType import TaskType
from sa_scheduling.cost_functions import cost_f
from sa_scheduling.neighborhood import Neighborhood

max_number_of_polling_servers = 10


# tournament selection
def selection(pop, scores, k=3):
    # first random selection
    selection_ix = randint(len(pop))

    for ix in randint(0, len(pop), k - 1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix

    return pop[selection_ix]


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


def create_pop(population_size, task_set):
    population = []

    neighborhood = Neighborhood()

    tt_tasks = [t for t in task_set if t.type == TaskType.TIME]
    et_tasks = [t for t in task_set if t.type == TaskType.EVENT]

    for x in range(population_size):
        population.append(neighborhood.create_random_ps(et_tasks))

    return population


# genetic algorithm
def genetic_algorithm(task_set, fitness_func, number_of_generations, population_size, crossover_rate,
                      mutation_rate):
    tt_tasks = [t for t in task_set if t.type == TaskType.TIME]

    # Initialise the entire population
    pop = create_pop(population_size, task_set)

    # keep track of best solution
    best, best_eval = min(fitness_func(pop, tt_tasks), key=lambda t: t[1])

    # enumerate generations (repeat)
    for gen in range(number_of_generations):
        # evaluate all candidates in the population
        # scores = [fitness_func(c, init_tt_tasks) for c in pop]
        scores = fitness_func(pop, tt_tasks)
        # check for new best solution
        for i in range(population_size):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen, pop[i], scores[i]))
        # select parents
        selected = [selection(pop, scores) for _ in range(population_size)]
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
    return [best, best_eval]


# fitness function
def cost(population, tt_tasks):
    return [(solution, cost_f(tt_tasks + solution)) for solution in population]


def eval(population, tt_tasks):
    return min(cost(population, tt_tasks), key=lambda t: t[1])





if __name__ == "__main__":
    # define the total iterations
    n_iter = 100
    # bits
    n_bits = 20
    # define the population size
    n_pop = 100
    # crossover rate
    r_cross = 0.9
    # mutation rate
    r_mut = 1.0 / float(n_bits)

    # perform the genetic algorithm search
    best, score = genetic_algorithm(cost, n_bits, n_iter, n_pop, r_cross, r_mut)

    print('Done!')
    print('f(%s) = %f' % (best, score))
