import copy
import random
import time

import numpy as np

from shared.models.taskType import TaskType


class SimulatedAnnealer:

    # give neighborhood as member??
    def __init__(self, neighborhood):
        self.neighborhood = neighborhood
        self.rand = random.Random()
        self.n_solutions = 0
        self.cost_log = []
        self.best_solution = []
        self.best_ps_config = []
        self.best_cost = 0

    def reset(self):
        self.n_solutions = 0 
        self.cost_log = []
        self.best_solution = []
        self.best_ps_config = []
        self.best_cost = 0

    def get_neighbor(self, polling_servers):
        return self.neighborhood.get_neighbor(polling_servers)

    def p(self, delta, t):
        return np.exp( -delta / t )

    # simulated annealing 
    def sa(self, s0, t, a, stopcriterion_sec, cost_f=None, log_costs = False):
        # reset part of state 
        self.reset()

        # used for checking stop criterion
        sec0 = int(time.time())

        # get tt and et tasks
        tt = [t for t in s0 if t.type == TaskType.TIME and t.et_subset == None] 
        polling_servers = [t for t in s0 if t.et_subset != None]
        
        # current and best solution
        current_solution = tt + polling_servers
        schedule, current_cost, is_schedulable = cost_f(current_solution)
        self.best_solution = copy.deepcopy(current_solution)
        best_cost = current_cost
        self.best_cost = current_cost
        self.best_ps_config = polling_servers
         
        # for logging purposes
        self.n_solutions = 0
        self.cost_log = []
        if log_costs: # logging
            self.cost_log.append(current_cost)    

        print("cost0: ", current_cost, " t: ", t, " is schedulable: ", is_schedulable)

        # does not matter if < or <= if 0 then new solution will be selected no matter what     
        while int(time.time()) - sec0 < stopcriterion_sec: 
            tmp_ps = self.get_neighbor(copy.deepcopy(polling_servers)) # obtain ps configuration from neighborhood
            tmp_solution = tt + tmp_ps # complete task set  
             
            tmp_schedule, tmp_cost, is_schedulable = cost_f(tmp_solution) # apply objective function

            pss = [t for t in tmp_solution if t.et_subset != None]
            #print(len(pss))

            # compute delta
            delta = tmp_cost - current_cost
         
            # some logging     
            if delta > 0:
                print("cost: ", tmp_cost, f" delta: {delta:.10f}", f" t: {t:.10f}", f" p(delta, t): {self.p(delta, t):.10f}", " is schedulable: ", is_schedulable, " num_ps: ", len(pss))
            else:
                print("cost: ", tmp_cost, " delta: ", delta, " t: ", t, " is schedulable: ", is_schedulable, " num ps: ", len(pss))
                 
            # accept randomly drawn solution from current neighborhood if better or with some probability
            if delta <= 0 or self.p(delta, t) > self.rand.uniform(0.0, 1.0): 
                polling_servers = copy.deepcopy(tmp_ps) # all these copies...
                current_solution = tmp_solution # update current solution, current set of polling servers, costs & schedule
                current_cost = tmp_cost
                schedule = tmp_schedule[:] 
                            
                if log_costs: # logging
                    self.cost_log.append(current_cost)
                
                # keep track of the best solution. save all the things..
                if current_cost < best_cost and is_schedulable:
                    self.best_solution = current_solution
                    self.best_schedule = schedule[:]
                    self.best_cost = current_cost
                    best_cost = current_cost # not so clean having best cost and self.best_cost ...
                    self.best_ps_config = copy.deepcopy(polling_servers)
                    
                    # log to prompt
                    #print("*************************************************")
                    print("************* updated best solution *************")
                    #print("*************************************************")

            # logging
            self.n_solutions = self.n_solutions + 1

            # update temperature 
            t = t * a 
 
        self.print_message(stopcriterion_sec)        
        #return (schedule, best_cost, self.best_ps_config) 

    def print_message(self, stopcriterion_sec):
        print("\n")
        print("ran for ", stopcriterion_sec, " seconds")
        print("number of generated solutions: ", self.n_solutions)
        print("number of visited solutions: ", len(self.cost_log))
    
    def print_n_solutions(self):
        print("Total generated solutions: ", self.n_solutions)
        print("Visited solutions:         ", len(self.cost_log))

    # some getters 
    def get_cost_log(self):
        return self.cost_log

    def get_best_solution(self):
        return self.best_solution

    def get_best_schedule(self):
        return self.best_solution

    def get_best_cost(self):
        return self.best_cost

    def get_best_ps_config(self):
        return self.best_ps_config 