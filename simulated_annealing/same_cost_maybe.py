from taskType import TaskType
from caseLoader import CaseLoader
from neighborhood import Neighborhood
from cost_functions import *

loader = CaseLoader() # load test case 
test_file = ["testcases_seperation_tested", 20]

all_tasks = loader.load_test_case("../test_cases/testcases_seperation_tested/taskset__1643188157-a_0.2-b_0.2-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__20__tsk.csv")
print(all_tasks) 
neighborhood = Neighborhood()

tt_tasks = [t for t in all_tasks if t.type == TaskType.TIME]
et_tasks = [t for t in all_tasks if t.type == TaskType.EVENT]

et_map = {}
for et_t in et_tasks:
    et_map[et_t.name] = et_t

et_subset1 = [et_map["tET1"], et_map["tET19"], et_map["tET13"], et_map["tET14"], et_map["tET6"],et_map["tET2"], et_map["tET11"] ]
ps1 = Task("ps1", 3, 15, TaskType.TIME, 7, 15, et_subset=et_subset1)

#ps1 = Task("ps1", 3, 15, TaskType.TIME, 7, deadline, et_subset, et_subset[0].separation, period_index=period_index)
et_subset2 = [et_map["tET3"], et_map["tET5"], et_map["tET8"], et_map["tET16"], et_map["tET12"], et_map["tET7"], et_map["tET15"], et_map["tET18"], et_map["tET0"]]
ps2 = Task("ps2", 5, 20, TaskType.TIME, 7, 12, et_subset=et_subset2)

et_subset3 = [et_map["tET9"], et_map["tET17"], et_map["tET4"], et_map["tET10"]]
ps3 = Task("ps3", 3, 40, TaskType.TIME, 7, 26, et_subset=et_subset2)

tt_tasks = tt_tasks + [ps1, ps2, ps3]

s, sum_avg_wcrts, is_schedulable = cost_f(tt_tasks)

print(sum_avg_wcrts, " ", is_schedulable)





