import sys
sys.path.insert(1, "../")
from shared.models.task import Task
from shared.models.taskType import TaskType
from shared.cost_functions import *
from shared.caseLoader import CaseLoader
from shared.neighborhood import Neighborhood
from shared.cost_functions import *
import unittest

# ONLY works when running in terminal for some weird reason 

# 2 feasible 2 infeasible for each. test the last case where ready list not empty??
class TestNeighborhood(unittest.TestCase):

    # test that ets are separeted into lists properly 
    def test_separate_ets_into_lists(self): # using file taskset__1643188013-a_0.1-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__0__tsk.csv
        loader = CaseLoader() # load test case 
        test_file = ["testcases_seperation_tested", 0]
        all_tasks = loader.load_test_case(test_file[0], test_file[1])
        print(all_tasks) 
        neighborhood = Neighborhood()

        tt_tasks = [t for t in all_tasks if t.type == TaskType.TIME]
        et_tasks = [t for t in all_tasks if t.type == TaskType.EVENT]

        d = neighborhood.get_separated_ets(et_tasks)

        # inspecting file there should be 5 1s, 8 2s, 7 3s 
        self.assertEqual(len(d[1]), 5)
        self.assertEqual(len(d[2]), 8)
        self.assertEqual(len(d[3]), 7)  
        # 19 et tasks totally test if all present  
        names = []
        for key, val in d.items(): 
            for et in val:
                names.append(et.name) 
                 
        self.assertEqual(len(names), 20)
         
    # test that polling servers are generated correctly somehow
    def test_polling_server_separation(self):
        loader = CaseLoader() # load test case 
        test_case = ["testcases_seperation_tested", 0]
        
        all_tasks = loader.load_test_case(test_case[0], test_case[1])   
        neighborhood = Neighborhood()
        
        tt_tasks = [t for t in all_tasks if t.type == TaskType.TIME]
        et_tasks = [t for t in all_tasks if t.type == TaskType.EVENT]

        polling_servers = neighborhood.create_random_pss_sep(et_tasks)

        for polling_server in polling_servers:
            self.assertLessEqual(len(set([et.separation for et in polling_server.et_subset])), 2)


if __name__ == "__main__":
    unittest.main()

