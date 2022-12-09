import copy

from numpy.random import randint, rand

from simulated_annealing.caseLoader import CaseLoader
from simulated_annealing.cost_functions import cost_f
from simulated_annealing.neighborhood import Neighborhood
from simulated_annealing.taskType import TaskType

max_number_of_polling_servers = 10


# tournament selection
def selection(pop_scores, k=3):
    # first random selection
    selection_ix = randint(len(pop_scores))

    for ix in randint(0, len(pop_scores), k - 1):
        # check if better (e.g. perform a tournament)
        if pop_scores[ix][1] < pop_scores[selection_ix][1]:
            selection_ix = ix

    return pop_scores[selection_ix]


# mutation operator
def mutation(obj, r_mut):
    for attr, value in obj.__dict__.items():
        # do mutation if rand less then r_mut
        if attr == "duration" or attr == "period" or attr == "deadline":
            if rand() < r_mut:
                p = randint(-1, 1)
                setattr(obj, attr, int(value) + (1 * p))


def list_to_task(l, obj):
    for idx, ele in enumerate(l):
        if idx == 0:
            obj.duration = ele
        elif idx == 1:
            obj.period = ele
        else:
            obj.deadline = ele

    return obj


def crossover(p1, p2, r_cross):
    p = randint(1, 4)

    c1, c2 = copy.deepcopy(p1[0]), copy.deepcopy(p2[0])

    l1 = list(vars(p1[0]).values())
    l2 = list(vars(p2[0]).values())

    if rand() < r_cross:

        if p == 1:
            return list_to_task([l1[1], l1[2], l2[5]], c1), list_to_task([l2[1], l2[2], l1[5]], c2)
        if p == 2:
            return list_to_task([l1[1], l2[2], l2[5]], c1), list_to_task([l2[1], l1[2], l1[5]], c2)
        if p == 3:
            return list_to_task([l1[1], l2[2], l1[5]], c1), list_to_task([l2[1], l1[2], l2[5]], c2)
    else:
        return c1, c2


def create_pop(population_size, task_set):
    population = []

    neighborhood = Neighborhood()

    tt_tasks = [t for t in task_set if t.type == TaskType.TIME]
    et_tasks = [t for t in task_set if t.type == TaskType.EVENT]

    for x in range(population_size):
        population.append(neighborhood.create_random_ps(copy.deepcopy(et_tasks))[0])

    return population


# genetic algorithm
def genetic_algorithm(task_set, fitness_func, number_of_generations, population_size, crossover_rate,
                      mutation_rate):
    tt_tasks = [t for t in task_set if t.type == TaskType.TIME]

    print("----------------- Initialise population --------------------")
    # Initialise the entire population
    pop = create_pop(population_size, task_set)

    # keep track of best solution

    best, all_solutions = fitness_func(pop, tt_tasks)

    print("Starting best: ", best[1][1])

    # enumerate generations (repeat)
    for gen in range(number_of_generations):
        print("--------------------------- (" + str(gen) + ")-----------------------------")

        # evaluate all candidates in the population
        # scores = [fitness_func(c, init_tt_tasks) for c in pop]
        gen_best, gen_solutions = fitness_func(pop, tt_tasks)

        print("Best of gen (" + str(gen) + "): ", gen_best[1][1])

        if gen_best[1][1] < best[1][1]:
            print(best[1][1], "-->", gen_best[1][1])
            best = gen_best

        selected = [selection(gen_solutions) for _ in range(population_size)]

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

        # always keep det best in the population
        pop.append(best[0])

    return [best]


# fitness function
def cost(population, tt_tasks):
    return [(solution, cost_f(tt_tasks + [solution])) for solution in population]


def eval(population, tt_tasks):
    solutions = cost(population, tt_tasks)
    best = min(solutions, key=lambda t: t[1][1])
    return best, solutions


if __name__ == "__main__":
    neighborhood = Neighborhood()
    # instantiate simulated annealer

    loader = CaseLoader()
    all_tasks = loader.load_test_case("inf_10_10", 0, filePath="../test_cases/")

    tt_tasks = [t for t in all_tasks if t.type == TaskType.TIME]
    et_tasks = [t for t in all_tasks if t.type == TaskType.EVENT]

    # polling_servers_0 = [neighborhood.create_random_ps(et_tasks)]

    # task_set = tt_tasks + polling_servers_0

    # define the total iterations
    n_iter = 50
    # bits
    n_bits = 2
    # define the population size
    n_pop = 50
    # crossover rate
    r_cross = 0.7
    # mutation rate
    r_mut = 0.2

    # perform the genetic algorithm search
    best = genetic_algorithm(all_tasks, eval, n_iter, n_pop, r_cross, r_mut)

    print('Done!')
    print("Best: ", best[0][1][1])
