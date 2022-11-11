from shared.models.task import Task
from shared.models.taskType import TaskType
from shared.cost_functions import *
import unittest

# 2 feasible 2 infeasible for each. test the last case where ready list not empty??
class TestEDF(unittest.TestCase):    
    # feasible
    def test_edf_case_1(self):
        # create task set
        task0 = Task("tTT0", 1, 3, TaskType.TIME, 7, 3) 
        task1 = Task("tTT1", 2, 4, TaskType.TIME, 7, 4)
        task_set = [task0, task1]
        
        # obatin schedule and wcrts
        s, wcrts = edf(task_set)

        # both valid options for task set. no order defined when deadline equal
        schedule_1_opt1 = ["tTT0", "tTT1", "tTT1", "tTT0", "tTT1", "tTT1", \
            "tTT0", "IDLE", "tTT1", "tTT1", "tTT0", "IDLE"]
        
        schedule_1_opt2 = ["tTT0", "tTT1", "tTT1", "tTT0", "tTT1", "tTT1", \
            "tTT0", "IDLE", "tTT1", "tTT1", "tTT0", "IDLE"]
        
        schedule_options = [schedule_1_opt1, schedule_1_opt2]
        
        self.assertIn(s, schedule_options) 
    
    # feasible. from hard real time p. 102
    def test_edf_case_2(self):
        task0 = Task("tTT0", 2, 5, TaskType.TIME, 7, 5) 
        task1 = Task("tTT1", 4, 7, TaskType.TIME, 7, 7)
        task_set = [task0, task1]

        schedule = ["tTT0", "tTT0", "tTT1", "tTT1", "tTT1", "tTT1", "tTT0", \
            "tTT0", "tTT1", "tTT1", "tTT1", "tTT1", "tTT0", "tTT0", "tTT1", \
            "tTT0", "tTT0", "tTT1", "tTT1", "tTT1", "tTT0", "tTT0", "tTT1", \
            "tTT1", "tTT1", "tTT1", "tTT0", "tTT0", "tTT1", "tTT1", "tTT1", \
            "tTT1", "tTT0", "tTT0", "IDLE"]

        s, wcrts = edf(task_set)

        self.assertListEqual(s, schedule)

    # not feasible
    def test_edf_case_3(self): 
        task0 = Task("tTT0", 2, 3, TaskType.TIME, 7, 3) 
        task1 = Task("tTT1", 2, 4, TaskType.TIME, 7, 4)
        task_set = [task0, task1]

        s, wcrts = edf(task_set)
        self.assertListEqual(s, [])

    # not feasible
    def test_edf_case4(self):
        task0 = Task("tTT0", 1, 2, TaskType.TIME, 7, 2) 
        task1 = Task("tTT1", 3, 4, TaskType.TIME, 7, 4)
        task_set = [task0, task1]

        s, wcrts = edf(task_set)
        self.assertEqual(s, [])

    # not feasible 
    def test_edf_case5(self):
        task0 = Task("tTT0", 1, 2, TaskType.TIME, 7, 2) 
        task1 = Task("tTT1", 1, 3, TaskType.TIME, 7, 3) 
        task2 = Task("tTT2", 3, 4, TaskType.TIME, 7, 4) 
        
        task_set = [task0, task1, task2]

        s, wcrts = edf(task_set)

        self.assertListEqual(s, [])


        
if __name__ == "__main__":
    unittest.main()

