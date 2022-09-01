import os
import shutil
import sys

from task import Task
from taskType import TaskType


class CaseLoader:

    def load_test_case(self, test_case_name=""):
        print("Searching for test cases at:")
        path = "./test cases/" + test_case_name if len(test_case_name) > 0 else "./test cases"
        print(path)
        cases = {}

        if not os.path.exists(path):
            print(path + " does not exist.")
            return

        for root, dirs, files in os.walk(path):
            for fileName in files:
                case_name = root.split("/")[2]
                path = os.path.join(root, fileName)
                file = open(path, "r")
                lines = file.readlines()
                lines.pop(0)
                for line in lines:
                    values = line.split(";")
                    event_type = TaskType.TIME if values[4] == "TT" else TaskType.EVENT
                    task = Task(str(values[1]), int(values[2]), int(values[3]), event_type, int(values[5]),
                                int(values[6]))

                    if cases.get(case_name) is None:
                        cases[case_name] = []

                    cases[case_name].append(task)

        print("Loaded " + str(len(cases)) + " test case(s).")

        return cases
