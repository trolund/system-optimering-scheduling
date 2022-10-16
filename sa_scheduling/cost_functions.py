import math
import copy 
from functools import reduce

def get_ready(task_set, cycle, ready_list):
    for task in task_set:
        if cycle % task.period == 0:
            new_job = copy.deepcopy(task)
            new_job.deadline = new_job.deadline + cycle
            new_job.release_time = cycle
            ready_list.append(new_job)
    
    # sort on deadline
    # https://www.geeksforgeeks.org/sorting-objects-of-user-defined-class-in-python/
    ready_list = sorted(ready_list, key=lambda t: t.deadline) 
    
    return ready_list
        

# ts is set of TT tasks
def edf(ts):
    #print("in edf: ", ts[-1].name, ts[-1].duration, ts[-1].period, ts[-1].deadline)
    periods = [t.period for t in ts]
    T = math.lcm(*periods) # least common multiple of TT task periods. 2000 mt = 
    #print(T)
    s = [] # schedule will be hyperperiod long. 12 000 microticks == 120 000 microsecs == 120 ms
    ready_list = []
    wcrts = {} # worst case response times
    
    # overvej reset funktioner i task klassen istedet for alle de kopier...
    for t in range(0, T):
        for task in ready_list:
            if task.duration > 0 and task.deadline <= t:
                #print(t)
                #for task in ready_list:
                #    print("name: ", task.name, " duration: ", task.duration, " deadline: ", task.deadline, " period: ", task.period, " release: ", task.release_time)
                return s, -1
        
            # job done check response time gt wcrt and remove from ready list
            if task.duration == 0 and task.deadline >= t:
                response_time = t - task.release_time
                
                if task.name not in wcrts or response_time >= wcrts[task.name]:
                    wcrts[task.name] = response_time
                
                ready_list.remove(task)
                
        # release taks at time t
        ready_list = get_ready(ts, t, ready_list)

        if ready_list == []:
            s.append("IDLE")
            continue
        else:
            # EDF get next job to execute 
            s.append(ready_list[0].name)
            ready_list[0].duration = ready_list[0].duration - 1
    
    if ready_list != []:
        return [], wcrts
    
    #print("in EDF wcrts is: ", wcrts)
    
    return s, wcrts

# utility function 
def unpack(task):
    return (task.priority, task.duration, task.period, task.deadline)

#Schedulability of ET tasks under a given polling task
def calculate_schedulabiltiy(polling_server):
    et_tasks = polling_server.et_subset
    Tp = polling_server.period
    Dp = polling_server.deadline
    Cp = polling_server.duration
    result_dict = {}
    
    #compute delta and alpha accordingly to [2]
    Delta = Tp + Dp - 2*Cp
    alpha = Cp/Tp
    
    #hyperperiod is lcm of all task periods in T_ET (all values must be from the chosen subset of ET tasks from the .csv)
    periods = [t.period for t in et_tasks]
    #for task in et_tasks:
    #    (pi, Ci, Ti, Di) = unpack(task)
    #    periods.append(Ti)

    
    hyperperiod = math.lcm(*periods)
    #print("hyperperiod ets is ", hyperperiod)

    for et_task in et_tasks:
        (pi, Ci, Ti, Di) = unpack(et_task)
        t = 0
        #initialize the response time of ti (task period) to a value exceeding the deadline
        response_time = Di + 1

        #remember we are dealing with constrained deadline tasks for the AdvPoll, hence, in the worst case arrival pattern, the intersection must lie within the hyperperiod if the task is schedulable

        while t <= hyperperiod:
            #the supply at time t ([1])
            supply = alpha*(t-Delta)

            #compute the maximum demand at time t according to Eq. 2
            demand = 0
            for tj in et_tasks:
                (pj, Cj, Tj, Dj) = unpack(tj)

                if pj >= pi:
                    demand  = demand + math.ceil(t/Tj)*Cj
            
            #According to lemma 1 of [1], we are searching for the earliest time, when the supply exceeds the demand
            if supply >= demand:
                response_time = t
                result_dict[et_task.name]  = (True, response_time, et_task.deadline) # if actually greater than deadline, set to false later
                break
            
            t = t + 1
        
        if response_time > Di:
            result_dict[et_task.name] = (False, response_time, et_task.deadline)
            
        
    return result_dict # contains wcrtbool indicating schedulability and deadline for each et



# cost is sum of worst case response times of tt tasks + sum worst case respone times for et tasks
# the wcrt of tt/et task i is multiplied by 1/deadline_i to normalize it
# the sum of wcrts tt is multiplied by 1/len(tt_task_set) and 1/len(et_task_set) for wcrts of et tasks
# this gives us a number betwen 0 and 1 for both tt and et 
# add these two together and get a number between 0 and 2
# use this as cost 
def cost_f(task_set):
    polling_servers = [ps for ps in task_set if ps.et_subset != None] # get set of polling servers from task set 
    
    l = [calculate_schedulabiltiy(ps) for ps in polling_servers] # check schedulability for each polling server
    
    wcrts_et = 0 # use worst case response time for cost metric
    is_schedulable = True # if some ps is not schedulable at some penalty to cost 
    
    # a little convoluted but add wcrts for ets in each polling server
    # if not schedulable add some penalty 1 instead of 1 / deadline_et_i
    # the is schedulable variable is used in sa right now but find better solution
    for entry in l: 
        wcrts_et += (sum([(entry[key][1] / entry[key][2]) if entry[key][0] else 1 for key in entry]) / len(entry))
        is_schedulable = is_schedulable and reduce((lambda a, b : a and b), [entry[key][0] for key in entry]) # https://www.geeksforgeeks.org/reduce-in-python/ 
    
    # normalize such that 0 <= cost <= 1 
    if l != []:
        wcrts_et *= 1/len(l) 

    # apply earliest deadline first 
    s, wcrts = edf(task_set)
    
    # if not tt tasks not schedulable (-1) return faulty schedule, 2 (max cost the way we normalize right now)
    # and false (not schedulable)
    if wcrts == -1:
        return s, 2, False
    
    # normalize worst case response time. for each tt task 0 <= wcrt <= 1 by setting it to wcrt/deadline
    sum_wcrts_tt = sum([wcrts[task.name] / task.deadline for task in task_set])
     

    # normalize cost of    
    sum_wcrts_tt = sum_wcrts_tt / len(task_set)
    sum_wcrts = (sum_wcrts_tt + wcrts_et)

    #alternative 0 <= sum <= 1 by doing sum/2 ..
    assert 0 <= sum_wcrts and sum_wcrts <= 2
    
    return s, sum_wcrts, is_schedulable