import math
import copy 
from functools import reduce
from shared.models.task import Task

# not used anymore 
def get_ready(task_set, cycle, ready_list):
    for task in task_set:
        if cycle % task.period == 0:
            new_job = copy.deepcopy(task)
            new_job.deadline = new_job.deadline + cycle
            new_job.release_time = cycle
            ready_list.append(new_job)
    
    # sort on deadline 
    ready_list = sorted(ready_list, key=lambda t: t.deadline) # https://www.geeksforgeeks.org/sorting-objects-of-user-defined-class-in-python/ 
    
    return ready_list

# processor demand. see section 4.6 of hard real time 
def processor_demand_criterion(t1, t2, task_set):

    # phase or capital phi is 0 for all task in our case
    # for some task demand = duration*number_of_instances_interval 
    demand = sum([max(0, (t2 + task.period - task.deadline - t1) / task.period) * task.duration for task in task_set])
    
    # task set is schedulable if processor demand does not exceed available time  
    return demand <= (t2 - t1)

# release new task instance
def create_job(cycle, task): # create new instance instead of deepcopy. Tried using list instead of task object. doesnt seem better and less readble 
    new_job = Task(task.name, task.duration, task.period, task.type, task.priority, task.deadline + cycle, et_subset=task.et_subset)
    #new_job.deadline = new_job.deadline + cycle
    new_job.release_time = cycle

    return new_job 

# microticks to get to next point at which some task will be relased
def steps_to_next_release(cycle, task_set):
    return min([task.period - (cycle % task.period) for task in task_set])
        
# ts is set of TT tasks
def edf(ts):
    periods = [t.period for t in ts]
    T = math.lcm(*periods) # least common multiple of TT task periods
    s = [] # schedule will be hyperperiod long. 12 000 microticks == 120 000 microsecs == 120 ms
    ready_list = [] 
    wcrts = {} # worst case response times
    is_schedulable = True
    # total amount of computation time needed exceeding available time -> not schedulable
    if not processor_demand_criterion(0, T, ts): 
        #return [], -1 
        is_schedulable = False

    # return same thing in all failed cases, just empty list fx!! 
    t = 0
    while t < T:
        for task in ready_list:
            if task.duration > 0 and task.deadline <= t:
                #return [], -1 # just return 1 here maybe lol?
                is_schedulable = False

        # release task at time t
        ready_list = ready_list + [create_job(t, task) for task in ts if t % task.period == 0]     

        if ready_list == []:
            # increase period to next task's release
            steps_to_skip = steps_to_next_release(t, ts)
            t += steps_to_skip
            
            # append steps_to_skip amount of IDLEs to schedule
            s.extend(["IDLE"] * steps_to_skip)
            continue
        else:
            # EDF get next job to execute  
            ed_job = min(ready_list, key=lambda x: x.deadline)
            s.append(ed_job.name)
            ed_job.duration = ed_job.duration - 1

            # 31 october addition to assignment
            if ed_job.duration == 0 and ed_job.deadline >= t:
                response_time = t - ed_job.release_time 
                
                if ed_job.name not in wcrts or response_time >= wcrts[ed_job.name]: 
                    wcrts[ed_job.name] = response_time 
                 
                ready_list.remove(ed_job)

        # increment cycle counter
        t += 1

    # not feasible if ready list is not empty after hyperperiod
    if ready_list != []:
        #return [], -1
        is_schedulable = False

    #print("in EDF wcrts is: ", wcrts)
    return s, wcrts, is_schedulable

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
    is_schedulable = True
    #compute delta and alpha accordingly to [2]
    Delta = Tp + Dp - 2*Cp
    #Original -> Using lower bound: alpha = Cp/Tp (from [1]^2)
    #We use the so-called linear supply lower bound function lslbf (t) (c.f. [9]) with α = Cp/Tp and ∆ = Tp + Dp − 2*Cp, as lslbf (t) = max{0, (t − ∆)*α}.
    #Ext3: Use the actual server supply function called A_s(t) which can be determined from the schedule table
    #   This will be done by remove alpha, and thereby saying the supply at e.g tick 2 is 2 - that way it will remove the pessimism
    alpha = Cp/Tp

    #hyperperiod is lcm of all task periods in T_ET (all values must be from the chosen subset of ET tasks from the .csv)
    periods = [t.period for t in et_tasks]
     
    hyperperiod = math.lcm(*periods)
    
    for et_task in et_tasks:
        (pi, Ci, Ti, Di) = unpack(et_task)
        t = 0
        #initialize the response time of ti (task period) to a value exceeding the deadline
        response_time = Di + 1

        #remember we are dealing with constrained deadline tasks for the AdvPoll, hence, in the worst case arrival pattern, the intersection must lie within the hyperperiod if the task is schedulable

        while t <= hyperperiod:
            #the supply at time t ([1])
            supply = alpha*(t-Delta)
            #EXT3:
            #supply = t-Delta

            #compute the maximum demand at time t according to Eq. 2
            demand = 0
            for tj in et_tasks:
                (pj, Cj, Tj, Dj) = unpack(tj)

                if pj >= pi:
                    demand = demand + math.ceil(t/Tj)*Cj
            
            #According to lemma 1 of [1], we are searching for the earliest time, when the supply exceeds the demand
            if supply >= demand:
                response_time = t
                result_dict[et_task.name] = (response_time, et_task.deadline) # if actually greater than deadline, set to false later
                break
            
            t = t + 1
        
        if response_time > Di: 
            is_schedulable = False # TODO maybe just return here ... and penalize with 1 
            result_dict[et_task.name] = (response_time, et_task.deadline)
            return is_schedulable, result_dict 
        
    return is_schedulable, result_dict # contains wcrtbool indicating schedulability and deadline for each et

# sum of average worst case response time for tt tasks and et tasks. penality for not schedulable
# also returns the schedule and boolean indicating schedulability 
def cost_f(task_set):
    polling_servers = [ps for ps in task_set if ps.et_subset != None] # get set of polling servers from task set
    l = [calculate_schedulabiltiy(ps) for ps in polling_servers] # check schedulability for each polling server
    
    wcrts_et = 0 # use worst case response time for cost metric
    is_schedulable = True # if some ps is not schedulable at some penalty to cost 
    
    # cost contribution of et tasks is the average of worst case response times
    # si costs for et is: (sum(wcrt_i/deadline_i) / len(et_subset)) /len(polling_servers)
    for element in l: 
        is_schedulable, wcrts = element
        
        wcrts_et += sum([wcrts[key][0] for key in wcrts]) / len(wcrts)
        
        if not is_schedulable:
            wcrts_et = wcrts_et + 0.2*wcrts_et # add penalty
         
    # do not divide by zero. 
    if l != []:
        wcrts_et *= 1/len(l) 
     
    # apply earliest deadline first 
    s, wcrts, is_schedulable = edf(task_set) 
    
    # handle case where some task isn't even run also by check if in dict
    sum_wcrts_tt = sum([wcrts[task.name] if task.name in wcrts else task.deadline + 100 for task in task_set ]) / len(task_set)
    if not is_schedulable: # penalize. do this to avoid ending up in a "false" minimum
        sum_wcrts_tt = sum_wcrts_tt + 0.2*sum_wcrts_tt 

    #print("cost et: ", wcrts_et, " cost tt: ", sum_wcrts_tt) 
    sum_avg_wcrts = (sum_wcrts_tt + wcrts_et)
 
    return s, sum_avg_wcrts, is_schedulable
