import unittest
from taskType import TaskType
from task import Task
from cost_functions import calculate_schedulabiltiy

class CheckSchedulabilityTests(unittest.TestCase):
    
    #subset is schedulable 
    def testIsSchedulable(self):
        
        #name, duration, period, tasktype, priority, deadline
        task0 = Task("tET0", 1, 3, TaskType.EVENT, 7, 3) 
        task1 = Task("tET1", 2, 4, TaskType.EVENT, 7, 4)
        et_subset = [task0, task1]

        #ps = name, duration, period, tasktype, priority, deadline, et_subset
        ps0 = Task("tTTps0", 5, 3, TaskType.TIME, 1, 3, et_subset)

        is_schedulable, result_dict = calculate_schedulabiltiy(ps0)
        self.assertEqual(is_schedulable, True)

    #subset is not schedulable
    def testIsNotSchedulable(self):
        task0 = Task("tET0", 1, 3, TaskType.EVENT, 8, 1) 
        task1 = Task("tET1", 2, 4, TaskType.EVENT, 7, 4)
        et_subset = [task0, task1]

        #ps = name, duration, period, tasktype, priority, deadline, et_subset
        ps0 = Task("tTTps0", 10000, 100000, TaskType.TIME, 7, 1, et_subset)

        is_schedulable, result_dict = calculate_schedulabiltiy(ps0)
        self.assertEqual(is_schedulable, False)


if __name__ == '__main__':
    unittest.main()