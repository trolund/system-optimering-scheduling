from asyncore import poll
from task import Task
from caseLoader import CaseLoader
from taskType import TaskType
from simulated_annealer import SimulatedAnnealer
from neighborhood import Neighborhood
from cost_functions import *
import sys 
import matplotlib.pyplot as plt 
import numpy as np 

def usage(argv):
    print("python3.9 ", argv[0], " [-l/--log <filename>] <inf_X_Y N> <temperature0> <alpha> <stopcriterion_sec>", )
    print("--log/-l <filename>: log solutions and save plot of costs save as <filename>")


def generate_plot(cost_log, best_cost, filename, test_case):
    fig, ax = plt.subplots()
    ax.plot(np.arange(len(cost_log)), cost_log)
    fig.set_size_inches(18.5, 10.5)
    plt.axhline(y = best_cost, color = 'r', linestyle = '-', label="Best cost")
    plt.title("Costs " + test_case[0] + " " + str(test_case[1]))
    plt.xlabel("Solution number")
    plt.ylabel("Cost")
    ax.legend()
    fig.set_dpi(300)
    plt.savefig(filename)

def print_best_ps_config(best_ps_config):
    print("Best polling server configuration: ")
    for polling_server in best_ps_config:
        print("\tName: ", polling_server.name, " Duration: ", polling_server.duration, " Period: ", polling_server.period, " Deadline: ", polling_server.deadline)
        for et in polling_server.et_subset:
            print("\t\tName: ", et.name)
        # add print ets for each ps 


if __name__ == "__main__":
    if len(sys.argv) < 6:
        usage(sys.argv)
        sys.exit(0)
    
    is_logging = False

    # get commandline arguments
    if sys.argv[1] == "-l" or sys.argv[1] == "--log":
        filename = sys.argv[2]
        test_case = [sys.argv[3], int(sys.argv[4])]
        temperature = float(sys.argv[5])
        alpha = float(sys.argv[6])
        stopcriterion_sec = float(sys.argv[7])
        is_logging = True
    else:
        test_case = [sys.argv[1], int(sys.argv[2])]
        temperature = float(sys.argv[3])
        alpha = float(sys.argv[4])
        stopcriterion_sec = float(sys.argv[5])

    neighborhood = Neighborhood() 
    # instantiate simulated annealer
    simulated_annealer = SimulatedAnnealer(neighborhood)

    loader = CaseLoader()
    all_tasks = loader.load_test_case(test_case[0], test_case[1])
    tt_tasks = [t for t in all_tasks if t.type == TaskType.TIME]
    et_tasks = [t for t in all_tasks if t.type == TaskType.EVENT]

    # generates good solution for many cases, but should be random
    polling_servers_0 = [Task("tTTps00", 500, 1000, TaskType.TIME, 7, 1000, et_tasks)]
    
    #polling_servers_0 = [neighborhood.create_random_ps(et_tasks)]


    task_set = tt_tasks + polling_servers_0

    simulated_annealer.sa(task_set, temperature, alpha, stopcriterion_sec, cost_f=cost_f, log_costs=True)

    print_best_ps_config(simulated_annealer.get_best_ps_config())

    if is_logging:
        generate_plot(simulated_annealer.get_cost_log(), simulated_annealer.get_best_cost(), filename, test_case)

    