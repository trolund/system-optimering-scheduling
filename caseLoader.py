import os
import shutil
import sys

from task import Task
from taskType import TaskType


class CaseLoader:

    def loadAllTestCases(self):
        print("Searching for test cases at:")
        path = "./test cases"
        print(path)
        tasks = []

        for root, dirs, files in os.walk(path):
            for fileName in files:
                path = os.path.join(root, fileName)
                file = open(path, "r")
                lines = file.readlines()
                lines.pop(0)
                for line in lines:
                    values = line.split(";")
                    event_type = TaskType.TIME if values[4] == "TT" else TaskType.EVENT
                    task = Task(str(values[1]), int(values[2]), int(values[3]), event_type, int(values[5]), int(values[6]))
                    tasks.append(task)

        print("Loaded " + str(len(tasks)) + " test cases.")

        return tasks
