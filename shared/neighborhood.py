from shared.cost_functions import calculate_schedulabiltiy
from shared.models.task import Task
from shared.models.taskType import TaskType
import random
from functools import reduce

"""

    TODO fix arbitrary numbers !!!!!!!!!!!!!
    TODO number of pss also related to separation requirement 
    TODO SEPARATION!!!! 
    TODO steal from subset 
    TODO multiple polling servers in initial solution

"""

NUM_PS = 0
BUDGET = 1
PERIOD = 2
DEADLINE = 3
SUBSET = 4


# did not have to be a class but naming of polling servers easier this way
# + do not need to pass random generator as argument
class Neighborhood:
    def __init__(self):
        self.rand = random.Random()
        self.n_polling_servers = 0

    # hardcode mins and max duration,period, deadline for now
    def create_random_ps(self, et_subset):
        # try like this bc hyperperiod thing if very long we visit very few solutions 
        # periods = [1000, 2000,3000,4000]
        # period = periods[rand.randint(0,len(periods)-1)]
        # deadline = max(period, (rand.randint(1, 40) * 100)) # deadline <= period

        # TODO try without prime numbers !!
        # period = self.rand.choice([2, 4, 8]) * self.rand.choice([1, 3]) * self.rand.choice([5, 25])
        server_list = []
        for task in et_subset:

            period = self.rand.randint(1, 20) * 10  # multiple of 10 to avoid hyperperiod exploding??
            deadline = max(period, (self.rand.randint(1, 20) * 10))
            duration = min(self.rand.randint(1, 50), deadline)  # this seems like cheating hardcoding range
            if task.separation not in [ps.separation for ps in server_list]:
                server_list.append(Task("tTTps" + str(task.separation), duration, period, TaskType.TIME, 7, deadline, [task], task.separation))
            else:
                server_list[task.separation].et_subset.append(task)
        # find naming scheme,have to b unique, requires counting or sth, some state
        return server_list
    
    # not even guaranteed to return...
    def create_random_schedulable_ps(self, et_subset):

        is_schedulable = False
        while not is_schedulable:
            is_schedulable = True
            ps = self.create_random_ps(et_subset)
            d = calculate_schedulabiltiy(ps)
            is_schedulable = is_schedulable and reduce((lambda a, b: a and b), [d[key][0] for key in d])

        ps.et_subset = et_subset
        return ps

    # hardcode mins and max duration,period, deadline for now
    def create_random_ps1(self, et_subset):
        # TODO try without prime numbers !!
        # period = self.rand.choice([2, 4, 8]) * self.rand.choice([1, 3]) * self.rand.choice([5, 25])
        period = self.rand.randint(1, 20) * 10  # multiple of 10 to avoid hyperperiod exploding??
        deadline = min(period, (self.rand.randint(1, 20) * 10)) # do not allow deadline > period 
        duration = min(self.rand.randint(1, 50), deadline)  # this seems like cheating hardcoding range

        # naming of polling servers must be unique 
        self.n_polling_servers += 1

        # find naming scheme,have to b unique, requires counting or sth, some state 
        return Task("tTTps" + str(self.n_polling_servers), duration, period, TaskType.TIME, 7, deadline, et_subset)

    def partition_et_tasks(self, n, et_tasks):
        num_tasks = int(len(et_tasks)/n)
        polling_servers = [et_tasks[i*num_tasks:(i+1)*num_tasks] for i in range(n-1)] 
        polling_servers += [et_tasks[(n-1)*num_tasks:]]

        return  polling_servers 

    def create_n_random_ps(self, n, et_tasks):
        # consider
        et_subsets = self.partition_et_tasks(n, et_tasks)
        return [self.create_random_ps1(et_subset) for et_subset in et_subsets]


    # get a subset of pses from victim and delete these from victim 
    def create_ps_subset(self, victim_ps):
        num_et_tasks = self.rand.randint(1, max(1, len(victim_ps.et_subset) - 1))
        new_ps_et_subset = []

        for task in victim_ps.et_subset[0:num_et_tasks]:
            new_ps_et_subset.append(task)

        # do not know how removing and iterating at same time works so do like this 
        for task in victim_ps.et_subset[0:num_et_tasks]:
            victim_ps.et_subset.remove(task)

        return new_ps_et_subset

        # move the polling server subset from one ps to another

    def merge_ps_subsets(self, ps_giver, ps_receiver):
        ps_receiver.et_subset += ps_giver.et_subset

        # take polling servers as arg, lists are mutable and passed by reference

    def get_neighbor(self, polling_servers):
        # num_ps, period, budget, deadline, subset

        # select parameter to change. we rarely generate feasible solutions when including NUM_PS option
        parameter = self.rand.randint(NUM_PS, SUBSET)

        # select polling server to operate on 
        victim_ps = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

        # increase or decrease chosen parameter
        sign = 1 if self.rand.randint(0, 1) == 0 else -1

        # an argument for doing this is that sometimes we need a big difference to get far neighbor, avoid being stuck?
        steps = [1, 5, 10, 100]
        step = steps[self.rand.randint(1, len(steps) - 1)]

        # if sign positive add a polling server if negative remove one 
        # when adding a polling server take some et tasks from victim
        if False: # TODO refactor PS neighbour function
        #if parameter == NUM_PS:
            if sign == 1 and len(
                    polling_servers) < 7:  # TODO find some way to determine max num polling servers or if we should even have
                # print("adding polling server")
                new_et_subset = self.create_ps_subset(victim_ps)
                new_ps = self.create_random_ps1(new_et_subset)
                polling_servers.append(new_ps)

                # remove victim from task set if it does not have any et tasks  
                if victim_ps.et_subset == []:
                    polling_servers.remove(victim_ps)

            else:
                if len(polling_servers) > 1:  # do not make set of polling servers empty
                    # print("removing polling server")
                    receiver_ps = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

                    while receiver_ps == victim_ps:  # select a different ps than victim
                        receiver_ps = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

                    self.merge_ps_subsets(victim_ps, receiver_ps)  # transfer et tasks to other ps

                    polling_servers.remove(victim_ps)  # remove victim from set of polling servers

        elif parameter == BUDGET:  # change budget of victim
            # victim_ps.duration = max(1, victim_ps.duration + sign * self.rand.randint(1,50))
            victim_ps.duration = max(1, victim_ps.duration + sign)
            victim_ps.duration = min(victim_ps.duration, victim_ps.deadline)  # do not accept duration > deadline

        # we add/subtract sum number divisible by 10 and <= 100
        elif parameter == PERIOD:  # change period of victim. we do not accept period < deadline, but we could also just let sa handle it
            # victim_ps.period = max(5, victim_ps.period + sign * self.rand.randint(1,100))
            victim_ps.period = max(1, victim_ps.period + sign * step)
            victim_ps.period = max(victim_ps.period, victim_ps.deadline)  # do not accept period < deadline for now

        elif parameter == DEADLINE:  # change deadline of victim
            # victim_ps.deadline = max(5, victim_ps.deadline + sign * self.rand.randint(1,100))
            victim_ps.deadline = max(1, victim_ps.deadline + sign * step)
            victim_ps.deadline = min(victim_ps.period, victim_ps.deadline)  # do not accept period < deadline for now

        # not confident that it works  
        elif parameter == SUBSET:  # move et tasks from one ps to another
            if len(polling_servers) == 1:  # if no one to steal from
                return polling_servers

            other_ps_victim = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

            while other_ps_victim == victim_ps:
                other_ps_victim = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

            # get some et tasks from other ps victim, delete these from this ps    
            new_ps_et_subset = self.create_ps_subset(other_ps_victim)

            # remove other victim from task set if it does not have any et tasks  
            if other_ps_victim.et_subset == []:
                polling_servers.remove(other_ps_victim)

                # add et tasks to victim ps
            victim_ps.et_subset += new_ps_et_subset

        return polling_servers


"""
    QUESTIONS:
        neighborhood different approaches 
        cost make sense??? ok but consider this other approach
        random initial configuration
        
        
        
        separation requirement: same value same ps, no other value on this ps except 0?
                                may we have multiple ps on same ps or must they be on same??
                                or just no two different values on same?
                                should we generate solutions that do not meet this criterium
                                and just penalize them? or simply not generate such solutions?

            emjn@dtu.dk
            se

            do not consider solutions that do not meet separation criteria! 




"""
