import random
from math import lcm

from task import Task
from taskType import TaskType

""" 
    TODO look into random sampling of set library functions :D lots of homemade stuff here
"""

# constants for selecting what parameter to change when creating a neighboring solution
NUM_PS = 0
BUDGET = 1
PERIOD = 2
DEADLINE = 3
SUBSET = 5
SWAP_SEP = 4


# neighborhood class. class bc we want some state e.g. to keep a random number generator
class Neighborhood:
    def __init__(self):
        self.rand = random.Random()
        self.rand.seed()  # if no arguments passed system time is used as seed
        self.n_polling_servers = 0
        # restrict search space like this. only choose periods from here -> make hyperperiod < 10*12000. 12000 = lcm(2000,3000,4000)
        self.periods = [i for i in range(2, 2001) if lcm(i, 2000, 3000, 4000) <= 12000]

    # return dict m[separation] = list of ets with separation
    def get_separated_ets(self, et_tasks):
        ets_separated = {}
        for et in et_tasks:  # create map m[separation] = list of ets with separation
            if et.separation not in ets_separated:
                ets_separated[et.separation] = [et]  # create entry
            else:
                ets_separated[et.separation].append(et)  # append if key(=separation value) already present

        return ets_separated

    # create random polling servers with separation requirement 
    def create_random_pss_sep(self, et_tasks):
        ets_separated = self.get_separated_ets(et_tasks)

        ets_non_zero = [value for key, value in ets_separated.items() if key != 0]

        # create a random number of partitions of et zero tasks. et_zeros is list of list of ets with sep 0
        if len(ets_non_zero) == 0:
            et_zeros = self.partition_et_tasks(random.randint(1, 5),
                                               ets_separated[0]) if 0 in ets_separated else []
        else:
            et_zeros = self.partition_et_tasks(random.randint(1, len(ets_non_zero)),
                                               ets_separated[0]) if 0 in ets_separated else []

        # create polling servers
        polling_servers = [self.create_random_ps(subset + et_zeros.pop()) if et_zeros != [] \
                               else self.create_random_ps(subset) for subset in ets_non_zero]

        # make sure that separation requirement is fulfilled by every polling server
        for ps in polling_servers:
            if not self.verify_separation_req(ps):
                return -1  # find something to do here, should NOT happen

        return polling_servers

    # create a polling server with a given et subset and randomly chosen parameters
    def create_random_ps_old(self, et_subset):

        period = self.rand.randint(1, 20) * 10  # multiple of 10 to avoid hyperperiod exploding??
        deadline = min(period, (self.rand.randint(1, 20) * 10))  # do not allow deadline > period
        duration = min(self.rand.randint(1, 50), deadline)  # this seems like cheating hardcoding range

        # naming of polling servers is unique
        self.n_polling_servers += 1

        # find naming scheme,have to b unique, requires counting or sth, some state 
        return Task("tTTps" + str(self.n_polling_servers), duration, period, TaskType.TIME, 7, deadline, et_subset,
                    et_subset[0].separation)

    # create a polling server with a given et subset and randomly chosen parameters
    def create_random_ps(self, et_subset):

        period_index = self.rand.randint(0, len(self.periods) - 1)  # choose an index in list of precomputed periods
        period = self.periods[period_index]
        deadline = period
        duration = min(self.rand.randint(1, 50),
                       deadline - 1)  # restrict range of possible durations. restrict search space

        # naming of polling servers is unique
        self.n_polling_servers += 1

        # find naming scheme,have to b unique, requires counting or sth, some state
        return Task("tTTps" + str(self.n_polling_servers), duration, period, TaskType.TIME, 7, deadline, et_subset,
                    et_subset[0].separation, period_index=period_index)

    # partition list of et_tasks into n lists of et_tasks
    def partition_et_tasks(self, n, et_tasks):
        num_tasks = int(len(et_tasks) / n)
        polling_servers = [et_tasks[i * num_tasks:(i + 1) * num_tasks] for i in range(n - 1)]
        polling_servers += [et_tasks[(n - 1) * num_tasks:]]

        return polling_servers

    # without separation requirement
    def create_n_random_ps(self, n, et_tasks):
        et_subsets = self.partition_et_tasks(n, et_tasks)
        return [self.create_random_ps(et_subset) for et_subset in et_subsets]

    # get a subset of pses from victim, delete these from victim and return them. only operate on sep 0
    def create_ps_subset(self, victim_ps):
        # number of et_tasks to move
        num_et_tasks = self.rand.randint(1, max(1, len(victim_ps.et_subset) - 1))
        new_ps_et_subset = []

        # only get 0s
        for task in victim_ps.et_subset[0:num_et_tasks]:
            if task.separation == 0:
                new_ps_et_subset.append(task)

        # do not know how removing and iterating at same time works so loop twice
        for task in victim_ps.et_subset[0:num_et_tasks]:
            if task.separation == 0:
                victim_ps.et_subset.remove(task)

        return new_ps_et_subset

    def merge_ps_subsets(self, ps_giver, ps_receiver):
        ps_receiver.et_subset += ps_giver.et_subset

    def get_neighbor(self, polling_servers):

        # select parameter to change.
        parameter = self.rand.randint(NUM_PS, SWAP_SEP)  # both bounds included

        # select polling server to operate on
        victim_ps = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

        # increase or decrease chosen parameter
        sign = 1 if self.rand.randint(0, 1) == 0 else -1

        # if sign positive add a polling server if negative remove one
        # when adding a polling server take some et tasks from victim
        if parameter == NUM_PS:
            self.num_ps(sign, polling_servers, victim_ps, self.rand)

        elif parameter == BUDGET:  # change budget of victim
            self.budget(victim_ps, sign)

        # we add/subtract sum number divisible by 10 and <= 100
        elif parameter == PERIOD:  # change period of victim. we do not accept period < deadline, but we could also just let sa handle it
            self.period(victim_ps, sign)

        elif parameter == DEADLINE:  # change deadline of victim
            self.deadline(victim_ps, sign)

        elif parameter == SUBSET:  # move et tasks from one ps to another
            if len(polling_servers) == 1:  # if no one to steal from
                pass
            else:
                self.subset(polling_servers, victim_ps)

        elif parameter == SWAP_SEP:
            other_ps_victim = self.get_different_ps(polling_servers, victim_ps)
            self.swap_ets(victim_ps, other_ps_victim)

        return polling_servers

    # function for parameter NUM_PS. add or remove a polling server
    def num_ps(self, sign, polling_servers, victim_ps, rand):
        if sign == 1 and len(
                polling_servers) < 7:  # TODO find some way to determine max num polling servers or if we should even have
            new_et_subset = self.create_ps_subset(victim_ps)  # get separation 0s

            # if no 0s nothing to do
            if len(new_et_subset) != 0:
                new_ps = self.create_random_ps(new_et_subset)
                polling_servers.append(new_ps)

            # remove victim from task set if it does not have any et tasks
            if victim_ps.et_subset == []:
                polling_servers.remove(victim_ps)
        else:
            if len(polling_servers) > 1:  # do not make set of polling servers empty
                # use get different here
                receiver_ps = self.get_different_ps(polling_servers, victim_ps)

                # we just need a single value. but doing it like this helps us checking that ps only has sep 0s
                victim_separation = [et.separation for et in victim_ps.et_subset if et.separation != 0]
                receiver_separation = [et.separation for et in receiver_ps.et_subset if et.separation != 0]

                # only remove polling server and merge ets into receiver if one of
                # them only contains 0s or both of them have same sep ets (we never end up in this situation)
                if len(victim_separation) == 0 or len(receiver_separation) == 0 \
                        or victim_separation[0] == receiver_separation[0]:
                    self.merge_ps_subsets(victim_ps, receiver_ps)  # transfer all et tasks from victim to receiver

                    polling_servers.remove(victim_ps)  # remove victim from set of polling servers

    # function for parameter BUDGET
    def budget(self, victim_ps, sign):
        victim_ps.duration = max(1, victim_ps.duration + sign)  # avoid negative
        victim_ps.duration = min(victim_ps.duration, victim_ps.deadline)  # do not accept duration > deadline

    # function for parameter PERIOD
    def period(self, victim_ps, sign):
        # avoid stepping out of list bound
        if victim_ps.period_index + sign == len(self.periods):
            sign = -1
        elif victim_ps.period_index + sign == -1:
            sign = 1

        victim_ps.period_index = victim_ps.period_index + sign  # move up or down the list
        victim_ps.period = self.periods[
            victim_ps.period_index]  # get closest period that does not make hyperperiod > 10*12000

        # victim_ps.period = max(victim_ps.period, victim_ps.deadline)  # do not accept period < deadline for now
        # victim_ps.deadline = victim_ps.period # if period always = deadline we find solution more often - robust but they are not as good as when deadline can be < period
        victim_ps.deadline = min(victim_ps.period, victim_ps.deadline)

    # function for parameter DEADLINE
    def deadline(self, victim_ps, sign):
        # self.period(victim_ps, sign) # just doing nothing or changing period and having deadline=period generates solutions more often
        victim_ps.deadline = max(1, victim_ps.deadline + sign * 5)
        victim_ps.deadline = min(victim_ps.period, victim_ps.deadline)  # do not accept period < deadline

    # function for parameter SUBSET
    def subset(self, polling_servers, victim_ps):
        other_ps_victim = self.get_different_ps(polling_servers, victim_ps)

        # get some et tasks from other ps victim, delete these from this ps. only gets 0s
        new_ps_et_subset = self.create_ps_subset(other_ps_victim)

        # remove other victim from task set if it does not have any et tasks
        if other_ps_victim.et_subset == []:
            polling_servers.remove(other_ps_victim)

            # add et tasks to victim ps
        victim_ps.et_subset += new_ps_et_subset

    # randomly choose a polling server that is different from victim
    def get_different_ps(self, polling_servers, victim_ps):
        other_victim_ps = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

        while other_victim_ps == victim_ps:
            other_victim_ps = polling_servers[self.rand.randint(0, len(polling_servers) - 1)]

        return other_victim_ps

    # true if only contains ets of one sep type 
    def verify_separation_req(self, polling_server):
        non_zeros = [et.separation for et in polling_server.et_subset if et.separation != 0]

        return len(
            set(non_zeros)) <= 1  # https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical

    # precondition: both polling servers satisfy separation requirements
    def swap_ets(self, ps1, ps2):
        et_sep1 = [et for et in ps1.et_subset if et.separation != 0]  # ps1 has sep = x
        et_sep2 = [et for et in ps2.et_subset if et.separation != 0]  # ps2 has sep = y

        for et in et_sep1:
            ps1.et_subset.remove(et)

        for et in et_sep2:
            ps2.et_subset.remove(et)

        ps1.et_subset += et_sep2  # ps1 now has sep = y
        ps2.et_subset += et_sep1  # ps2 now has sep = x

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
