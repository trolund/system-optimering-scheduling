import random
from caseloader import CaseLoader
from enum import Enum

from caseloader import TaskType

# get a subset of pses from victim and delete these from victim
# -2 as to not steal all :)
def get_subset(case_name, case_id):
     #load in test case
    loader = CaseLoader()
    tasks = loader.load_test_case(case_name, case_id)
    ets = [t for t in tasks if t.type == TaskType.EVENT]

    num_et_tasks = random.randint(0, len(ets))
    new_ps_et_subset = []
        
    for i in range(num_et_tasks):
        new_ps_et_subset.append(ets[i])

    return new_ps_et_subset