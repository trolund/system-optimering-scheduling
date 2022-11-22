from shared.cost_functions import calculate_schedulabiltiy
from shared.models.task import Task
from shared.models.taskType import TaskType
import random
from functools import reduce

"""

    TODO fix arbitrary numbers !!!!!!!!!!!!! seems to be ok -> design choice 
    TODO number of pss also related to separation requirement 
    TODO SEPARATION!!!! working on this and the above
    TODO test everything 
    TODO look into random sampling of set library functions :D lots of homemade stuff here
"""

NUM_PS = 0
BUDGET = 1
PERIOD = 2
DEADLINE = 3
SUBSET = 5
SWAP_SEP = 4


# did not have to be a class but naming of polling servers easier this way
# + do not need to pass random generator as argument
class Neighborhood:
    def __init__(self):
        self.rand = random.Random()
        self.n_polling_servers = 0

    # hardcode mins and max duration,period, deadline for now
    def create_random_ps(self, et_subset):
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

    # return dict m[separation] = list of ets with separation
    def get_separated_ets(self, et_tasks):
        #separations = set([et.separation for et in et_subset])
        # couldnt figure out how to do dict comprehension only iterating once here because key already in check
        ets_separated = {}
        for et in et_tasks: # create map m[separation] = list of ets with separation
            if et.separation not in ets_separated:
                ets_separated[et.separation] = [et]
            else:
                ets_separated[et.separation].append(et)

        return ets_separated#[value for key, value in ps_separated]

    # create random polling servers with separation requirement 
    def create_random_pss_sep(self, et_tasks):
        ets_separated = self.get_separated_ets(et_tasks)

        ets_non_zero = [value for key, value in ets_separated.items() if key != 0]

        # create a random number of partitions of et zero tasks. et_zeros is list of list of ets with sep 0 
        et_zeros = self.partition_et_tasks(random.randint(0, len(ets_non_zero)), ets_separated[0]) if 0 in ets_separated else []


        # create polling servers 
        polling_servers = [self.create_random_ps1(subset + et_zeros.pop()) if et_zeros != [] \
                               else self.create_random_ps1(subset) for subset in ets_non_zero]

        # make sure that separation requirement is fulfilled by every polling server
        for ps in polling_servers:
            if not self.verify_separation_req(ps):
                return -1 # find something to do here, should NOT happen 

        return polling_servers

    # without separation requirement 
    # hardcode mins and max duration,period, deadline for now
    def create_random_ps1(self, et_subset):
        # TODO try without prime numbers !! 
        period = self.rand.randint(1, 20) * 10  # multiple of 10 to avoid hyperperiod exploding??
        deadline = min(period, (self.rand.randint(1, 20) * 10)) # do not allow deadline > period 
        duration = min(self.rand.randint(1, 50), deadline)  # this seems like cheating hardcoding range

        # naming of polling servers must be unique 
        self.n_polling_servers += 1

        # find naming scheme,have to b unique, requires counting or sth, some state 
        return Task("tTTps" + str(self.n_polling_servers), duration, period, TaskType.TIME, 7, deadline, et_subset, et_subset[0].separation)

    # partition list of et_tasks into n lists of et_tasks
    def partition_et_tasks(self, n, et_tasks):
        num_tasks = int(len(et_tasks)/n)
        polling_servers = [et_tasks[i*num_tasks:(i+1)*num_tasks] for i in range(n-1)]
        polling_servers += [et_tasks[(n-1)*num_tasks:]]

        return  polling_servers

        # without separation requirement
    def create_n_random_ps(self, n, et_tasks):
        et_subsets = self.partition_et_tasks(n, et_tasks)
        return [self.create_random_ps1(et_subset) for et_subset in et_subsets]


    # get a subset of pses from victim and delete these from victim 
    def create_ps_subset(self, victim_ps):
        num_et_tasks = self.rand.randint(1, max(1, len(victim_ps.et_subset) - 1)) # doesnt work like this anymore only count 0s
        new_ps_et_subset = []

        for task in victim_ps.et_subset[0:num_et_tasks]:
            if task.separation == 0:
                new_ps_et_subset.append(task)

        # do not know how removing and iterating at same time works so do like this 
        for task in victim_ps.et_subset[0:num_et_tasks]:
            if task.separation == 0:
                victim_ps.et_subset.remove(task)

        return new_ps_et_subset

        # move the polling server subset from one ps to another


    def merge_ps_subsets(self, ps_giver, ps_receiver):
        ps_receiver.et_subset += ps_giver.et_subset

        # take polling servers as arg, lists are mutable and passed by reference

    def get_neighbor(self, polling_servers):
        # num_ps, period, budget, deadline, subset

        # select parameter to change. we rarely generate feasible solutions when including NUM_PS option
        parameter = self.rand.randint(NUM_PS+1, SWAP_SEP)

        # select polling server to operate on
        victim_ps = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

        # increase or decrease chosen parameter
        sign = 1 if self.rand.randint(0, 1) == 0 else -1

        # an argument for doing this is that sometimes we need a big difference to get far neighbor, avoid being stuck?
        steps_period = [10, 10, 20]
        steps_deadline = [1, 2, 5, 10, 10, 10, 20]
        step_p = steps_period[self.rand.randint(0, len(steps_period) - 1)]
        step_d = steps_deadline[self.rand.randint(0, len(steps_deadline) - 1)]

        # if sign positive add a polling server if negative remove one
        # when adding a polling server take some et tasks from victim
        if parameter == NUM_PS:
            self.num_ps(sign, polling_servers, victim_ps, self.rand)

        elif parameter == BUDGET:  # change budget of victim
            self.budget(victim_ps, sign, step_d)

        # we add/subtract sum number divisible by 10 and <= 100
        elif parameter == PERIOD:  # change period of victim. we do not accept period < deadline, but we could also just let sa handle it
            self.period(victim_ps, sign, step_p)

        elif parameter == DEADLINE:  # change deadline of victim
            self.deadline(victim_ps, sign, step_d)

        elif parameter == SUBSET:  # move et tasks from one ps to another
            if len(polling_servers) == 1:  # if no one to steal from
                return polling_servers

            self.subset(polling_servers, victim_ps)

        elif parameter == SWAP_SEP:
            other_ps_victim = self.swap_sep(polling_servers, victim_ps, self.rand)

            self.swap_ets(victim_ps, other_ps_victim)

        return polling_servers

    # moving code in to functions
    # function for parameter NUM_PS
    def num_ps(self, sign, polling_servers, victim_ps, rand):
        if sign == 1 and len(
                polling_servers) < 7:  # TODO find some way to determine max num polling servers or if we should even have
            # print("adding polling server")
            new_et_subset = self.create_ps_subset(victim_ps)
            if len(new_et_subset) != 0:
                new_ps = self.create_random_ps1(new_et_subset)
                polling_servers.append(new_ps)

            # remove victim from task set if it does not have any et tasks
            if victim_ps.et_subset == []:
                polling_servers.remove(victim_ps)
        else:
            if len(polling_servers) > 1:  # do not make set of polling servers empty
                # print("removing polling server")
                receiver_ps = polling_servers[rand.randint(0, len(polling_servers) - 1)]

                while receiver_ps == victim_ps:  # select a different ps than victim
                    receiver_ps = polling_servers[rand.randint(0, len(polling_servers) - 1)]

                victim_separation = [ps.separation for ps in victim_ps if ps.separation != 0]
                receiver_separation = [ps.separation for ps in receiver_ps if ps.separation != 0]
                if len(victim_separation) == 0 or len(receiver_separation) == 0 or victim_separation[0].separation == \
                        receiver_separation[0].separation:
                    self.merge_ps_subsets(victim_ps, receiver_ps)  # transfer et tasks to other ps

                    polling_servers.remove(victim_ps)  # remove victim from set of polling servers

    # function for parameter BUDGET
    def budget(self, victim_ps, sign, step_d):
        # victim_ps.duration = max(1, victim_ps.duration + sign * self.rand.randint(1,50))
        victim_ps.duration = max(1, victim_ps.duration + sign * step_d)
        victim_ps.duration = min(victim_ps.duration, victim_ps.deadline)  # do not accept duration > deadline

    # function for parameter PERIOD
    def period(self, victim_ps, sign, step_p):
        # victim_ps.period = max(5, victim_ps.period + sign * self.rand.randint(1,100))
        victim_ps.period = max(2, victim_ps.period + sign * step_p)
        victim_ps.period = max(victim_ps.period, victim_ps.deadline)  # do not accept period < deadline for now

    # function for parameter DEADLINE
    def deadline(self, victim_ps, sign, step_d):
        # victim_ps.deadline = max(5, victim_ps.deadline + sign * self.rand.randint(1,100))
        victim_ps.deadline = max(1, victim_ps.deadline + sign * step_d)
        victim_ps.deadline = min(victim_ps.period, victim_ps.deadline)  # do not accept period < deadline for now

    # function for parameter SUBSET
    def subset(self, polling_servers, victim_ps):
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

    # function for parameter SWAP_SEP
    def swap_sep(self, polling_servers, victim_ps, rand):
        other_ps_victim = polling_servers[rand.randint(0, len(polling_servers) - 1)]

        while other_ps_victim == victim_ps:
            other_ps_victim = polling_servers[rand.randint(0, len(polling_servers) - 1)]

        return other_ps_victim

    # true if only contains ets of one sep type 
    def verify_separation_req(self, polling_server):
        non_zeros = [et.separation for et in polling_server.et_subset if et.separation != 0]

        return len(set(non_zeros)) <= 1 #https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical

    # precondition: both polling servers satisfy separation requirements 
    def swap_ets(self, ps1, ps2):
        et_sep1 = [et for et in ps1.et_subset if et.separation != 0]
        et_sep2 = [et for et in ps2.et_subset if et.separation != 0]
        print("ayo we here")
        for et in et_sep1:
            ps1.et_subset.remove(et)

        for et in et_sep2:
            ps2.et_subset.remove(et)

        ps1.et_subset += et_sep2
        ps2.et_subset += et_sep1

        # maybe not assert here...
        assert self.verify_separation_req(ps1) and self.verify_separation_req(ps2)

    # lists are mutable and passed by reference, we do not need to pass anything

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
