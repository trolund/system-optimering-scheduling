import unittest
from taskType import TaskType
from task import Task
from cost_functions import calculate_schedulabiltiy

class CheckSchedulabilityTests(unittest.TestCase):

    #define ET subsets and polling server tasks here
    # create task set
    task0 = Task("tET0", 1, 3, TaskType.EVENT, 7, 3) 
    task1 = Task("tET1", 2, 4, TaskType.EVENT, 7, 4)
    et_subset = [task0, task1]

    #ps = name, duration, period, tasktype, priority, deadline, et_subset
    ps0 = Task("tTTps0", 5, 3, TaskType.TIME, 1, 3, et_subset)

    #Create tasks that are not schedulable, expect 
    def isNotSchedulable(self):
        is_schedulable, result_dict = calculate_schedulability(ps0)
        self.print(is_schedulable)
    

    #Create tasks that are schedulable
    def isSchedulable(self):
        return "Not implemented"


if __name__ == '__main__':
    unittest.main()