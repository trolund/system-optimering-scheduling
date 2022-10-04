#Schedulability of ET tasks under a given polling task

#Data:
#polling task budget: Cp
#polling task period: Tp
#polling task deadline: Dp
#subset of ET tasks to check Tau^ET (T_ET)
#pi = priority
#Ci = Computation time?
#ti = task period (tuple)

#result: small_tau (Boolean)

####


import math


def unpack(task):
    return (task.priority, task.duration, task.period, task.deadline)

def calculate_schedulabiltiy(Tp, Dp, Cp, task_periods):
    #compute delta and alpha accordingly to [2]
    Delta = Tp + Dp - 2*Cp
    alpha = Cp/Tp
    
    #hyperperiod is lcm of all task periods in T_ET (all values must be from the chosen subset of ET tasks from the .csv)
    periods = []
    for task in task_periods:
        (pi, Ci, Ti, Di) = unpack(task)
        periods.append(Ti)

    hyperperiod = math.lcm(*periods)

    #loop
    for task_period in task_periods:
        (pi, Ci, Ti, Di) = unpack(task_period)
        t = 0
        #initialize the response time of ti (task period) to a value exceeding the deadline
        response_time = Di + 1

        #remember we are dealing with constrained deadline tasks for the AdvPoll, hence, in the worst case arrival pattern, the intersection must lie within the hyperperiod if the task is schedulable

        while t <= hyperperiod:
            #the supply at time t ([1])
            supply = alpha*(t-Delta)

            #compute the maximum demand at time t according to Eq. 2
            demand = 0
            for tj in task_periods:
                (pj, Cj, Tj, Dj) = unpack(tj)

                if pj >= pi:
                    demand  = demand + math.ceil(t/Tj)*Cj
            
            #According to lemma 1 of [1], we are searching for the earliest time, when the supply exceeds the demand
            if supply >= demand:
                response_time = t
                break
            
            t = t +1
        
            if response_time >= Di:
                return False
        
    return True



